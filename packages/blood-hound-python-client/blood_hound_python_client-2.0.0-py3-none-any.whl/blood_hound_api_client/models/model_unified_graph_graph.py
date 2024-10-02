from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_unified_graph_edge import ModelUnifiedGraphEdge
    from ..models.model_unified_graph_graph_nodes import ModelUnifiedGraphGraphNodes


T = TypeVar("T", bound="ModelUnifiedGraphGraph")


@_attrs_define
class ModelUnifiedGraphGraph:
    """
    Attributes:
        nodes (Union[Unset, ModelUnifiedGraphGraphNodes]):
        edges (Union[Unset, List['ModelUnifiedGraphEdge']]):
    """

    nodes: Union[Unset, "ModelUnifiedGraphGraphNodes"] = UNSET
    edges: Union[Unset, List["ModelUnifiedGraphEdge"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        nodes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = self.nodes.to_dict()

        edges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.edges, Unset):
            edges = []
            for edges_item_data in self.edges:
                edges_item = edges_item_data.to_dict()
                edges.append(edges_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if edges is not UNSET:
            field_dict["edges"] = edges

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_unified_graph_edge import ModelUnifiedGraphEdge
        from ..models.model_unified_graph_graph_nodes import ModelUnifiedGraphGraphNodes

        d = src_dict.copy()
        _nodes = d.pop("nodes", UNSET)
        nodes: Union[Unset, ModelUnifiedGraphGraphNodes]
        if isinstance(_nodes, Unset):
            nodes = UNSET
        else:
            nodes = ModelUnifiedGraphGraphNodes.from_dict(_nodes)

        edges = []
        _edges = d.pop("edges", UNSET)
        for edges_item_data in _edges or []:
            edges_item = ModelUnifiedGraphEdge.from_dict(edges_item_data)

            edges.append(edges_item)

        model_unified_graph_graph = cls(
            nodes=nodes,
            edges=edges,
        )

        model_unified_graph_graph.additional_properties = d
        return model_unified_graph_graph

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
