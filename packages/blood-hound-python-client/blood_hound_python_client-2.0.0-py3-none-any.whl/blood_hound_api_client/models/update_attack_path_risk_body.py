import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateAttackPathRiskBody")


@_attrs_define
class UpdateAttackPathRiskBody:
    """
    Attributes:
        risk_type (Union[Unset, str]):
        accept_until (Union[Unset, datetime.datetime]):
        accepted (Union[Unset, bool]):
    """

    risk_type: Union[Unset, str] = UNSET
    accept_until: Union[Unset, datetime.datetime] = UNSET
    accepted: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        risk_type = self.risk_type

        accept_until: Union[Unset, str] = UNSET
        if not isinstance(self.accept_until, Unset):
            accept_until = self.accept_until.isoformat()

        accepted = self.accepted

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if risk_type is not UNSET:
            field_dict["risk_type"] = risk_type
        if accept_until is not UNSET:
            field_dict["accept_until"] = accept_until
        if accepted is not UNSET:
            field_dict["accepted"] = accepted

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        risk_type = d.pop("risk_type", UNSET)

        _accept_until = d.pop("accept_until", UNSET)
        accept_until: Union[Unset, datetime.datetime]
        if isinstance(_accept_until, Unset):
            accept_until = UNSET
        else:
            accept_until = isoparse(_accept_until)

        accepted = d.pop("accepted", UNSET)

        update_attack_path_risk_body = cls(
            risk_type=risk_type,
            accept_until=accept_until,
            accepted=accepted,
        )

        update_attack_path_risk_body.additional_properties = d
        return update_attack_path_risk_body

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
