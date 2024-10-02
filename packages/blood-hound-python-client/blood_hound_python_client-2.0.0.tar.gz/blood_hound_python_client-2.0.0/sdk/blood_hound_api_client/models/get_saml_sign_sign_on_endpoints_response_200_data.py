from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_saml_sign_on_endpoint import ModelSamlSignOnEndpoint


T = TypeVar("T", bound="GetSamlSignSignOnEndpointsResponse200Data")


@_attrs_define
class GetSamlSignSignOnEndpointsResponse200Data:
    """
    Attributes:
        endpoints (Union[Unset, List['ModelSamlSignOnEndpoint']]):
    """

    endpoints: Union[Unset, List["ModelSamlSignOnEndpoint"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        endpoints: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.endpoints, Unset):
            endpoints = []
            for endpoints_item_data in self.endpoints:
                endpoints_item = endpoints_item_data.to_dict()
                endpoints.append(endpoints_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if endpoints is not UNSET:
            field_dict["endpoints"] = endpoints

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_saml_sign_on_endpoint import ModelSamlSignOnEndpoint

        d = src_dict.copy()
        endpoints = []
        _endpoints = d.pop("endpoints", UNSET)
        for endpoints_item_data in _endpoints or []:
            endpoints_item = ModelSamlSignOnEndpoint.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        get_saml_sign_sign_on_endpoints_response_200_data = cls(
            endpoints=endpoints,
        )

        get_saml_sign_sign_on_endpoints_response_200_data.additional_properties = d
        return get_saml_sign_sign_on_endpoints_response_200_data

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
