import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelAzureDataQualityStat")


@_attrs_define
class ModelAzureDataQualityStat:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        tenantid (Union[Unset, str]):
        users (Union[Unset, int]):
        groups (Union[Unset, int]):
        apps (Union[Unset, int]):
        service_principals (Union[Unset, int]):
        devices (Union[Unset, int]):
        management_groups (Union[Unset, int]):
        subscriptions (Union[Unset, int]):
        resource_groups (Union[Unset, int]):
        vms (Union[Unset, int]):
        key_vaults (Union[Unset, int]):
        relationships (Union[Unset, int]):
        run_id (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    tenantid: Union[Unset, str] = UNSET
    users: Union[Unset, int] = UNSET
    groups: Union[Unset, int] = UNSET
    apps: Union[Unset, int] = UNSET
    service_principals: Union[Unset, int] = UNSET
    devices: Union[Unset, int] = UNSET
    management_groups: Union[Unset, int] = UNSET
    subscriptions: Union[Unset, int] = UNSET
    resource_groups: Union[Unset, int] = UNSET
    vms: Union[Unset, int] = UNSET
    key_vaults: Union[Unset, int] = UNSET
    relationships: Union[Unset, int] = UNSET
    run_id: Union[Unset, str] = UNSET
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

        tenantid = self.tenantid

        users = self.users

        groups = self.groups

        apps = self.apps

        service_principals = self.service_principals

        devices = self.devices

        management_groups = self.management_groups

        subscriptions = self.subscriptions

        resource_groups = self.resource_groups

        vms = self.vms

        key_vaults = self.key_vaults

        relationships = self.relationships

        run_id = self.run_id

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
        if tenantid is not UNSET:
            field_dict["tenantid"] = tenantid
        if users is not UNSET:
            field_dict["users"] = users
        if groups is not UNSET:
            field_dict["groups"] = groups
        if apps is not UNSET:
            field_dict["apps"] = apps
        if service_principals is not UNSET:
            field_dict["service_principals"] = service_principals
        if devices is not UNSET:
            field_dict["devices"] = devices
        if management_groups is not UNSET:
            field_dict["management_groups"] = management_groups
        if subscriptions is not UNSET:
            field_dict["subscriptions"] = subscriptions
        if resource_groups is not UNSET:
            field_dict["resource_groups"] = resource_groups
        if vms is not UNSET:
            field_dict["vms"] = vms
        if key_vaults is not UNSET:
            field_dict["key_vaults"] = key_vaults
        if relationships is not UNSET:
            field_dict["relationships"] = relationships
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

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

        tenantid = d.pop("tenantid", UNSET)

        users = d.pop("users", UNSET)

        groups = d.pop("groups", UNSET)

        apps = d.pop("apps", UNSET)

        service_principals = d.pop("service_principals", UNSET)

        devices = d.pop("devices", UNSET)

        management_groups = d.pop("management_groups", UNSET)

        subscriptions = d.pop("subscriptions", UNSET)

        resource_groups = d.pop("resource_groups", UNSET)

        vms = d.pop("vms", UNSET)

        key_vaults = d.pop("key_vaults", UNSET)

        relationships = d.pop("relationships", UNSET)

        run_id = d.pop("run_id", UNSET)

        model_azure_data_quality_stat = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            tenantid=tenantid,
            users=users,
            groups=groups,
            apps=apps,
            service_principals=service_principals,
            devices=devices,
            management_groups=management_groups,
            subscriptions=subscriptions,
            resource_groups=resource_groups,
            vms=vms,
            key_vaults=key_vaults,
            relationships=relationships,
            run_id=run_id,
        )

        model_azure_data_quality_stat.additional_properties = d
        return model_azure_data_quality_stat

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
