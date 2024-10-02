from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_asset_group_selector_spec_action import ModelAssetGroupSelectorSpecAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelAssetGroupSelectorSpec")


@_attrs_define
class ModelAssetGroupSelectorSpec:
    """
    Attributes:
        selector_name (Union[Unset, str]):
        sid (Union[Unset, str]):
        action (Union[Unset, ModelAssetGroupSelectorSpecAction]):
    """

    selector_name: Union[Unset, str] = UNSET
    sid: Union[Unset, str] = UNSET
    action: Union[Unset, ModelAssetGroupSelectorSpecAction] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        selector_name = self.selector_name

        sid = self.sid

        action: Union[Unset, str] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if selector_name is not UNSET:
            field_dict["selector_name"] = selector_name
        if sid is not UNSET:
            field_dict["sid"] = sid
        if action is not UNSET:
            field_dict["action"] = action

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        selector_name = d.pop("selector_name", UNSET)

        sid = d.pop("sid", UNSET)

        _action = d.pop("action", UNSET)
        action: Union[Unset, ModelAssetGroupSelectorSpecAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = ModelAssetGroupSelectorSpecAction(_action)

        model_asset_group_selector_spec = cls(
            selector_name=selector_name,
            sid=sid,
            action=action,
        )

        model_asset_group_selector_spec.additional_properties = d
        return model_asset_group_selector_spec

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
