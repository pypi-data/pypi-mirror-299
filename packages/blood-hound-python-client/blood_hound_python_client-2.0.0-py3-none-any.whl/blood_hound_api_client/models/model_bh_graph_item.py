from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
    from ..models.model_bh_graph_item_data import ModelBhGraphItemData


T = TypeVar("T", bound="ModelBhGraphItem")


@_attrs_define
class ModelBhGraphItem:
    """
    Attributes:
        color (Union[Unset, str]):
        fade (Union[Unset, bool]):
        data (Union[Unset, ModelBhGraphItemData]):
        glyphs (Union[Unset, List['ModelBhGraphGlyph']]):
    """

    color: Union[Unset, str] = UNSET
    fade: Union[Unset, bool] = UNSET
    data: Union[Unset, "ModelBhGraphItemData"] = UNSET
    glyphs: Union[Unset, List["ModelBhGraphGlyph"]] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
        from ..models.model_bh_graph_item_data import ModelBhGraphItemData

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

        model_bh_graph_item = cls(
            color=color,
            fade=fade,
            data=data,
            glyphs=glyphs,
        )

        model_bh_graph_item.additional_properties = d
        return model_bh_graph_item

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
