import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.enum_job_status import EnumJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_domain_collection_result import ModelDomainCollectionResult
    from ..models.model_domain_details import ModelDomainDetails
    from ..models.model_ou_details import ModelOuDetails
    from ..models.null_int_32 import NullInt32


T = TypeVar("T", bound="ModelClientScheduledJobDisplay")


@_attrs_define
class ModelClientScheduledJobDisplay:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        client_id (Union[Unset, str]):
        client_name (Union[Unset, str]):
        event_id (Union[Unset, NullInt32]):
        execution_time (Union[Unset, datetime.datetime]):
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
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
        session_collection (Union[Unset, bool]):
        local_group_collection (Union[Unset, bool]):
        ad_structure_collection (Union[Unset, bool]):
        cert_services_collection (Union[Unset, bool]):
        ca_registry_collection (Union[Unset, bool]):
        dc_registry_collection (Union[Unset, bool]):
        all_trusted_domains (Union[Unset, bool]):
        domain_controller (Union[Unset, str]):
        ous (Union[Unset, List['ModelOuDetails']]):
        domains (Union[Unset, List['ModelDomainDetails']]):
        domain_results (Union[Unset, List['ModelDomainCollectionResult']]):
    """

    id: Union[Unset, int] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_name: Union[Unset, str] = UNSET
    event_id: Union[Unset, "NullInt32"] = UNSET
    execution_time: Union[Unset, datetime.datetime] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, EnumJobStatus] = UNSET
    status_message: Union[Unset, str] = UNSET
    session_collection: Union[Unset, bool] = UNSET
    local_group_collection: Union[Unset, bool] = UNSET
    ad_structure_collection: Union[Unset, bool] = UNSET
    cert_services_collection: Union[Unset, bool] = UNSET
    ca_registry_collection: Union[Unset, bool] = UNSET
    dc_registry_collection: Union[Unset, bool] = UNSET
    all_trusted_domains: Union[Unset, bool] = UNSET
    domain_controller: Union[Unset, str] = UNSET
    ous: Union[Unset, List["ModelOuDetails"]] = UNSET
    domains: Union[Unset, List["ModelDomainDetails"]] = UNSET
    domain_results: Union[Unset, List["ModelDomainCollectionResult"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        client_id = self.client_id

        client_name = self.client_name

        event_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.event_id, Unset):
            event_id = self.event_id.to_dict()

        execution_time: Union[Unset, str] = UNSET
        if not isinstance(self.execution_time, Unset):
            execution_time = self.execution_time.isoformat()

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_message = self.status_message

        session_collection = self.session_collection

        local_group_collection = self.local_group_collection

        ad_structure_collection = self.ad_structure_collection

        cert_services_collection = self.cert_services_collection

        ca_registry_collection = self.ca_registry_collection

        dc_registry_collection = self.dc_registry_collection

        all_trusted_domains = self.all_trusted_domains

        domain_controller = self.domain_controller

        ous: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ous, Unset):
            ous = []
            for ous_item_data in self.ous:
                ous_item = ous_item_data.to_dict()
                ous.append(ous_item)

        domains: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.domains, Unset):
            domains = []
            for domains_item_data in self.domains:
                domains_item = domains_item_data.to_dict()
                domains.append(domains_item)

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
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_name is not UNSET:
            field_dict["client_name"] = client_name
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if execution_time is not UNSET:
            field_dict["execution_time"] = execution_time
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["status_message"] = status_message
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
        from ..models.model_domain_details import ModelDomainDetails
        from ..models.model_ou_details import ModelOuDetails
        from ..models.null_int_32 import NullInt32

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        client_id = d.pop("client_id", UNSET)

        client_name = d.pop("client_name", UNSET)

        _event_id = d.pop("event_id", UNSET)
        event_id: Union[Unset, NullInt32]
        if isinstance(_event_id, Unset):
            event_id = UNSET
        else:
            event_id = NullInt32.from_dict(_event_id)

        _execution_time = d.pop("execution_time", UNSET)
        execution_time: Union[Unset, datetime.datetime]
        if isinstance(_execution_time, Unset):
            execution_time = UNSET
        else:
            execution_time = isoparse(_execution_time)

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

        _status = d.pop("status", UNSET)
        status: Union[Unset, EnumJobStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = EnumJobStatus(_status)

        status_message = d.pop("status_message", UNSET)

        session_collection = d.pop("session_collection", UNSET)

        local_group_collection = d.pop("local_group_collection", UNSET)

        ad_structure_collection = d.pop("ad_structure_collection", UNSET)

        cert_services_collection = d.pop("cert_services_collection", UNSET)

        ca_registry_collection = d.pop("ca_registry_collection", UNSET)

        dc_registry_collection = d.pop("dc_registry_collection", UNSET)

        all_trusted_domains = d.pop("all_trusted_domains", UNSET)

        domain_controller = d.pop("domain_controller", UNSET)

        ous = []
        _ous = d.pop("ous", UNSET)
        for ous_item_data in _ous or []:
            ous_item = ModelOuDetails.from_dict(ous_item_data)

            ous.append(ous_item)

        domains = []
        _domains = d.pop("domains", UNSET)
        for domains_item_data in _domains or []:
            domains_item = ModelDomainDetails.from_dict(domains_item_data)

            domains.append(domains_item)

        domain_results = []
        _domain_results = d.pop("domain_results", UNSET)
        for domain_results_item_data in _domain_results or []:
            domain_results_item = ModelDomainCollectionResult.from_dict(domain_results_item_data)

            domain_results.append(domain_results_item)

        model_client_scheduled_job_display = cls(
            id=id,
            client_id=client_id,
            client_name=client_name,
            event_id=event_id,
            execution_time=execution_time,
            start_time=start_time,
            end_time=end_time,
            status=status,
            status_message=status_message,
            session_collection=session_collection,
            local_group_collection=local_group_collection,
            ad_structure_collection=ad_structure_collection,
            cert_services_collection=cert_services_collection,
            ca_registry_collection=ca_registry_collection,
            dc_registry_collection=dc_registry_collection,
            all_trusted_domains=all_trusted_domains,
            domain_controller=domain_controller,
            ous=ous,
            domains=domains,
            domain_results=domain_results,
        )

        model_client_scheduled_job_display.additional_properties = d
        return model_client_scheduled_job_display

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
