import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.enum_audit_log_status import EnumAuditLogStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_audit_log_fields import ModelAuditLogFields


T = TypeVar("T", bound="ModelAuditLog")


@_attrs_define
class ModelAuditLog:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        actor_id (Union[Unset, str]):
        actor_name (Union[Unset, str]):
        actor_email (Union[Unset, str]):
        action (Union[Unset, str]):
        fields (Union[Unset, ModelAuditLogFields]):
        request_id (Union[Unset, str]):
        source_ip_address (Union[Unset, str]):
        commit_id (Union[Unset, str]):
        status (Union[Unset, EnumAuditLogStatus]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    actor_id: Union[Unset, str] = UNSET
    actor_name: Union[Unset, str] = UNSET
    actor_email: Union[Unset, str] = UNSET
    action: Union[Unset, str] = UNSET
    fields: Union[Unset, "ModelAuditLogFields"] = UNSET
    request_id: Union[Unset, str] = UNSET
    source_ip_address: Union[Unset, str] = UNSET
    commit_id: Union[Unset, str] = UNSET
    status: Union[Unset, EnumAuditLogStatus] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        actor_id = self.actor_id

        actor_name = self.actor_name

        actor_email = self.actor_email

        action = self.action

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        request_id = self.request_id

        source_ip_address = self.source_ip_address

        commit_id = self.commit_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if actor_id is not UNSET:
            field_dict["actor_id"] = actor_id
        if actor_name is not UNSET:
            field_dict["actor_name"] = actor_name
        if actor_email is not UNSET:
            field_dict["actor_email"] = actor_email
        if action is not UNSET:
            field_dict["action"] = action
        if fields is not UNSET:
            field_dict["fields"] = fields
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if source_ip_address is not UNSET:
            field_dict["source_ip_address"] = source_ip_address
        if commit_id is not UNSET:
            field_dict["commit_id"] = commit_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_audit_log_fields import ModelAuditLogFields

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        actor_id = d.pop("actor_id", UNSET)

        actor_name = d.pop("actor_name", UNSET)

        actor_email = d.pop("actor_email", UNSET)

        action = d.pop("action", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, ModelAuditLogFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = ModelAuditLogFields.from_dict(_fields)

        request_id = d.pop("request_id", UNSET)

        source_ip_address = d.pop("source_ip_address", UNSET)

        commit_id = d.pop("commit_id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, EnumAuditLogStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = EnumAuditLogStatus(_status)

        model_audit_log = cls(
            id=id,
            created_at=created_at,
            actor_id=actor_id,
            actor_name=actor_name,
            actor_email=actor_email,
            action=action,
            fields=fields,
            request_id=request_id,
            source_ip_address=source_ip_address,
            commit_id=commit_id,
            status=status,
        )

        model_audit_log.additional_properties = d
        return model_audit_log

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
