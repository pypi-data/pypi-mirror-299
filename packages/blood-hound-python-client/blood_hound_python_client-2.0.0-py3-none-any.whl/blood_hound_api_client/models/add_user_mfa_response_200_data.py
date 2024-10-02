from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddUserMfaResponse200Data")


@_attrs_define
class AddUserMfaResponse200Data:
    """
    Attributes:
        qr_code (Union[Unset, str]):
        totp_secret (Union[Unset, str]):
    """

    qr_code: Union[Unset, str] = UNSET
    totp_secret: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        qr_code = self.qr_code

        totp_secret = self.totp_secret

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if qr_code is not UNSET:
            field_dict["qr_code"] = qr_code
        if totp_secret is not UNSET:
            field_dict["totp_secret"] = totp_secret

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        qr_code = d.pop("qr_code", UNSET)

        totp_secret = d.pop("totp_secret", UNSET)

        add_user_mfa_response_200_data = cls(
            qr_code=qr_code,
            totp_secret=totp_secret,
        )

        add_user_mfa_response_200_data.additional_properties = d
        return add_user_mfa_response_200_data

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
