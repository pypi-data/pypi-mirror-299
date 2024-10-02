import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelRiskCounts")


@_attrs_define
class ModelRiskCounts:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        composite_risk (Union[Unset, float]):
        finding_count (Union[Unset, int]):
        impacted_asset_count (Union[Unset, int]):
        domain_sid (Union[Unset, str]):
        finding (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    composite_risk: Union[Unset, float] = UNSET
    finding_count: Union[Unset, int] = UNSET
    impacted_asset_count: Union[Unset, int] = UNSET
    domain_sid: Union[Unset, str] = UNSET
    finding: Union[Unset, str] = UNSET
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

        composite_risk = self.composite_risk

        finding_count = self.finding_count

        impacted_asset_count = self.impacted_asset_count

        domain_sid = self.domain_sid

        finding = self.finding

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
        if composite_risk is not UNSET:
            field_dict["CompositeRisk"] = composite_risk
        if finding_count is not UNSET:
            field_dict["FindingCount"] = finding_count
        if impacted_asset_count is not UNSET:
            field_dict["ImpactedAssetCount"] = impacted_asset_count
        if domain_sid is not UNSET:
            field_dict["DomainSID"] = domain_sid
        if finding is not UNSET:
            field_dict["Finding"] = finding

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

        composite_risk = d.pop("CompositeRisk", UNSET)

        finding_count = d.pop("FindingCount", UNSET)

        impacted_asset_count = d.pop("ImpactedAssetCount", UNSET)

        domain_sid = d.pop("DomainSID", UNSET)

        finding = d.pop("Finding", UNSET)

        model_risk_counts = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            composite_risk=composite_risk,
            finding_count=finding_count,
            impacted_asset_count=impacted_asset_count,
            domain_sid=domain_sid,
            finding=finding,
        )

        model_risk_counts.additional_properties = d
        return model_risk_counts

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
