from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAssetGroupCustomMemberCountResponse200")


@_attrs_define
class GetAssetGroupCustomMemberCountResponse200:
    """
    Attributes:
        custom_member_count (Union[Unset, int]):
    """

    custom_member_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        custom_member_count = self.custom_member_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if custom_member_count is not UNSET:
            field_dict["custom_member_count"] = custom_member_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_member_count = d.pop("custom_member_count", UNSET)

        get_asset_group_custom_member_count_response_200 = cls(
            custom_member_count=custom_member_count,
        )

        get_asset_group_custom_member_count_response_200.additional_properties = d
        return get_asset_group_custom_member_count_response_200

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
