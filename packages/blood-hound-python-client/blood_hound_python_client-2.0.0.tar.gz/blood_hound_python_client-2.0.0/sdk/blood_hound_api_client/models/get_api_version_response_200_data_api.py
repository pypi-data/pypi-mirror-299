from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiVersionResponse200DataAPI")


@_attrs_define
class GetApiVersionResponse200DataAPI:
    """
    Attributes:
        current_version (Union[Unset, str]):
        deprecated_version (Union[Unset, str]):
    """

    current_version: Union[Unset, str] = UNSET
    deprecated_version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        current_version = self.current_version

        deprecated_version = self.deprecated_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if current_version is not UNSET:
            field_dict["current_version"] = current_version
        if deprecated_version is not UNSET:
            field_dict["deprecated_version"] = deprecated_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        current_version = d.pop("current_version", UNSET)

        deprecated_version = d.pop("deprecated_version", UNSET)

        get_api_version_response_200_data_api = cls(
            current_version=current_version,
            deprecated_version=deprecated_version,
        )

        get_api_version_response_200_data_api.additional_properties = d
        return get_api_version_response_200_data_api

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
