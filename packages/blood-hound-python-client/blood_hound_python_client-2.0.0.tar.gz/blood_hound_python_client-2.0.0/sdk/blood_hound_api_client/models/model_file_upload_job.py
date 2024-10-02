import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.enum_job_status import EnumJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelFileUploadJob")


@_attrs_define
class ModelFileUploadJob:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        user_id (Union[Unset, str]):
        user_email_address (Union[Unset, str]):
        status (Union[Unset, EnumJobStatus]): This enum describes the current status of a Job. Values are:
            - `-1` Invalid
            - `0` Ready
            - `1` Running
            - `2` Complete
            - `3` Canceled
            - `4` Timed Out
            - `5` Failed
            - `6` Ingesting
            - `7` Analyzing
            - `8` Partially Complete
        status_message (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
        last_ingest (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    user_id: Union[Unset, str] = UNSET
    user_email_address: Union[Unset, str] = UNSET
    status: Union[Unset, EnumJobStatus] = UNSET
    status_message: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    last_ingest: Union[Unset, datetime.datetime] = UNSET
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

        user_id = self.user_id

        user_email_address = self.user_email_address

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_message = self.status_message

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        last_ingest: Union[Unset, str] = UNSET
        if not isinstance(self.last_ingest, Unset):
            last_ingest = self.last_ingest.isoformat()

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
        if user_email_address is not UNSET:
            field_dict["user_email_address"] = user_email_address
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["status_message"] = status_message
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if last_ingest is not UNSET:
            field_dict["last_ingest"] = last_ingest

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
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

        user_id = d.pop("user_id", UNSET)

        user_email_address = d.pop("user_email_address", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, EnumJobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = EnumJobStatus(_status)

        status_message = d.pop("status_message", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        _last_ingest = d.pop("last_ingest", UNSET)
        last_ingest: Union[Unset, datetime.datetime]
        if isinstance(_last_ingest, Unset):
            last_ingest = UNSET
        else:
            last_ingest = isoparse(_last_ingest)

        model_file_upload_job = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            user_id=user_id,
            user_email_address=user_email_address,
            status=status,
            status_message=status_message,
            start_time=start_time,
            end_time=end_time,
            last_ingest=last_ingest,
        )

        model_file_upload_job.additional_properties = d
        return model_file_upload_job

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
