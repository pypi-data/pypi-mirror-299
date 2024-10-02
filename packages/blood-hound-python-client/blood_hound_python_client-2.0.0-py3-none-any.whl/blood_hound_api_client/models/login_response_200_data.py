from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LoginResponse200Data")


@_attrs_define
class LoginResponse200Data:
    """
    Attributes:
        user_id (Union[Unset, str]):
        auth_expired (Union[Unset, bool]):
        session_token (Union[Unset, str]):
    """

    user_id: Union[Unset, str] = UNSET
    auth_expired: Union[Unset, bool] = UNSET
    session_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id

        auth_expired = self.auth_expired

        session_token = self.session_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if auth_expired is not UNSET:
            field_dict["auth_expired"] = auth_expired
        if session_token is not UNSET:
            field_dict["session_token"] = session_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id", UNSET)

        auth_expired = d.pop("auth_expired", UNSET)

        session_token = d.pop("session_token", UNSET)

        login_response_200_data = cls(
            user_id=user_id,
            auth_expired=auth_expired,
            session_token=session_token,
        )

        login_response_200_data.additional_properties = d
        return login_response_200_data

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
