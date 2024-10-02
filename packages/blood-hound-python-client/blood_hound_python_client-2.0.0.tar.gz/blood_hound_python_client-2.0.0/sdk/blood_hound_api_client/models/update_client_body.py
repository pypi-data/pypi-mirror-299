from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateClientBody")


@_attrs_define
class UpdateClientBody:
    """
    Attributes:
        name (Union[Unset, str]):
        domain_controller (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    domain_controller: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        domain_controller = self.domain_controller

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if domain_controller is not UNSET:
            field_dict["domain_controller"] = domain_controller

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        domain_controller = d.pop("domain_controller", UNSET)

        update_client_body = cls(
            name=name,
            domain_controller=domain_controller,
        )

        update_client_body.additional_properties = d
        return update_client_body

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
