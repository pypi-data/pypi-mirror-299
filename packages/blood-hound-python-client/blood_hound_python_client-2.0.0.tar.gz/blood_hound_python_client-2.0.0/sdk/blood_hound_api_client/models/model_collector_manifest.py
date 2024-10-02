from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_collector_version import ModelCollectorVersion


T = TypeVar("T", bound="ModelCollectorManifest")


@_attrs_define
class ModelCollectorManifest:
    """
    Attributes:
        latest (Union[Unset, str]):
        versions (Union[Unset, List['ModelCollectorVersion']]):
    """

    latest: Union[Unset, str] = UNSET
    versions: Union[Unset, List["ModelCollectorVersion"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        latest = self.latest

        versions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()
                versions.append(versions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if latest is not UNSET:
            field_dict["latest"] = latest
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_collector_version import ModelCollectorVersion

        d = src_dict.copy()
        latest = d.pop("latest", UNSET)

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = ModelCollectorVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        model_collector_manifest = cls(
            latest=latest,
            versions=versions,
        )

        model_collector_manifest.additional_properties = d
        return model_collector_manifest

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
