import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelClientSchedule")


@_attrs_define
class ModelClientSchedule:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        client_id (Union[Unset, str]):
        rrule (Union[Unset, str]):
        session_collection (Union[Unset, bool]):
        local_group_collection (Union[Unset, bool]):
        ad_structure_collection (Union[Unset, bool]):
        cert_services_collection (Union[Unset, bool]):
        ca_registry_collection (Union[Unset, bool]):
        dc_registry_collection (Union[Unset, bool]):
        all_trusted_domains (Union[Unset, bool]):
        next_scheduled_at (Union[Unset, datetime.datetime]):
        ous (Union[Unset, List[str]]):
        domains (Union[Unset, List[str]]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    client_id: Union[Unset, str] = UNSET
    rrule: Union[Unset, str] = UNSET
    session_collection: Union[Unset, bool] = UNSET
    local_group_collection: Union[Unset, bool] = UNSET
    ad_structure_collection: Union[Unset, bool] = UNSET
    cert_services_collection: Union[Unset, bool] = UNSET
    ca_registry_collection: Union[Unset, bool] = UNSET
    dc_registry_collection: Union[Unset, bool] = UNSET
    all_trusted_domains: Union[Unset, bool] = UNSET
    next_scheduled_at: Union[Unset, datetime.datetime] = UNSET
    ous: Union[Unset, List[str]] = UNSET
    domains: Union[Unset, List[str]] = UNSET
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

        rrule = self.rrule

        session_collection = self.session_collection

        local_group_collection = self.local_group_collection

        ad_structure_collection = self.ad_structure_collection

        cert_services_collection = self.cert_services_collection

        ca_registry_collection = self.ca_registry_collection

        dc_registry_collection = self.dc_registry_collection

        all_trusted_domains = self.all_trusted_domains

        next_scheduled_at: Union[Unset, str] = UNSET
        if not isinstance(self.next_scheduled_at, Unset):
            next_scheduled_at = self.next_scheduled_at.isoformat()

        ous: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ous, Unset):
            ous = self.ous

        domains: Union[Unset, List[str]] = UNSET
        if not isinstance(self.domains, Unset):
            domains = self.domains

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
        if rrule is not UNSET:
            field_dict["rrule"] = rrule
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
        if next_scheduled_at is not UNSET:
            field_dict["next_scheduled_at"] = next_scheduled_at
        if ous is not UNSET:
            field_dict["ous"] = ous
        if domains is not UNSET:
            field_dict["domains"] = domains

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

        client_id = d.pop("client_id", UNSET)

        rrule = d.pop("rrule", UNSET)

        session_collection = d.pop("session_collection", UNSET)

        local_group_collection = d.pop("local_group_collection", UNSET)

        ad_structure_collection = d.pop("ad_structure_collection", UNSET)

        cert_services_collection = d.pop("cert_services_collection", UNSET)

        ca_registry_collection = d.pop("ca_registry_collection", UNSET)

        dc_registry_collection = d.pop("dc_registry_collection", UNSET)

        all_trusted_domains = d.pop("all_trusted_domains", UNSET)

        _next_scheduled_at = d.pop("next_scheduled_at", UNSET)
        next_scheduled_at: Union[Unset, datetime.datetime]
        if isinstance(_next_scheduled_at, Unset):
            next_scheduled_at = UNSET
        else:
            next_scheduled_at = isoparse(_next_scheduled_at)

        ous = cast(List[str], d.pop("ous", UNSET))

        domains = cast(List[str], d.pop("domains", UNSET))

        model_client_schedule = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            client_id=client_id,
            rrule=rrule,
            session_collection=session_collection,
            local_group_collection=local_group_collection,
            ad_structure_collection=ad_structure_collection,
            cert_services_collection=cert_services_collection,
            ca_registry_collection=ca_registry_collection,
            dc_registry_collection=dc_registry_collection,
            all_trusted_domains=all_trusted_domains,
            next_scheduled_at=next_scheduled_at,
            ous=ous,
            domains=domains,
        )

        model_client_schedule.additional_properties = d
        return model_client_schedule

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
