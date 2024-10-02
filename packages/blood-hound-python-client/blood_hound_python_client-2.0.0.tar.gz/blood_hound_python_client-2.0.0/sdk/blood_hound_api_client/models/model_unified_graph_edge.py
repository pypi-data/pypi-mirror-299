import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_unified_graph_edge_properties import ModelUnifiedGraphEdgeProperties


T = TypeVar("T", bound="ModelUnifiedGraphEdge")


@_attrs_define
class ModelUnifiedGraphEdge:
    """
    Attributes:
        source (Union[Unset, str]):
        target (Union[Unset, str]):
        label (Union[Unset, str]):
        kind (Union[Unset, str]):
        last_seen (Union[Unset, datetime.datetime]):
        properties (Union[Unset, ModelUnifiedGraphEdgeProperties]):
    """

    source: Union[Unset, str] = UNSET
    target: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    last_seen: Union[Unset, datetime.datetime] = UNSET
    properties: Union[Unset, "ModelUnifiedGraphEdgeProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source

        target = self.target

        label = self.label

        kind = self.kind

        last_seen: Union[Unset, str] = UNSET
        if not isinstance(self.last_seen, Unset):
            last_seen = self.last_seen.isoformat()

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if target is not UNSET:
            field_dict["target"] = target
        if label is not UNSET:
            field_dict["label"] = label
        if kind is not UNSET:
            field_dict["kind"] = kind
        if last_seen is not UNSET:
            field_dict["lastSeen"] = last_seen
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_unified_graph_edge_properties import ModelUnifiedGraphEdgeProperties

        d = src_dict.copy()
        source = d.pop("source", UNSET)

        target = d.pop("target", UNSET)

        label = d.pop("label", UNSET)

        kind = d.pop("kind", UNSET)

        _last_seen = d.pop("lastSeen", UNSET)
        last_seen: Union[Unset, datetime.datetime]
        if isinstance(_last_seen, Unset):
            last_seen = UNSET
        else:
            last_seen = isoparse(_last_seen)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ModelUnifiedGraphEdgeProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ModelUnifiedGraphEdgeProperties.from_dict(_properties)

        model_unified_graph_edge = cls(
            source=source,
            target=target,
            label=label,
            kind=kind,
            last_seen=last_seen,
            properties=properties,
        )

        model_unified_graph_edge.additional_properties = d
        return model_unified_graph_edge

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
