from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelSearchResult")


@_attrs_define
class ModelSearchResult:
    """
    Attributes:
        objectid (Union[Unset, str]):
        type (Union[Unset, str]):
        name (Union[Unset, str]):
        distinguishedname (Union[Unset, str]):
        system_tags (Union[Unset, str]):
    """

    objectid: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    distinguishedname: Union[Unset, str] = UNSET
    system_tags: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        objectid = self.objectid

        type = self.type

        name = self.name

        distinguishedname = self.distinguishedname

        system_tags = self.system_tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if objectid is not UNSET:
            field_dict["objectid"] = objectid
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if distinguishedname is not UNSET:
            field_dict["distinguishedname"] = distinguishedname
        if system_tags is not UNSET:
            field_dict["system_tags"] = system_tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        objectid = d.pop("objectid", UNSET)

        type = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        distinguishedname = d.pop("distinguishedname", UNSET)

        system_tags = d.pop("system_tags", UNSET)

        model_search_result = cls(
            objectid=objectid,
            type=type,
            name=name,
            distinguishedname=distinguishedname,
            system_tags=system_tags,
        )

        model_search_result.additional_properties = d
        return model_search_result

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
