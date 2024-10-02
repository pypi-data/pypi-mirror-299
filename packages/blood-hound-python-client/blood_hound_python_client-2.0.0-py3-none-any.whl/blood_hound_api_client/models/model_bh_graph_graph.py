from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.model_bh_graph_edge import ModelBhGraphEdge
    from ..models.model_bh_graph_node import ModelBhGraphNode


T = TypeVar("T", bound="ModelBhGraphGraph")


@_attrs_define
class ModelBhGraphGraph:
    """ """

    additional_properties: Dict[str, Union["ModelBhGraphEdge", "ModelBhGraphNode"]] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        from ..models.model_bh_graph_node import ModelBhGraphNode

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ModelBhGraphNode):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_bh_graph_edge import ModelBhGraphEdge
        from ..models.model_bh_graph_node import ModelBhGraphNode

        d = src_dict.copy()
        model_bh_graph_graph = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union["ModelBhGraphEdge", "ModelBhGraphNode"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = ModelBhGraphNode.from_dict(data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                additional_property_type_1 = ModelBhGraphEdge.from_dict(data)

                return additional_property_type_1

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        model_bh_graph_graph.additional_properties = additional_properties
        return model_bh_graph_graph

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["ModelBhGraphEdge", "ModelBhGraphNode"]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union["ModelBhGraphEdge", "ModelBhGraphNode"]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
