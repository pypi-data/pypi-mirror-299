from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUserBody")


@_attrs_define
class CreateUserBody:
    """
    Attributes:
        first_name (Union[Unset, str]):
        last_name (Union[Unset, str]):
        email_address (Union[Unset, str]):
        principal (Union[Unset, str]):
        roles (Union[Unset, List[int]]):
        saml_provider_id (Union[Unset, str]):
        is_disabled (Union[Unset, bool]):
        secret (Union[Unset, str]):
        needs_password_reset (Union[Unset, bool]):
    """

    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    principal: Union[Unset, str] = UNSET
    roles: Union[Unset, List[int]] = UNSET
    saml_provider_id: Union[Unset, str] = UNSET
    is_disabled: Union[Unset, bool] = UNSET
    secret: Union[Unset, str] = UNSET
    needs_password_reset: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name

        last_name = self.last_name

        email_address = self.email_address

        principal = self.principal

        roles: Union[Unset, List[int]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        saml_provider_id = self.saml_provider_id

        is_disabled = self.is_disabled

        secret = self.secret

        needs_password_reset = self.needs_password_reset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if principal is not UNSET:
            field_dict["principal"] = principal
        if roles is not UNSET:
            field_dict["roles"] = roles
        if saml_provider_id is not UNSET:
            field_dict["saml_provider_id"] = saml_provider_id
        if is_disabled is not UNSET:
            field_dict["is_disabled"] = is_disabled
        if secret is not UNSET:
            field_dict["secret"] = secret
        if needs_password_reset is not UNSET:
            field_dict["needs_password_reset"] = needs_password_reset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        email_address = d.pop("email_address", UNSET)

        principal = d.pop("principal", UNSET)

        roles = cast(List[int], d.pop("roles", UNSET))

        saml_provider_id = d.pop("saml_provider_id", UNSET)

        is_disabled = d.pop("is_disabled", UNSET)

        secret = d.pop("secret", UNSET)

        needs_password_reset = d.pop("needs_password_reset", UNSET)

        create_user_body = cls(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            principal=principal,
            roles=roles,
            saml_provider_id=saml_provider_id,
            is_disabled=is_disabled,
            secret=secret,
            needs_password_reset=needs_password_reset,
        )

        create_user_body.additional_properties = d
        return create_user_body

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
