from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="CreateSamlProviderBody")


@_attrs_define
class CreateSamlProviderBody:
    """
    Attributes:
        name (Union[Unset, str]): Name of the new SAML provider.
        metadata (Union[Unset, File]): Metadata XML file.
    """

    name: Union[Unset, str] = UNSET
    metadata: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        metadata: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        metadata: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, File]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = File(payload=BytesIO(_metadata))

        create_saml_provider_body = cls(
            name=name,
            metadata=metadata,
        )

        create_saml_provider_body.additional_properties = d
        return create_saml_provider_body

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
