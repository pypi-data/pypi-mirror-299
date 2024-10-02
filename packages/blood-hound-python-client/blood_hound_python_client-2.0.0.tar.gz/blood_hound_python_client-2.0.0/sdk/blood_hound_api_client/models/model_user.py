import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_auth_secret import ModelAuthSecret
    from ..models.model_role import ModelRole
    from ..models.null_int_32 import NullInt32
    from ..models.null_string import NullString
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelUser")


@_attrs_define
class ModelUser:
    """
    Attributes:
        id (Union[Unset, str]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        saml_provider_id (Union[Unset, NullInt32]):
        auth_secret (Union[Unset, ModelAuthSecret]):
        roles (Union[Unset, List['ModelRole']]):
        first_name (Union[Unset, NullString]):
        last_name (Union[Unset, NullString]):
        email_address (Union[Unset, NullString]):
        principal_name (Union[Unset, str]):
        last_login (Union[Unset, datetime.datetime]):
        is_disabled (Union[Unset, bool]):
        eula_accepted (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    saml_provider_id: Union[Unset, "NullInt32"] = UNSET
    auth_secret: Union[Unset, "ModelAuthSecret"] = UNSET
    roles: Union[Unset, List["ModelRole"]] = UNSET
    first_name: Union[Unset, "NullString"] = UNSET
    last_name: Union[Unset, "NullString"] = UNSET
    email_address: Union[Unset, "NullString"] = UNSET
    principal_name: Union[Unset, str] = UNSET
    last_login: Union[Unset, datetime.datetime] = UNSET
    is_disabled: Union[Unset, bool] = UNSET
    eula_accepted: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        deleted_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.to_dict()

        saml_provider_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.saml_provider_id, Unset):
            saml_provider_id = self.saml_provider_id.to_dict()

        auth_secret: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auth_secret, Unset):
            auth_secret = self.auth_secret.to_dict()

        roles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.to_dict()
                roles.append(roles_item)

        first_name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.first_name, Unset):
            first_name = self.first_name.to_dict()

        last_name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_name, Unset):
            last_name = self.last_name.to_dict()

        email_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.email_address, Unset):
            email_address = self.email_address.to_dict()

        principal_name = self.principal_name

        last_login: Union[Unset, str] = UNSET
        if not isinstance(self.last_login, Unset):
            last_login = self.last_login.isoformat()

        is_disabled = self.is_disabled

        eula_accepted = self.eula_accepted

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if saml_provider_id is not UNSET:
            field_dict["saml_provider_id"] = saml_provider_id
        if auth_secret is not UNSET:
            field_dict["AuthSecret"] = auth_secret
        if roles is not UNSET:
            field_dict["roles"] = roles
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if principal_name is not UNSET:
            field_dict["principal_name"] = principal_name
        if last_login is not UNSET:
            field_dict["last_login"] = last_login
        if is_disabled is not UNSET:
            field_dict["is_disabled"] = is_disabled
        if eula_accepted is not UNSET:
            field_dict["eula_accepted"] = eula_accepted

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_auth_secret import ModelAuthSecret
        from ..models.model_role import ModelRole
        from ..models.null_int_32 import NullInt32
        from ..models.null_string import NullString
        from ..models.null_time import NullTime

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _deleted_at = d.pop("deleted_at", UNSET)
        deleted_at: Union[Unset, NullTime]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = NullTime.from_dict(_deleted_at)

        _saml_provider_id = d.pop("saml_provider_id", UNSET)
        saml_provider_id: Union[Unset, NullInt32]
        if isinstance(_saml_provider_id, Unset):
            saml_provider_id = UNSET
        else:
            saml_provider_id = NullInt32.from_dict(_saml_provider_id)

        _auth_secret = d.pop("AuthSecret", UNSET)
        auth_secret: Union[Unset, ModelAuthSecret]
        if isinstance(_auth_secret, Unset):
            auth_secret = UNSET
        else:
            auth_secret = ModelAuthSecret.from_dict(_auth_secret)

        roles = []
        _roles = d.pop("roles", UNSET)
        for roles_item_data in _roles or []:
            roles_item = ModelRole.from_dict(roles_item_data)

            roles.append(roles_item)

        _first_name = d.pop("first_name", UNSET)
        first_name: Union[Unset, NullString]
        if isinstance(_first_name, Unset):
            first_name = UNSET
        else:
            first_name = NullString.from_dict(_first_name)

        _last_name = d.pop("last_name", UNSET)
        last_name: Union[Unset, NullString]
        if isinstance(_last_name, Unset):
            last_name = UNSET
        else:
            last_name = NullString.from_dict(_last_name)

        _email_address = d.pop("email_address", UNSET)
        email_address: Union[Unset, NullString]
        if isinstance(_email_address, Unset):
            email_address = UNSET
        else:
            email_address = NullString.from_dict(_email_address)

        principal_name = d.pop("principal_name", UNSET)

        _last_login = d.pop("last_login", UNSET)
        last_login: Union[Unset, datetime.datetime]
        if isinstance(_last_login, Unset):
            last_login = UNSET
        else:
            last_login = isoparse(_last_login)

        is_disabled = d.pop("is_disabled", UNSET)

        eula_accepted = d.pop("eula_accepted", UNSET)

        model_user = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            saml_provider_id=saml_provider_id,
            auth_secret=auth_secret,
            roles=roles,
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            principal_name=principal_name,
            last_login=last_login,
            is_disabled=is_disabled,
            eula_accepted=eula_accepted,
        )

        model_user.additional_properties = d
        return model_user

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
