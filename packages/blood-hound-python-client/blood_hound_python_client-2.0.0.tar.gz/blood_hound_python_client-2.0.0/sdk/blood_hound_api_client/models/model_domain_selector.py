from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelDomainSelector")


@_attrs_define
class ModelDomainSelector:
    """
    Attributes:
        type (Union[Unset, str]):
        name (Union[Unset, str]):
        id (Union[Unset, str]):
        collected (Union[Unset, bool]):
    """

    type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    collected: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        name = self.name

        id = self.id

        collected = self.collected

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if id is not UNSET:
            field_dict["id"] = id
        if collected is not UNSET:
            field_dict["collected"] = collected

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        id = d.pop("id", UNSET)

        collected = d.pop("collected", UNSET)

        model_domain_selector = cls(
            type=type,
            name=name,
            id=id,
            collected=collected,
        )

        model_domain_selector.additional_properties = d
        return model_domain_selector

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
