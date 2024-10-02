from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_saml_provider import ModelSamlProvider


T = TypeVar("T", bound="ListSamlProvidersResponse200Data")


@_attrs_define
class ListSamlProvidersResponse200Data:
    """
    Attributes:
        saml_providers (Union[Unset, List['ModelSamlProvider']]):
    """

    saml_providers: Union[Unset, List["ModelSamlProvider"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        saml_providers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.saml_providers, Unset):
            saml_providers = []
            for saml_providers_item_data in self.saml_providers:
                saml_providers_item = saml_providers_item_data.to_dict()
                saml_providers.append(saml_providers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if saml_providers is not UNSET:
            field_dict["saml_providers"] = saml_providers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_saml_provider import ModelSamlProvider

        d = src_dict.copy()
        saml_providers = []
        _saml_providers = d.pop("saml_providers", UNSET)
        for saml_providers_item_data in _saml_providers or []:
            saml_providers_item = ModelSamlProvider.from_dict(saml_providers_item_data)

            saml_providers.append(saml_providers_item)

        list_saml_providers_response_200_data = cls(
            saml_providers=saml_providers,
        )

        list_saml_providers_response_200_data.additional_properties = d
        return list_saml_providers_response_200_data

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
