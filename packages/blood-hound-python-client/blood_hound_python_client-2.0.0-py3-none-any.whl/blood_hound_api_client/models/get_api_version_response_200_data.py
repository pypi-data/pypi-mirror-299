from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_api_version_response_200_data_api import GetApiVersionResponse200DataAPI


T = TypeVar("T", bound="GetApiVersionResponse200Data")


@_attrs_define
class GetApiVersionResponse200Data:
    """
    Attributes:
        api (Union[Unset, GetApiVersionResponse200DataAPI]):
        server_version (Union[Unset, str]):
    """

    api: Union[Unset, "GetApiVersionResponse200DataAPI"] = UNSET
    server_version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        api: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.api, Unset):
            api = self.api.to_dict()

        server_version = self.server_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api is not UNSET:
            field_dict["API"] = api
        if server_version is not UNSET:
            field_dict["server_version"] = server_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_api_version_response_200_data_api import GetApiVersionResponse200DataAPI

        d = src_dict.copy()
        _api = d.pop("API", UNSET)
        api: Union[Unset, GetApiVersionResponse200DataAPI]
        if isinstance(_api, Unset):
            api = UNSET
        else:
            api = GetApiVersionResponse200DataAPI.from_dict(_api)

        server_version = d.pop("server_version", UNSET)

        get_api_version_response_200_data = cls(
            api=api,
            server_version=server_version,
        )

        get_api_version_response_200_data.additional_properties = d
        return get_api_version_response_200_data

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
