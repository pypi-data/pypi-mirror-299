from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_domain_details import ModelDomainDetails
    from ..models.model_ou_details import ModelOuDetails


T = TypeVar("T", bound="ModelClientScheduleDisplay")


@_attrs_define
class ModelClientScheduleDisplay:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        client_id (Union[Unset, str]):
        rrule (Union[Unset, str]):
        session_collection (Union[Unset, bool]):
        local_group_collection (Union[Unset, bool]):
        ad_structure_collection (Union[Unset, bool]):
        cert_services_collection (Union[Unset, bool]):
        ca_registry_collection (Union[Unset, bool]):
        dc_registry_collection (Union[Unset, bool]):
        all_trusted_domains (Union[Unset, bool]):
        ous (Union[Unset, List['ModelOuDetails']]):
        domains (Union[Unset, List['ModelDomainDetails']]):
    """

    id: Union[Unset, int] = UNSET
    client_id: Union[Unset, str] = UNSET
    rrule: Union[Unset, str] = UNSET
    session_collection: Union[Unset, bool] = UNSET
    local_group_collection: Union[Unset, bool] = UNSET
    ad_structure_collection: Union[Unset, bool] = UNSET
    cert_services_collection: Union[Unset, bool] = UNSET
    ca_registry_collection: Union[Unset, bool] = UNSET
    dc_registry_collection: Union[Unset, bool] = UNSET
    all_trusted_domains: Union[Unset, bool] = UNSET
    ous: Union[Unset, List["ModelOuDetails"]] = UNSET
    domains: Union[Unset, List["ModelDomainDetails"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        client_id = self.client_id

        rrule = self.rrule

        session_collection = self.session_collection

        local_group_collection = self.local_group_collection

        ad_structure_collection = self.ad_structure_collection

        cert_services_collection = self.cert_services_collection

        ca_registry_collection = self.ca_registry_collection

        dc_registry_collection = self.dc_registry_collection

        all_trusted_domains = self.all_trusted_domains

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
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
        if ous is not UNSET:
            field_dict["ous"] = ous
        if domains is not UNSET:
            field_dict["domains"] = domains

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_domain_details import ModelDomainDetails
        from ..models.model_ou_details import ModelOuDetails

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        client_id = d.pop("client_id", UNSET)

        rrule = d.pop("rrule", UNSET)

        session_collection = d.pop("session_collection", UNSET)

        local_group_collection = d.pop("local_group_collection", UNSET)

        ad_structure_collection = d.pop("ad_structure_collection", UNSET)

        cert_services_collection = d.pop("cert_services_collection", UNSET)

        ca_registry_collection = d.pop("ca_registry_collection", UNSET)

        dc_registry_collection = d.pop("dc_registry_collection", UNSET)

        all_trusted_domains = d.pop("all_trusted_domains", UNSET)

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

        model_client_schedule_display = cls(
            id=id,
            client_id=client_id,
            rrule=rrule,
            session_collection=session_collection,
            local_group_collection=local_group_collection,
            ad_structure_collection=ad_structure_collection,
            cert_services_collection=cert_services_collection,
            ca_registry_collection=ca_registry_collection,
            dc_registry_collection=dc_registry_collection,
            all_trusted_domains=all_trusted_domains,
            ous=ous,
            domains=domains,
        )

        model_client_schedule_display.additional_properties = d
        return model_client_schedule_display

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
