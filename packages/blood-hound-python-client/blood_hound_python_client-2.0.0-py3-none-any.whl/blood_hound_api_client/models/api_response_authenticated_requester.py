from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_client import ModelClient
    from ..models.model_user import ModelUser


T = TypeVar("T", bound="ApiResponseAuthenticatedRequester")


@_attrs_define
class ApiResponseAuthenticatedRequester:
    """
    Attributes:
        data (Union['ModelClient', 'ModelUser', Unset]):
    """

    data: Union["ModelClient", "ModelUser", Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.model_user import ModelUser

        data: Union[Dict[str, Any], Unset]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, ModelUser):
            data = self.data.to_dict()
        else:
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_client import ModelClient
        from ..models.model_user import ModelUser

        d = src_dict.copy()

        def _parse_data(data: object) -> Union["ModelClient", "ModelUser", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = ModelUser.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            data_type_1 = ModelClient.from_dict(data)

            return data_type_1

        data = _parse_data(d.pop("data", UNSET))

        api_response_authenticated_requester = cls(
            data=data,
        )

        api_response_authenticated_requester.additional_properties = d
        return api_response_authenticated_requester

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
