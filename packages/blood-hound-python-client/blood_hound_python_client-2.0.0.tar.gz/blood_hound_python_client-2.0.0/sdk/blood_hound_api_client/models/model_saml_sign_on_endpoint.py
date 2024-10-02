from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelSamlSignOnEndpoint")


@_attrs_define
class ModelSamlSignOnEndpoint:
    """
    Attributes:
        name (Union[Unset, str]):
        idp_url (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    idp_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        idp_url = self.idp_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if idp_url is not UNSET:
            field_dict["idp_url"] = idp_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        idp_url = d.pop("idp_url", UNSET)

        model_saml_sign_on_endpoint = cls(
            name=name,
            idp_url=idp_url,
        )

        model_saml_sign_on_endpoint.additional_properties = d
        return model_saml_sign_on_endpoint

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
