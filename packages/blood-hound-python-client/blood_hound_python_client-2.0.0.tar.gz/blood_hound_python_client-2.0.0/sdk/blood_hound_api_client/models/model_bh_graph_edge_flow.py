from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelBhGraphEdgeFlow")


@_attrs_define
class ModelBhGraphEdgeFlow:
    """
    Attributes:
        velocity (Union[Unset, int]):
    """

    velocity: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        velocity = self.velocity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if velocity is not UNSET:
            field_dict["velocity"] = velocity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        velocity = d.pop("velocity", UNSET)

        model_bh_graph_edge_flow = cls(
            velocity=velocity,
        )

        model_bh_graph_edge_flow.additional_properties = d
        return model_bh_graph_edge_flow

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
