import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_list_finding_props import ModelListFindingProps
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelListFinding")


@_attrs_define
class ModelListFinding:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        principal (Union[Unset, str]):
        principal_kind (Union[Unset, str]):
        finding (Union[Unset, str]):
        domain_sid (Union[Unset, str]):
        props (Union[Unset, ModelListFindingProps]):
        accepted_until (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    principal: Union[Unset, str] = UNSET
    principal_kind: Union[Unset, str] = UNSET
    finding: Union[Unset, str] = UNSET
    domain_sid: Union[Unset, str] = UNSET
    props: Union[Unset, "ModelListFindingProps"] = UNSET
    accepted_until: Union[Unset, datetime.datetime] = UNSET
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

        principal = self.principal

        principal_kind = self.principal_kind

        finding = self.finding

        domain_sid = self.domain_sid

        props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.props, Unset):
            props = self.props.to_dict()

        accepted_until: Union[Unset, str] = UNSET
        if not isinstance(self.accepted_until, Unset):
            accepted_until = self.accepted_until.isoformat()

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
        if principal is not UNSET:
            field_dict["Principal"] = principal
        if principal_kind is not UNSET:
            field_dict["PrincipalKind"] = principal_kind
        if finding is not UNSET:
            field_dict["Finding"] = finding
        if domain_sid is not UNSET:
            field_dict["DomainSID"] = domain_sid
        if props is not UNSET:
            field_dict["Props"] = props
        if accepted_until is not UNSET:
            field_dict["accepted_until"] = accepted_until

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_list_finding_props import ModelListFindingProps
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

        principal = d.pop("Principal", UNSET)

        principal_kind = d.pop("PrincipalKind", UNSET)

        finding = d.pop("Finding", UNSET)

        domain_sid = d.pop("DomainSID", UNSET)

        _props = d.pop("Props", UNSET)
        props: Union[Unset, ModelListFindingProps]
        if isinstance(_props, Unset):
            props = UNSET
        else:
            props = ModelListFindingProps.from_dict(_props)

        _accepted_until = d.pop("accepted_until", UNSET)
        accepted_until: Union[Unset, datetime.datetime]
        if isinstance(_accepted_until, Unset):
            accepted_until = UNSET
        else:
            accepted_until = isoparse(_accepted_until)

        model_list_finding = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            principal=principal,
            principal_kind=principal_kind,
            finding=finding,
            domain_sid=domain_sid,
            props=props,
            accepted_until=accepted_until,
        )

        model_list_finding.additional_properties = d
        return model_list_finding

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
