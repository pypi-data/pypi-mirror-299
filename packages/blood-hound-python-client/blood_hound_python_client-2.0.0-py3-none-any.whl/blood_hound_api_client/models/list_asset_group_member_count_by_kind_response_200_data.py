from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_asset_group_member_count_by_kind_response_200_data_counts import (
        ListAssetGroupMemberCountByKindResponse200DataCounts,
    )


T = TypeVar("T", bound="ListAssetGroupMemberCountByKindResponse200Data")


@_attrs_define
class ListAssetGroupMemberCountByKindResponse200Data:
    """
    Attributes:
        total_count (Union[Unset, int]):
        counts (Union[Unset, ListAssetGroupMemberCountByKindResponse200DataCounts]):
    """

    total_count: Union[Unset, int] = UNSET
    counts: Union[Unset, "ListAssetGroupMemberCountByKindResponse200DataCounts"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_count = self.total_count

        counts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_count is not UNSET:
            field_dict["total_count"] = total_count
        if counts is not UNSET:
            field_dict["counts"] = counts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_asset_group_member_count_by_kind_response_200_data_counts import (
            ListAssetGroupMemberCountByKindResponse200DataCounts,
        )

        d = src_dict.copy()
        total_count = d.pop("total_count", UNSET)

        _counts = d.pop("counts", UNSET)
        counts: Union[Unset, ListAssetGroupMemberCountByKindResponse200DataCounts]
        if isinstance(_counts, Unset):
            counts = UNSET
        else:
            counts = ListAssetGroupMemberCountByKindResponse200DataCounts.from_dict(_counts)

        list_asset_group_member_count_by_kind_response_200_data = cls(
            total_count=total_count,
            counts=counts,
        )

        list_asset_group_member_count_by_kind_response_200_data.additional_properties = d
        return list_asset_group_member_count_by_kind_response_200_data

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
