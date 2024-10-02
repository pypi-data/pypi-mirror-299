from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateClientInfoBody")


@_attrs_define
class UpdateClientInfoBody:
    """
    Attributes:
        address (Union[Unset, str]):
        hostname (Union[Unset, str]):
        username (Union[Unset, str]):
        version (Union[Unset, str]):
        usersid (Union[Unset, str]):
    """

    address: Union[Unset, str] = UNSET
    hostname: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    usersid: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address

        hostname = self.hostname

        username = self.username

        version = self.version

        usersid = self.usersid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address is not UNSET:
            field_dict["address"] = address
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if username is not UNSET:
            field_dict["username"] = username
        if version is not UNSET:
            field_dict["version"] = version
        if usersid is not UNSET:
            field_dict["usersid"] = usersid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address", UNSET)

        hostname = d.pop("hostname", UNSET)

        username = d.pop("username", UNSET)

        version = d.pop("version", UNSET)

        usersid = d.pop("usersid", UNSET)

        update_client_info_body = cls(
            address=address,
            hostname=hostname,
            username=username,
            version=version,
            usersid=usersid,
        )

        update_client_info_body.additional_properties = d
        return update_client_info_body

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
