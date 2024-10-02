from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelDomainDetails")


@_attrs_define
class ModelDomainDetails:
    """
    Attributes:
        objectid (Union[Unset, str]):
        name (Union[Unset, str]):
        exists (Union[Unset, bool]):
        type (Union[Unset, str]):
    """

    objectid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    exists: Union[Unset, bool] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        objectid = self.objectid

        name = self.name

        exists = self.exists

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if objectid is not UNSET:
            field_dict["objectid"] = objectid
        if name is not UNSET:
            field_dict["name"] = name
        if exists is not UNSET:
            field_dict["exists"] = exists
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        objectid = d.pop("objectid", UNSET)

        name = d.pop("name", UNSET)

        exists = d.pop("exists", UNSET)

        type = d.pop("type", UNSET)

        model_domain_details = cls(
            objectid=objectid,
            name=name,
            exists=exists,
            type=type,
        )

        model_domain_details.additional_properties = d
        return model_domain_details

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
