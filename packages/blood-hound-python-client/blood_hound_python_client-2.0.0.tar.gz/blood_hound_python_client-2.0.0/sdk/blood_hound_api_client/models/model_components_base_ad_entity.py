from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelComponentsBaseAdEntity")


@_attrs_define
class ModelComponentsBaseAdEntity:
    """
    Attributes:
        objectid (Union[Unset, str]):
        name (Union[Unset, str]):
        exists (Union[Unset, bool]):
    """

    objectid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    exists: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        objectid = self.objectid

        name = self.name

        exists = self.exists

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if objectid is not UNSET:
            field_dict["objectid"] = objectid
        if name is not UNSET:
            field_dict["name"] = name
        if exists is not UNSET:
            field_dict["exists"] = exists

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        objectid = d.pop("objectid", UNSET)

        name = d.pop("name", UNSET)

        exists = d.pop("exists", UNSET)

        model_components_base_ad_entity = cls(
            objectid=objectid,
            name=name,
            exists=exists,
        )

        model_components_base_ad_entity.additional_properties = d
        return model_components_base_ad_entity

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
