import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelAdDataQualityStat")


@_attrs_define
class ModelAdDataQualityStat:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        domain_sid (Union[Unset, str]):
        users (Union[Unset, int]):
        groups (Union[Unset, int]):
        computers (Union[Unset, int]):
        ous (Union[Unset, int]):
        containers (Union[Unset, int]):
        gpos (Union[Unset, int]):
        aiacas (Union[Unset, int]):
        rootcas (Union[Unset, int]):
        enterprisecas (Union[Unset, int]):
        ntauthstores (Union[Unset, int]):
        certtemplates (Union[Unset, int]):
        acls (Union[Unset, int]):
        sessions (Union[Unset, int]):
        relationships (Union[Unset, int]):
        session_completeness (Union[Unset, float]):
        local_group_completeness (Union[Unset, float]):
        run_id (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    domain_sid: Union[Unset, str] = UNSET
    users: Union[Unset, int] = UNSET
    groups: Union[Unset, int] = UNSET
    computers: Union[Unset, int] = UNSET
    ous: Union[Unset, int] = UNSET
    containers: Union[Unset, int] = UNSET
    gpos: Union[Unset, int] = UNSET
    aiacas: Union[Unset, int] = UNSET
    rootcas: Union[Unset, int] = UNSET
    enterprisecas: Union[Unset, int] = UNSET
    ntauthstores: Union[Unset, int] = UNSET
    certtemplates: Union[Unset, int] = UNSET
    acls: Union[Unset, int] = UNSET
    sessions: Union[Unset, int] = UNSET
    relationships: Union[Unset, int] = UNSET
    session_completeness: Union[Unset, float] = UNSET
    local_group_completeness: Union[Unset, float] = UNSET
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

        domain_sid = self.domain_sid

        users = self.users

        groups = self.groups

        computers = self.computers

        ous = self.ous

        containers = self.containers

        gpos = self.gpos

        aiacas = self.aiacas

        rootcas = self.rootcas

        enterprisecas = self.enterprisecas

        ntauthstores = self.ntauthstores

        certtemplates = self.certtemplates

        acls = self.acls

        sessions = self.sessions

        relationships = self.relationships

        session_completeness = self.session_completeness

        local_group_completeness = self.local_group_completeness

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
        if domain_sid is not UNSET:
            field_dict["domain_sid"] = domain_sid
        if users is not UNSET:
            field_dict["users"] = users
        if groups is not UNSET:
            field_dict["groups"] = groups
        if computers is not UNSET:
            field_dict["computers"] = computers
        if ous is not UNSET:
            field_dict["ous"] = ous
        if containers is not UNSET:
            field_dict["containers"] = containers
        if gpos is not UNSET:
            field_dict["gpos"] = gpos
        if aiacas is not UNSET:
            field_dict["aiacas"] = aiacas
        if rootcas is not UNSET:
            field_dict["rootcas"] = rootcas
        if enterprisecas is not UNSET:
            field_dict["enterprisecas"] = enterprisecas
        if ntauthstores is not UNSET:
            field_dict["ntauthstores"] = ntauthstores
        if certtemplates is not UNSET:
            field_dict["certtemplates"] = certtemplates
        if acls is not UNSET:
            field_dict["acls"] = acls
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if relationships is not UNSET:
            field_dict["relationships"] = relationships
        if session_completeness is not UNSET:
            field_dict["session_completeness"] = session_completeness
        if local_group_completeness is not UNSET:
            field_dict["local_group_completeness"] = local_group_completeness
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

        domain_sid = d.pop("domain_sid", UNSET)

        users = d.pop("users", UNSET)

        groups = d.pop("groups", UNSET)

        computers = d.pop("computers", UNSET)

        ous = d.pop("ous", UNSET)

        containers = d.pop("containers", UNSET)

        gpos = d.pop("gpos", UNSET)

        aiacas = d.pop("aiacas", UNSET)

        rootcas = d.pop("rootcas", UNSET)

        enterprisecas = d.pop("enterprisecas", UNSET)

        ntauthstores = d.pop("ntauthstores", UNSET)

        certtemplates = d.pop("certtemplates", UNSET)

        acls = d.pop("acls", UNSET)

        sessions = d.pop("sessions", UNSET)

        relationships = d.pop("relationships", UNSET)

        session_completeness = d.pop("session_completeness", UNSET)

        local_group_completeness = d.pop("local_group_completeness", UNSET)

        run_id = d.pop("run_id", UNSET)

        model_ad_data_quality_stat = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            domain_sid=domain_sid,
            users=users,
            groups=groups,
            computers=computers,
            ous=ous,
            containers=containers,
            gpos=gpos,
            aiacas=aiacas,
            rootcas=rootcas,
            enterprisecas=enterprisecas,
            ntauthstores=ntauthstores,
            certtemplates=certtemplates,
            acls=acls,
            sessions=sessions,
            relationships=relationships,
            session_completeness=session_completeness,
            local_group_completeness=local_group_completeness,
            run_id=run_id,
        )

        model_ad_data_quality_stat.additional_properties = d
        return model_ad_data_quality_stat

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
