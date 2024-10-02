import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelSamlProvider")


@_attrs_define
class ModelSamlProvider:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        name (Union[Unset, str]):
        display_name (Union[Unset, str]):
        idp_issuer_uri (Union[Unset, str]):
        idp_sso_uri (Union[Unset, str]):
        principal_attribute_mappings (Union[Unset, List[str]]):
        sp_issuer_uri (Union[Unset, str]):
        sp_sso_uri (Union[Unset, str]):
        sp_metadata_uri (Union[Unset, str]):
        sp_acs_uri (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    idp_issuer_uri: Union[Unset, str] = UNSET
    idp_sso_uri: Union[Unset, str] = UNSET
    principal_attribute_mappings: Union[Unset, List[str]] = UNSET
    sp_issuer_uri: Union[Unset, str] = UNSET
    sp_sso_uri: Union[Unset, str] = UNSET
    sp_metadata_uri: Union[Unset, str] = UNSET
    sp_acs_uri: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        deleted_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.to_dict()

        name = self.name

        display_name = self.display_name

        idp_issuer_uri = self.idp_issuer_uri

        idp_sso_uri = self.idp_sso_uri

        principal_attribute_mappings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.principal_attribute_mappings, Unset):
            principal_attribute_mappings = self.principal_attribute_mappings

        sp_issuer_uri = self.sp_issuer_uri

        sp_sso_uri = self.sp_sso_uri

        sp_metadata_uri = self.sp_metadata_uri

        sp_acs_uri = self.sp_acs_uri

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if idp_issuer_uri is not UNSET:
            field_dict["idp_issuer_uri"] = idp_issuer_uri
        if idp_sso_uri is not UNSET:
            field_dict["idp_sso_uri"] = idp_sso_uri
        if principal_attribute_mappings is not UNSET:
            field_dict["principal_attribute_mappings"] = principal_attribute_mappings
        if sp_issuer_uri is not UNSET:
            field_dict["sp_issuer_uri"] = sp_issuer_uri
        if sp_sso_uri is not UNSET:
            field_dict["sp_sso_uri"] = sp_sso_uri
        if sp_metadata_uri is not UNSET:
            field_dict["sp_metadata_uri"] = sp_metadata_uri
        if sp_acs_uri is not UNSET:
            field_dict["sp_acs_uri"] = sp_acs_uri

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.null_time import NullTime

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _deleted_at = d.pop("deleted_at", UNSET)
        deleted_at: Union[Unset, NullTime]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = NullTime.from_dict(_deleted_at)

        name = d.pop("name", UNSET)

        display_name = d.pop("display_name", UNSET)

        idp_issuer_uri = d.pop("idp_issuer_uri", UNSET)

        idp_sso_uri = d.pop("idp_sso_uri", UNSET)

        principal_attribute_mappings = cast(List[str], d.pop("principal_attribute_mappings", UNSET))

        sp_issuer_uri = d.pop("sp_issuer_uri", UNSET)

        sp_sso_uri = d.pop("sp_sso_uri", UNSET)

        sp_metadata_uri = d.pop("sp_metadata_uri", UNSET)

        sp_acs_uri = d.pop("sp_acs_uri", UNSET)

        model_saml_provider = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            name=name,
            display_name=display_name,
            idp_issuer_uri=idp_issuer_uri,
            idp_sso_uri=idp_sso_uri,
            principal_attribute_mappings=principal_attribute_mappings,
            sp_issuer_uri=sp_issuer_uri,
            sp_sso_uri=sp_sso_uri,
            sp_metadata_uri=sp_metadata_uri,
            sp_acs_uri=sp_acs_uri,
        )

        model_saml_provider.additional_properties = d
        return model_saml_provider

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
