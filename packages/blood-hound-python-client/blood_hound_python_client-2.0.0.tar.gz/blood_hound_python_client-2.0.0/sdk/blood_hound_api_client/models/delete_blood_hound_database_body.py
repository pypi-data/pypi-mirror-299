from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteBloodHoundDatabaseBody")


@_attrs_define
class DeleteBloodHoundDatabaseBody:
    """
    Attributes:
        delete_collected_graph_data (Union[Unset, bool]):
        delete_file_ingest_history (Union[Unset, bool]):
        delete_data_quality_history (Union[Unset, bool]):
        delete_asset_group_selectors (Union[Unset, List[int]]):
    """

    delete_collected_graph_data: Union[Unset, bool] = UNSET
    delete_file_ingest_history: Union[Unset, bool] = UNSET
    delete_data_quality_history: Union[Unset, bool] = UNSET
    delete_asset_group_selectors: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        delete_collected_graph_data = self.delete_collected_graph_data

        delete_file_ingest_history = self.delete_file_ingest_history

        delete_data_quality_history = self.delete_data_quality_history

        delete_asset_group_selectors: Union[Unset, List[int]] = UNSET
        if not isinstance(self.delete_asset_group_selectors, Unset):
            delete_asset_group_selectors = self.delete_asset_group_selectors

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if delete_collected_graph_data is not UNSET:
            field_dict["deleteCollectedGraphData"] = delete_collected_graph_data
        if delete_file_ingest_history is not UNSET:
            field_dict["deleteFileIngestHistory"] = delete_file_ingest_history
        if delete_data_quality_history is not UNSET:
            field_dict["deleteDataQualityHistory"] = delete_data_quality_history
        if delete_asset_group_selectors is not UNSET:
            field_dict["deleteAssetGroupSelectors"] = delete_asset_group_selectors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        delete_collected_graph_data = d.pop("deleteCollectedGraphData", UNSET)

        delete_file_ingest_history = d.pop("deleteFileIngestHistory", UNSET)

        delete_data_quality_history = d.pop("deleteDataQualityHistory", UNSET)

        delete_asset_group_selectors = cast(List[int], d.pop("deleteAssetGroupSelectors", UNSET))

        delete_blood_hound_database_body = cls(
            delete_collected_graph_data=delete_collected_graph_data,
            delete_file_ingest_history=delete_file_ingest_history,
            delete_data_quality_history=delete_data_quality_history,
            delete_asset_group_selectors=delete_asset_group_selectors,
        )

        delete_blood_hound_database_body.additional_properties = d
        return delete_blood_hound_database_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
