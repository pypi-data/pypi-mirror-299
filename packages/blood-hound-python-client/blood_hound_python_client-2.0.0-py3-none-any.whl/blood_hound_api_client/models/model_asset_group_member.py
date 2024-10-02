from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelAssetGroupMember")


@_attrs_define
class ModelAssetGroupMember:
    """
    Attributes:
        asset_group_id (Union[Unset, int]):
        object_id (Union[Unset, str]):
        primary_kind (Union[Unset, str]):
        kinds (Union[Unset, List[str]]):
        environment_id (Union[Unset, str]):
        environment_kind (Union[Unset, str]):
        name (Union[Unset, str]):
        custom_member (Union[Unset, bool]):
    """

    asset_group_id: Union[Unset, int] = UNSET
    object_id: Union[Unset, str] = UNSET
    primary_kind: Union[Unset, str] = UNSET
    kinds: Union[Unset, List[str]] = UNSET
    environment_id: Union[Unset, str] = UNSET
    environment_kind: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    custom_member: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asset_group_id = self.asset_group_id

        object_id = self.object_id

        primary_kind = self.primary_kind

        kinds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.kinds, Unset):
            kinds = self.kinds

        environment_id = self.environment_id

        environment_kind = self.environment_kind

        name = self.name

        custom_member = self.custom_member

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asset_group_id is not UNSET:
            field_dict["asset_group_id"] = asset_group_id
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if primary_kind is not UNSET:
            field_dict["primary_kind"] = primary_kind
        if kinds is not UNSET:
            field_dict["kinds"] = kinds
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if environment_kind is not UNSET:
            field_dict["environment_kind"] = environment_kind
        if name is not UNSET:
            field_dict["name"] = name
        if custom_member is not UNSET:
            field_dict["custom_member"] = custom_member

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset_group_id = d.pop("asset_group_id", UNSET)

        object_id = d.pop("object_id", UNSET)

        primary_kind = d.pop("primary_kind", UNSET)

        kinds = cast(List[str], d.pop("kinds", UNSET))

        environment_id = d.pop("environment_id", UNSET)

        environment_kind = d.pop("environment_kind", UNSET)

        name = d.pop("name", UNSET)

        custom_member = d.pop("custom_member", UNSET)

        model_asset_group_member = cls(
            asset_group_id=asset_group_id,
            object_id=object_id,
            primary_kind=primary_kind,
            kinds=kinds,
            environment_id=environment_id,
            environment_kind=environment_kind,
            name=name,
            custom_member=custom_member,
        )

        model_asset_group_member.additional_properties = d
        return model_asset_group_member

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
