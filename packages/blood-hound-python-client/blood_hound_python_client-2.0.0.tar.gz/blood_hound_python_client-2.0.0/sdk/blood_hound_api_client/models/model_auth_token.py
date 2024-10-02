import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_string import NullString
    from ..models.null_time import NullTime
    from ..models.null_uuid import NullUuid


T = TypeVar("T", bound="ModelAuthToken")


@_attrs_define
class ModelAuthToken:
    """
    Attributes:
        id (Union[Unset, str]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        user_id (Union[Unset, NullUuid]):
        name (Union[Unset, NullString]):
        key (Union[Unset, str]):
        hmac_method (Union[Unset, str]):
        last_access (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    user_id: Union[Unset, "NullUuid"] = UNSET
    name: Union[Unset, "NullString"] = UNSET
    key: Union[Unset, str] = UNSET
    hmac_method: Union[Unset, str] = UNSET
    last_access: Union[Unset, datetime.datetime] = UNSET
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

        user_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_id, Unset):
            user_id = self.user_id.to_dict()

        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        key = self.key

        hmac_method = self.hmac_method

        last_access: Union[Unset, str] = UNSET
        if not isinstance(self.last_access, Unset):
            last_access = self.last_access.isoformat()

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
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if name is not UNSET:
            field_dict["name"] = name
        if key is not UNSET:
            field_dict["key"] = key
        if hmac_method is not UNSET:
            field_dict["hmac_method"] = hmac_method
        if last_access is not UNSET:
            field_dict["last_access"] = last_access

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.null_string import NullString
        from ..models.null_time import NullTime
        from ..models.null_uuid import NullUuid

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

        _user_id = d.pop("user_id", UNSET)
        user_id: Union[Unset, NullUuid]
        if isinstance(_user_id, Unset):
            user_id = UNSET
        else:
            user_id = NullUuid.from_dict(_user_id)

        _name = d.pop("name", UNSET)
        name: Union[Unset, NullString]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = NullString.from_dict(_name)

        key = d.pop("key", UNSET)

        hmac_method = d.pop("hmac_method", UNSET)

        _last_access = d.pop("last_access", UNSET)
        last_access: Union[Unset, datetime.datetime]
        if isinstance(_last_access, Unset):
            last_access = UNSET
        else:
            last_access = isoparse(_last_access)

        model_auth_token = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            user_id=user_id,
            name=name,
            key=key,
            hmac_method=hmac_method,
            last_access=last_access,
        )

        model_auth_token.additional_properties = d
        return model_auth_token

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
