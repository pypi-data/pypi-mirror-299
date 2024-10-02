import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.enum_client_type import EnumClientType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_auth_token import ModelAuthToken
    from ..models.model_client_schedule_display import ModelClientScheduleDisplay
    from ..models.model_client_scheduled_job_display import ModelClientScheduledJobDisplay
    from ..models.null_int_64 import NullInt64
    from ..models.null_string import NullString


T = TypeVar("T", bound="ModelClientDisplay")


@_attrs_define
class ModelClientDisplay:
    """
    Attributes:
        id (Union[Unset, str]): This is the unique identifier for this object.
        name (Union[Unset, str]):
        ip_address (Union[Unset, str]):
        hostname (Union[Unset, str]):
        configured_user (Union[Unset, str]):
        last_checkin (Union[Unset, datetime.datetime]):
        events (Union[Unset, List['ModelClientScheduleDisplay']]):
        token (Union[Unset, ModelAuthToken]):
        current_job_id (Union[Unset, NullInt64]):
        current_task_id (Union[Unset, NullInt64]):
        current_job (Union[Unset, ModelClientScheduledJobDisplay]):
        current_task (Union[Unset, ModelClientScheduledJobDisplay]):
        completed_job_count (Union[Unset, int]):
        completed_task_count (Union[Unset, int]):
        domain_controller (Union[Unset, NullString]):
        version (Union[Unset, str]):
        user_sid (Union[Unset, NullString]):
        type (Union[Unset, EnumClientType]): This enum describes the collector client type.
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    ip_address: Union[Unset, str] = UNSET
    hostname: Union[Unset, str] = UNSET
    configured_user: Union[Unset, str] = UNSET
    last_checkin: Union[Unset, datetime.datetime] = UNSET
    events: Union[Unset, List["ModelClientScheduleDisplay"]] = UNSET
    token: Union[Unset, "ModelAuthToken"] = UNSET
    current_job_id: Union[Unset, "NullInt64"] = UNSET
    current_task_id: Union[Unset, "NullInt64"] = UNSET
    current_job: Union[Unset, "ModelClientScheduledJobDisplay"] = UNSET
    current_task: Union[Unset, "ModelClientScheduledJobDisplay"] = UNSET
    completed_job_count: Union[Unset, int] = UNSET
    completed_task_count: Union[Unset, int] = UNSET
    domain_controller: Union[Unset, "NullString"] = UNSET
    version: Union[Unset, str] = UNSET
    user_sid: Union[Unset, "NullString"] = UNSET
    type: Union[Unset, EnumClientType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        ip_address = self.ip_address

        hostname = self.hostname

        configured_user = self.configured_user

        last_checkin: Union[Unset, str] = UNSET
        if not isinstance(self.last_checkin, Unset):
            last_checkin = self.last_checkin.isoformat()

        events: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        token: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.token, Unset):
            token = self.token.to_dict()

        current_job_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_job_id, Unset):
            current_job_id = self.current_job_id.to_dict()

        current_task_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_task_id, Unset):
            current_task_id = self.current_task_id.to_dict()

        current_job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_job, Unset):
            current_job = self.current_job.to_dict()

        current_task: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_task, Unset):
            current_task = self.current_task.to_dict()

        completed_job_count = self.completed_job_count

        completed_task_count = self.completed_task_count

        domain_controller: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.domain_controller, Unset):
            domain_controller = self.domain_controller.to_dict()

        version = self.version

        user_sid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_sid, Unset):
            user_sid = self.user_sid.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if configured_user is not UNSET:
            field_dict["configured_user"] = configured_user
        if last_checkin is not UNSET:
            field_dict["last_checkin"] = last_checkin
        if events is not UNSET:
            field_dict["events"] = events
        if token is not UNSET:
            field_dict["token"] = token
        if current_job_id is not UNSET:
            field_dict["current_job_id"] = current_job_id
        if current_task_id is not UNSET:
            field_dict["current_task_id"] = current_task_id
        if current_job is not UNSET:
            field_dict["current_job"] = current_job
        if current_task is not UNSET:
            field_dict["current_task"] = current_task
        if completed_job_count is not UNSET:
            field_dict["completed_job_count"] = completed_job_count
        if completed_task_count is not UNSET:
            field_dict["completed_task_count"] = completed_task_count
        if domain_controller is not UNSET:
            field_dict["domain_controller"] = domain_controller
        if version is not UNSET:
            field_dict["version"] = version
        if user_sid is not UNSET:
            field_dict["user_sid"] = user_sid
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_auth_token import ModelAuthToken
        from ..models.model_client_schedule_display import ModelClientScheduleDisplay
        from ..models.model_client_scheduled_job_display import ModelClientScheduledJobDisplay
        from ..models.null_int_64 import NullInt64
        from ..models.null_string import NullString

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        ip_address = d.pop("ip_address", UNSET)

        hostname = d.pop("hostname", UNSET)

        configured_user = d.pop("configured_user", UNSET)

        _last_checkin = d.pop("last_checkin", UNSET)
        last_checkin: Union[Unset, datetime.datetime]
        if isinstance(_last_checkin, Unset):
            last_checkin = UNSET
        else:
            last_checkin = isoparse(_last_checkin)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = ModelClientScheduleDisplay.from_dict(events_item_data)

            events.append(events_item)

        _token = d.pop("token", UNSET)
        token: Union[Unset, ModelAuthToken]
        if isinstance(_token, Unset):
            token = UNSET
        else:
            token = ModelAuthToken.from_dict(_token)

        _current_job_id = d.pop("current_job_id", UNSET)
        current_job_id: Union[Unset, NullInt64]
        if isinstance(_current_job_id, Unset):
            current_job_id = UNSET
        else:
            current_job_id = NullInt64.from_dict(_current_job_id)

        _current_task_id = d.pop("current_task_id", UNSET)
        current_task_id: Union[Unset, NullInt64]
        if isinstance(_current_task_id, Unset):
            current_task_id = UNSET
        else:
            current_task_id = NullInt64.from_dict(_current_task_id)

        _current_job = d.pop("current_job", UNSET)
        current_job: Union[Unset, ModelClientScheduledJobDisplay]
        if isinstance(_current_job, Unset):
            current_job = UNSET
        else:
            current_job = ModelClientScheduledJobDisplay.from_dict(_current_job)

        _current_task = d.pop("current_task", UNSET)
        current_task: Union[Unset, ModelClientScheduledJobDisplay]
        if isinstance(_current_task, Unset):
            current_task = UNSET
        else:
            current_task = ModelClientScheduledJobDisplay.from_dict(_current_task)

        completed_job_count = d.pop("completed_job_count", UNSET)

        completed_task_count = d.pop("completed_task_count", UNSET)

        _domain_controller = d.pop("domain_controller", UNSET)
        domain_controller: Union[Unset, NullString]
        if isinstance(_domain_controller, Unset):
            domain_controller = UNSET
        else:
            domain_controller = NullString.from_dict(_domain_controller)

        version = d.pop("version", UNSET)

        _user_sid = d.pop("user_sid", UNSET)
        user_sid: Union[Unset, NullString]
        if isinstance(_user_sid, Unset):
            user_sid = UNSET
        else:
            user_sid = NullString.from_dict(_user_sid)

        _type = d.pop("type", UNSET)
        type: Union[Unset, EnumClientType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = EnumClientType(_type)

        model_client_display = cls(
            id=id,
            name=name,
            ip_address=ip_address,
            hostname=hostname,
            configured_user=configured_user,
            last_checkin=last_checkin,
            events=events,
            token=token,
            current_job_id=current_job_id,
            current_task_id=current_task_id,
            current_job=current_job,
            current_task=current_task,
            completed_job_count=completed_job_count,
            completed_task_count=completed_task_count,
            domain_controller=domain_controller,
            version=version,
            user_sid=user_sid,
            type=type,
        )

        model_client_display.additional_properties = d
        return model_client_display

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
