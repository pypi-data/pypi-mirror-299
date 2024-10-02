from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiRequestsUserSetSecret")


@_attrs_define
class ApiRequestsUserSetSecret:
    """
    Attributes:
        secret (Union[Unset, str]):
        needs_password_reset (Union[Unset, bool]):
    """

    secret: Union[Unset, str] = UNSET
    needs_password_reset: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        secret = self.secret

        needs_password_reset = self.needs_password_reset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if secret is not UNSET:
            field_dict["secret"] = secret
        if needs_password_reset is not UNSET:
            field_dict["needs_password_reset"] = needs_password_reset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        secret = d.pop("secret", UNSET)

        needs_password_reset = d.pop("needs_password_reset", UNSET)

        api_requests_user_set_secret = cls(
            secret=secret,
            needs_password_reset=needs_password_reset,
        )

        api_requests_user_set_secret.additional_properties = d
        return api_requests_user_set_secret

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
