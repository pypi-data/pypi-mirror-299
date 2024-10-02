import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_relationship_finding_from_principal_props import ModelRelationshipFindingFromPrincipalProps
    from ..models.model_relationship_finding_rel_props import ModelRelationshipFindingRelProps
    from ..models.model_relationship_finding_to_principal_props import ModelRelationshipFindingToPrincipalProps
    from ..models.null_int_64 import NullInt64
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ListDomainAttackPathsDetailsResponse200Type0DataItem")


@_attrs_define
class ListDomainAttackPathsDetailsResponse200Type0DataItem:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        from_principal (Union[Unset, str]):
        to_principal (Union[Unset, str]):
        from_principal_props (Union[Unset, ModelRelationshipFindingFromPrincipalProps]):
        from_principal_kind (Union[Unset, str]):
        to_principal_props (Union[Unset, ModelRelationshipFindingToPrincipalProps]):
        to_principal_kind (Union[Unset, str]):
        rel_props (Union[Unset, ModelRelationshipFindingRelProps]):
        combo_graph_relation_id (Union[Unset, NullInt64]):
        finding (Union[Unset, str]):
        domain_sid (Union[Unset, str]):
        principal_hash (Union[Unset, str]):
        accepted_until (Union[Unset, datetime.datetime]):
        accepted (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    from_principal: Union[Unset, str] = UNSET
    to_principal: Union[Unset, str] = UNSET
    from_principal_props: Union[Unset, "ModelRelationshipFindingFromPrincipalProps"] = UNSET
    from_principal_kind: Union[Unset, str] = UNSET
    to_principal_props: Union[Unset, "ModelRelationshipFindingToPrincipalProps"] = UNSET
    to_principal_kind: Union[Unset, str] = UNSET
    rel_props: Union[Unset, "ModelRelationshipFindingRelProps"] = UNSET
    combo_graph_relation_id: Union[Unset, "NullInt64"] = UNSET
    finding: Union[Unset, str] = UNSET
    domain_sid: Union[Unset, str] = UNSET
    principal_hash: Union[Unset, str] = UNSET
    accepted_until: Union[Unset, datetime.datetime] = UNSET
    accepted: Union[Unset, bool] = UNSET
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

        from_principal = self.from_principal

        to_principal = self.to_principal

        from_principal_props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.from_principal_props, Unset):
            from_principal_props = self.from_principal_props.to_dict()

        from_principal_kind = self.from_principal_kind

        to_principal_props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.to_principal_props, Unset):
            to_principal_props = self.to_principal_props.to_dict()

        to_principal_kind = self.to_principal_kind

        rel_props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rel_props, Unset):
            rel_props = self.rel_props.to_dict()

        combo_graph_relation_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.combo_graph_relation_id, Unset):
            combo_graph_relation_id = self.combo_graph_relation_id.to_dict()

        finding = self.finding

        domain_sid = self.domain_sid

        principal_hash = self.principal_hash

        accepted_until: Union[Unset, str] = UNSET
        if not isinstance(self.accepted_until, Unset):
            accepted_until = self.accepted_until.isoformat()

        accepted = self.accepted

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
        if from_principal is not UNSET:
            field_dict["FromPrincipal"] = from_principal
        if to_principal is not UNSET:
            field_dict["ToPrincipal"] = to_principal
        if from_principal_props is not UNSET:
            field_dict["FromPrincipalProps"] = from_principal_props
        if from_principal_kind is not UNSET:
            field_dict["FromPrincipalKind"] = from_principal_kind
        if to_principal_props is not UNSET:
            field_dict["ToPrincipalProps"] = to_principal_props
        if to_principal_kind is not UNSET:
            field_dict["ToPrincipalKind"] = to_principal_kind
        if rel_props is not UNSET:
            field_dict["RelProps"] = rel_props
        if combo_graph_relation_id is not UNSET:
            field_dict["ComboGraphRelationID"] = combo_graph_relation_id
        if finding is not UNSET:
            field_dict["Finding"] = finding
        if domain_sid is not UNSET:
            field_dict["DomainSID"] = domain_sid
        if principal_hash is not UNSET:
            field_dict["PrincipalHash"] = principal_hash
        if accepted_until is not UNSET:
            field_dict["AcceptedUntil"] = accepted_until
        if accepted is not UNSET:
            field_dict["Accepted"] = accepted

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_relationship_finding_from_principal_props import ModelRelationshipFindingFromPrincipalProps
        from ..models.model_relationship_finding_rel_props import ModelRelationshipFindingRelProps
        from ..models.model_relationship_finding_to_principal_props import ModelRelationshipFindingToPrincipalProps
        from ..models.null_int_64 import NullInt64
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

        from_principal = d.pop("FromPrincipal", UNSET)

        to_principal = d.pop("ToPrincipal", UNSET)

        _from_principal_props = d.pop("FromPrincipalProps", UNSET)
        from_principal_props: Union[Unset, ModelRelationshipFindingFromPrincipalProps]
        if isinstance(_from_principal_props, Unset):
            from_principal_props = UNSET
        else:
            from_principal_props = ModelRelationshipFindingFromPrincipalProps.from_dict(_from_principal_props)

        from_principal_kind = d.pop("FromPrincipalKind", UNSET)

        _to_principal_props = d.pop("ToPrincipalProps", UNSET)
        to_principal_props: Union[Unset, ModelRelationshipFindingToPrincipalProps]
        if isinstance(_to_principal_props, Unset):
            to_principal_props = UNSET
        else:
            to_principal_props = ModelRelationshipFindingToPrincipalProps.from_dict(_to_principal_props)

        to_principal_kind = d.pop("ToPrincipalKind", UNSET)

        _rel_props = d.pop("RelProps", UNSET)
        rel_props: Union[Unset, ModelRelationshipFindingRelProps]
        if isinstance(_rel_props, Unset):
            rel_props = UNSET
        else:
            rel_props = ModelRelationshipFindingRelProps.from_dict(_rel_props)

        _combo_graph_relation_id = d.pop("ComboGraphRelationID", UNSET)
        combo_graph_relation_id: Union[Unset, NullInt64]
        if isinstance(_combo_graph_relation_id, Unset):
            combo_graph_relation_id = UNSET
        else:
            combo_graph_relation_id = NullInt64.from_dict(_combo_graph_relation_id)

        finding = d.pop("Finding", UNSET)

        domain_sid = d.pop("DomainSID", UNSET)

        principal_hash = d.pop("PrincipalHash", UNSET)

        _accepted_until = d.pop("AcceptedUntil", UNSET)
        accepted_until: Union[Unset, datetime.datetime]
        if isinstance(_accepted_until, Unset):
            accepted_until = UNSET
        else:
            accepted_until = isoparse(_accepted_until)

        accepted = d.pop("Accepted", UNSET)

        list_domain_attack_paths_details_response_200_type_0_data_item = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            from_principal=from_principal,
            to_principal=to_principal,
            from_principal_props=from_principal_props,
            from_principal_kind=from_principal_kind,
            to_principal_props=to_principal_props,
            to_principal_kind=to_principal_kind,
            rel_props=rel_props,
            combo_graph_relation_id=combo_graph_relation_id,
            finding=finding,
            domain_sid=domain_sid,
            principal_hash=principal_hash,
            accepted_until=accepted_until,
            accepted=accepted,
        )

        list_domain_attack_paths_details_response_200_type_0_data_item.additional_properties = d
        return list_domain_attack_paths_details_response_200_type_0_data_item

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
