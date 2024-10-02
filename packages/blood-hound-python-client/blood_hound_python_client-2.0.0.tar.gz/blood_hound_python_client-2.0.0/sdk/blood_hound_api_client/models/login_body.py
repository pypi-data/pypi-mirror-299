from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.login_body_login_method import LoginBodyLoginMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="LoginBody")


@_attrs_define
class LoginBody:
    """
    Attributes:
        login_method (LoginBodyLoginMethod): The type of login. Currently only `secret` is supported.
        username (str):
        secret (Union[Unset, str]): The password for the user. This field can be used instead of `otp`.
        otp (Union[Unset, str]): The One Time Password for a single login. This field can be used instead of `secret`
    """

    login_method: LoginBodyLoginMethod
    username: str
    secret: Union[Unset, str] = UNSET
    otp: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        login_method = self.login_method.value

        username = self.username

        secret = self.secret

        otp = self.otp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "login_method": login_method,
                "username": username,
            }
        )
        if secret is not UNSET:
            field_dict["secret"] = secret
        if otp is not UNSET:
            field_dict["otp"] = otp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        login_method = LoginBodyLoginMethod(d.pop("login_method"))

        username = d.pop("username")

        secret = d.pop("secret", UNSET)

        otp = d.pop("otp", UNSET)

        login_body = cls(
            login_method=login_method,
            username=username,
            secret=secret,
            otp=otp,
        )

        login_body.additional_properties = d
        return login_body

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
