from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_user import ModelUser


T = TypeVar("T", bound="DeleteSamlProviderResponse200Data")


@_attrs_define
class DeleteSamlProviderResponse200Data:
    """
    Attributes:
        affected_user (Union[Unset, List['ModelUser']]):
    """

    affected_user: Union[Unset, List["ModelUser"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        affected_user: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.affected_user, Unset):
            affected_user = []
            for affected_user_item_data in self.affected_user:
                affected_user_item = affected_user_item_data.to_dict()
                affected_user.append(affected_user_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if affected_user is not UNSET:
            field_dict["affected_user"] = affected_user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_user import ModelUser

        d = src_dict.copy()
        affected_user = []
        _affected_user = d.pop("affected_user", UNSET)
        for affected_user_item_data in _affected_user or []:
            affected_user_item = ModelUser.from_dict(affected_user_item_data)

            affected_user.append(affected_user_item)

        delete_saml_provider_response_200_data = cls(
            affected_user=affected_user,
        )

        delete_saml_provider_response_200_data.additional_properties = d
        return delete_saml_provider_response_200_data

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
