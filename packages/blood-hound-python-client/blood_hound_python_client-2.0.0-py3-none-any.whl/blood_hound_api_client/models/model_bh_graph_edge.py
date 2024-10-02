from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_bh_graph_edge_flow import ModelBhGraphEdgeFlow
    from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
    from ..models.model_bh_graph_item_data import ModelBhGraphItemData
    from ..models.model_bh_graph_label import ModelBhGraphLabel
    from ..models.model_bh_graph_link_end import ModelBhGraphLinkEnd


T = TypeVar("T", bound="ModelBhGraphEdge")


@_attrs_define
class ModelBhGraphEdge:
    """
    Attributes:
        color (Union[Unset, str]):
        fade (Union[Unset, bool]):
        data (Union[Unset, ModelBhGraphItemData]):
        glyphs (Union[Unset, List['ModelBhGraphGlyph']]):
        end1 (Union[Unset, ModelBhGraphLinkEnd]):
        end2 (Union[Unset, ModelBhGraphLinkEnd]):
        flow (Union[Unset, ModelBhGraphEdgeFlow]):
        id1 (Union[Unset, str]):
        id2 (Union[Unset, str]):
        label (Union[Unset, ModelBhGraphLabel]):
        line_style (Union[Unset, str]):
        width (Union[Unset, int]):
    """

    color: Union[Unset, str] = UNSET
    fade: Union[Unset, bool] = UNSET
    data: Union[Unset, "ModelBhGraphItemData"] = UNSET
    glyphs: Union[Unset, List["ModelBhGraphGlyph"]] = UNSET
    end1: Union[Unset, "ModelBhGraphLinkEnd"] = UNSET
    end2: Union[Unset, "ModelBhGraphLinkEnd"] = UNSET
    flow: Union[Unset, "ModelBhGraphEdgeFlow"] = UNSET
    id1: Union[Unset, str] = UNSET
    id2: Union[Unset, str] = UNSET
    label: Union[Unset, "ModelBhGraphLabel"] = UNSET
    line_style: Union[Unset, str] = UNSET
    width: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        fade = self.fade

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        glyphs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.glyphs, Unset):
            glyphs = []
            for glyphs_item_data in self.glyphs:
                glyphs_item = glyphs_item_data.to_dict()
                glyphs.append(glyphs_item)

        end1: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end1, Unset):
            end1 = self.end1.to_dict()

        end2: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end2, Unset):
            end2 = self.end2.to_dict()

        flow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow, Unset):
            flow = self.flow.to_dict()

        id1 = self.id1

        id2 = self.id2

        label: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.label, Unset):
            label = self.label.to_dict()

        line_style = self.line_style

        width = self.width

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if fade is not UNSET:
            field_dict["fade"] = fade
        if data is not UNSET:
            field_dict["data"] = data
        if glyphs is not UNSET:
            field_dict["glyphs"] = glyphs
        if end1 is not UNSET:
            field_dict["end1"] = end1
        if end2 is not UNSET:
            field_dict["end2"] = end2
        if flow is not UNSET:
            field_dict["flow"] = flow
        if id1 is not UNSET:
            field_dict["id1"] = id1
        if id2 is not UNSET:
            field_dict["id2"] = id2
        if label is not UNSET:
            field_dict["label"] = label
        if line_style is not UNSET:
            field_dict["lineStyle"] = line_style
        if width is not UNSET:
            field_dict["width"] = width

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_bh_graph_edge_flow import ModelBhGraphEdgeFlow
        from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
        from ..models.model_bh_graph_item_data import ModelBhGraphItemData
        from ..models.model_bh_graph_label import ModelBhGraphLabel
        from ..models.model_bh_graph_link_end import ModelBhGraphLinkEnd

        d = src_dict.copy()
        color = d.pop("color", UNSET)

        fade = d.pop("fade", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, ModelBhGraphItemData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = ModelBhGraphItemData.from_dict(_data)

        glyphs = []
        _glyphs = d.pop("glyphs", UNSET)
        for glyphs_item_data in _glyphs or []:
            glyphs_item = ModelBhGraphGlyph.from_dict(glyphs_item_data)

            glyphs.append(glyphs_item)

        _end1 = d.pop("end1", UNSET)
        end1: Union[Unset, ModelBhGraphLinkEnd]
        if isinstance(_end1, Unset):
            end1 = UNSET
        else:
            end1 = ModelBhGraphLinkEnd.from_dict(_end1)

        _end2 = d.pop("end2", UNSET)
        end2: Union[Unset, ModelBhGraphLinkEnd]
        if isinstance(_end2, Unset):
            end2 = UNSET
        else:
            end2 = ModelBhGraphLinkEnd.from_dict(_end2)

        _flow = d.pop("flow", UNSET)
        flow: Union[Unset, ModelBhGraphEdgeFlow]
        if isinstance(_flow, Unset):
            flow = UNSET
        else:
            flow = ModelBhGraphEdgeFlow.from_dict(_flow)

        id1 = d.pop("id1", UNSET)

        id2 = d.pop("id2", UNSET)

        _label = d.pop("label", UNSET)
        label: Union[Unset, ModelBhGraphLabel]
        if isinstance(_label, Unset):
            label = UNSET
        else:
            label = ModelBhGraphLabel.from_dict(_label)

        line_style = d.pop("lineStyle", UNSET)

        width = d.pop("width", UNSET)

        model_bh_graph_edge = cls(
            color=color,
            fade=fade,
            data=data,
            glyphs=glyphs,
            end1=end1,
            end2=end2,
            flow=flow,
            id1=id1,
            id2=id2,
            label=label,
            line_style=line_style,
            width=width,
        )

        model_bh_graph_edge.additional_properties = d
        return model_bh_graph_edge

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
