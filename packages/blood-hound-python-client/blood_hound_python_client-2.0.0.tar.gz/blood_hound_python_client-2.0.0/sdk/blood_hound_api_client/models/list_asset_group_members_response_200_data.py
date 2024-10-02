from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_asset_group_member import ModelAssetGroupMember


T = TypeVar("T", bound="ListAssetGroupMembersResponse200Data")


@_attrs_define
class ListAssetGroupMembersResponse200Data:
    """
    Attributes:
        members (Union[Unset, List['ModelAssetGroupMember']]):
    """

    members: Union[Unset, List["ModelAssetGroupMember"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        members: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.members, Unset):
            members = []
            for members_item_data in self.members:
                members_item = members_item_data.to_dict()
                members.append(members_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if members is not UNSET:
            field_dict["members"] = members

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_asset_group_member import ModelAssetGroupMember

        d = src_dict.copy()
        members = []
        _members = d.pop("members", UNSET)
        for members_item_data in _members or []:
            members_item = ModelAssetGroupMember.from_dict(members_item_data)

            members.append(members_item)

        list_asset_group_members_response_200_data = cls(
            members=members,
        )

        list_asset_group_members_response_200_data.additional_properties = d
        return list_asset_group_members_response_200_data

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
