from collections import defaultdict
from functools import cached_property
from typing import AbstractSet, Mapping, Set, cast

from dagster import (
    AssetKey,
    Definitions,
    _check as check,
)
from dagster._record import record
from dagster._serdes.serdes import deserialize_value

from dagster_airlift.constants import STANDALONE_DAG_ID_METADATA_KEY
from dagster_airlift.core.airflow_instance import AirflowInstance
from dagster_airlift.core.serialization.compute import AirliftMetadataMappingInfo
from dagster_airlift.core.serialization.defs_construction import make_default_dag_asset_key
from dagster_airlift.core.serialization.serialized_data import (
    SerializedAirflowDefinitionsData,
    TaskHandle,
)
from dagster_airlift.core.utils import get_metadata_key, is_mapped_asset_spec, task_handles_for_spec


@record
class AirflowDefinitionsData:
    airflow_instance: AirflowInstance
    mapped_defs: Definitions

    @property
    def instance_name(self) -> str:
        return self.airflow_instance.name

    @cached_property
    def mapping_info(self) -> AirliftMetadataMappingInfo:
        return AirliftMetadataMappingInfo(asset_specs=list(self.mapped_defs.get_all_asset_specs()))

    def task_ids_in_dag(self, dag_id: str) -> Set[str]:
        return self.mapping_info.task_id_map[dag_id]

    @cached_property
    def serialized_data(self) -> SerializedAirflowDefinitionsData:
        regular_metadata_key = get_metadata_key(self.airflow_instance.name)
        automapped_metadata_key = regular_metadata_key + "/full_automapped_dags"
        check.invariant(
            any(
                metadata_key in self.mapped_defs.metadata
                for metadata_key in [regular_metadata_key, automapped_metadata_key]
            ),
            "Expected at least one of the possible metadata keys to be present",
        )
        serialized_data_str = (
            self.mapped_defs.metadata[regular_metadata_key].value
            if regular_metadata_key in self.mapped_defs.metadata
            else self.mapped_defs.metadata[automapped_metadata_key].value
        )
        return deserialize_value(
            cast(str, serialized_data_str), as_type=SerializedAirflowDefinitionsData
        )

    @property
    def all_dag_ids(self) -> AbstractSet[str]:
        return set(self.serialized_data.dag_datas.keys())

    @cached_property
    def asset_keys_per_task_handle(self) -> Mapping[TaskHandle, AbstractSet[AssetKey]]:
        asset_keys_per_handle = defaultdict(set)
        for spec in self.mapped_defs.get_all_asset_specs():
            if is_mapped_asset_spec(spec):
                task_handles = task_handles_for_spec(spec)
                for task_handle in task_handles:
                    asset_keys_per_handle[task_handle].add(spec.key)
        return asset_keys_per_handle

    @cached_property
    def asset_key_per_dag(self) -> Mapping[str, AssetKey]:
        dag_id_to_asset_key = {}
        for spec in self.mapped_defs.get_all_asset_specs():
            if STANDALONE_DAG_ID_METADATA_KEY in spec.metadata:
                dag_id = spec.metadata[STANDALONE_DAG_ID_METADATA_KEY]
                dag_id_to_asset_key[dag_id] = spec.key
        return dag_id_to_asset_key

    def asset_key_for_dag(self, dag_id: str) -> AssetKey:
        return make_default_dag_asset_key(self.serialized_data.instance_name, dag_id)

    def asset_keys_in_task(self, dag_id: str, task_id: str) -> AbstractSet[AssetKey]:
        return self.asset_keys_per_task_handle[TaskHandle(dag_id=dag_id, task_id=task_id)]
