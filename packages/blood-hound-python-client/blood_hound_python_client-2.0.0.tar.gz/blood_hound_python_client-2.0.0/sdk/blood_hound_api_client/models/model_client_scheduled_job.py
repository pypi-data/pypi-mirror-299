import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.enum_job_status import EnumJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_domain_collection_result import ModelDomainCollectionResult
    from ..models.null_int_32 import NullInt32
    from ..models.null_string import NullString
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelClientScheduledJob")


@_attrs_define
class ModelClientScheduledJob:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        client_id (Union[Unset, str]):
        client_name (Union[Unset, str]):
        event_id (Union[Unset, NullInt32]):
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
        log_path (Union[Unset, NullString]):
        session_collection (Union[Unset, bool]):
        local_group_collection (Union[Unset, bool]):
        ad_structure_collection (Union[Unset, bool]):
        cert_services_collection (Union[Unset, bool]):
        ca_registry_collection (Union[Unset, bool]):
        dc_registry_collection (Union[Unset, bool]):
        all_trusted_domains (Union[Unset, bool]):
        domain_controller (Union[Unset, NullString]):
        event_title (Union[Unset, str]):
        last_ingest (Union[Unset, datetime.datetime]):
        ous (Union[Unset, List[str]]):
        domains (Union[Unset, List[str]]):
        domain_results (Union[Unset, List['ModelDomainCollectionResult']]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_name: Union[Unset, str] = UNSET
    event_id: Union[Unset, "NullInt32"] = UNSET
    status: Union[Unset, EnumJobStatus] = UNSET
    status_message: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    log_path: Union[Unset, "NullString"] = UNSET
    session_collection: Union[Unset, bool] = UNSET
    local_group_collection: Union[Unset, bool] = UNSET
    ad_structure_collection: Union[Unset, bool] = UNSET
    cert_services_collection: Union[Unset, bool] = UNSET
    ca_registry_collection: Union[Unset, bool] = UNSET
    dc_registry_collection: Union[Unset, bool] = UNSET
    all_trusted_domains: Union[Unset, bool] = UNSET
    domain_controller: Union[Unset, "NullString"] = UNSET
    event_title: Union[Unset, str] = UNSET
    last_ingest: Union[Unset, datetime.datetime] = UNSET
    ous: Union[Unset, List[str]] = UNSET
    domains: Union[Unset, List[str]] = UNSET
    domain_results: Union[Unset, List["ModelDomainCollectionResult"]] = UNSET
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

        client_id = self.client_id

        client_name = self.client_name

        event_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.event_id, Unset):
            event_id = self.event_id.to_dict()

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

        log_path: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.log_path, Unset):
            log_path = self.log_path.to_dict()

        session_collection = self.session_collection

        local_group_collection = self.local_group_collection

        ad_structure_collection = self.ad_structure_collection

        cert_services_collection = self.cert_services_collection

        ca_registry_collection = self.ca_registry_collection

        dc_registry_collection = self.dc_registry_collection

        all_trusted_domains = self.all_trusted_domains

        domain_controller: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.domain_controller, Unset):
            domain_controller = self.domain_controller.to_dict()

        event_title = self.event_title

        last_ingest: Union[Unset, str] = UNSET
        if not isinstance(self.last_ingest, Unset):
            last_ingest = self.last_ingest.isoformat()

        ous: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ous, Unset):
            ous = self.ous

        domains: Union[Unset, List[str]] = UNSET
        if not isinstance(self.domains, Unset):
            domains = self.domains

        domain_results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.domain_results, Unset):
            domain_results = []
            for domain_results_item_data in self.domain_results:
                domain_results_item = domain_results_item_data.to_dict()
                domain_results.append(domain_results_item)

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
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_name is not UNSET:
            field_dict["client_name"] = client_name
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if log_path is not UNSET:
            field_dict["log_path"] = log_path
        if session_collection is not UNSET:
            field_dict["session_collection"] = session_collection
        if local_group_collection is not UNSET:
            field_dict["local_group_collection"] = local_group_collection
        if ad_structure_collection is not UNSET:
            field_dict["ad_structure_collection"] = ad_structure_collection
        if cert_services_collection is not UNSET:
            field_dict["cert_services_collection"] = cert_services_collection
        if ca_registry_collection is not UNSET:
            field_dict["ca_registry_collection"] = ca_registry_collection
        if dc_registry_collection is not UNSET:
            field_dict["dc_registry_collection"] = dc_registry_collection
        if all_trusted_domains is not UNSET:
            field_dict["all_trusted_domains"] = all_trusted_domains
        if domain_controller is not UNSET:
            field_dict["domain_controller"] = domain_controller
        if event_title is not UNSET:
            field_dict["event_title"] = event_title
        if last_ingest is not UNSET:
            field_dict["last_ingest"] = last_ingest
        if ous is not UNSET:
            field_dict["ous"] = ous
        if domains is not UNSET:
            field_dict["domains"] = domains
        if domain_results is not UNSET:
            field_dict["domain_results"] = domain_results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_domain_collection_result import ModelDomainCollectionResult
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

        client_id = d.pop("client_id", UNSET)

        client_name = d.pop("client_name", UNSET)

        _event_id = d.pop("event_id", UNSET)
        event_id: Union[Unset, NullInt32]
        if isinstance(_event_id, Unset):
            event_id = UNSET
        else:
            event_id = NullInt32.from_dict(_event_id)

        _status = d.pop("status", UNSET)
        status: Union[Unset, EnumJobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = EnumJobStatus(_status)

        status_message = d.pop("statusMessage", UNSET)

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

        _log_path = d.pop("log_path", UNSET)
        log_path: Union[Unset, NullString]
        if isinstance(_log_path, Unset):
            log_path = UNSET
        else:
            log_path = NullString.from_dict(_log_path)

        session_collection = d.pop("session_collection", UNSET)

        local_group_collection = d.pop("local_group_collection", UNSET)

        ad_structure_collection = d.pop("ad_structure_collection", UNSET)

        cert_services_collection = d.pop("cert_services_collection", UNSET)

        ca_registry_collection = d.pop("ca_registry_collection", UNSET)

        dc_registry_collection = d.pop("dc_registry_collection", UNSET)

        all_trusted_domains = d.pop("all_trusted_domains", UNSET)

        _domain_controller = d.pop("domain_controller", UNSET)
        domain_controller: Union[Unset, NullString]
        if isinstance(_domain_controller, Unset):
            domain_controller = UNSET
        else:
            domain_controller = NullString.from_dict(_domain_controller)

        event_title = d.pop("event_title", UNSET)

        _last_ingest = d.pop("last_ingest", UNSET)
        last_ingest: Union[Unset, datetime.datetime]
        if isinstance(_last_ingest, Unset):
            last_ingest = UNSET
        else:
            last_ingest = isoparse(_last_ingest)

        ous = cast(List[str], d.pop("ous", UNSET))

        domains = cast(List[str], d.pop("domains", UNSET))

        domain_results = []
        _domain_results = d.pop("domain_results", UNSET)
        for domain_results_item_data in _domain_results or []:
            domain_results_item = ModelDomainCollectionResult.from_dict(domain_results_item_data)

            domain_results.append(domain_results_item)

        model_client_scheduled_job = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            client_id=client_id,
            client_name=client_name,
            event_id=event_id,
            status=status,
            status_message=status_message,
            start_time=start_time,
            end_time=end_time,
            log_path=log_path,
            session_collection=session_collection,
            local_group_collection=local_group_collection,
            ad_structure_collection=ad_structure_collection,
            cert_services_collection=cert_services_collection,
            ca_registry_collection=ca_registry_collection,
            dc_registry_collection=dc_registry_collection,
            all_trusted_domains=all_trusted_domains,
            domain_controller=domain_controller,
            event_title=event_title,
            last_ingest=last_ingest,
            ous=ous,
            domains=domains,
            domain_results=domain_results,
        )

        model_client_scheduled_job.additional_properties = d
        return model_client_scheduled_job

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
