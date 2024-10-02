from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_client_error_body_additional import LogClientErrorBodyAdditional


T = TypeVar("T", bound="LogClientErrorBody")


@_attrs_define
class LogClientErrorBody:
    """
    Attributes:
        task_error (Union[Unset, str]):
        additional (Union[Unset, LogClientErrorBodyAdditional]):
    """

    task_error: Union[Unset, str] = UNSET
    additional: Union[Unset, "LogClientErrorBodyAdditional"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task_error = self.task_error

        additional: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.additional, Unset):
            additional = self.additional.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if task_error is not UNSET:
            field_dict["task_error"] = task_error
        if additional is not UNSET:
            field_dict["additional"] = additional

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_client_error_body_additional import LogClientErrorBodyAdditional

        d = src_dict.copy()
        task_error = d.pop("task_error", UNSET)

        _additional = d.pop("additional", UNSET)
        additional: Union[Unset, LogClientErrorBodyAdditional]
        if isinstance(_additional, Unset):
            additional = UNSET
        else:
            additional = LogClientErrorBodyAdditional.from_dict(_additional)

        log_client_error_body = cls(
            task_error=task_error,
            additional=additional,
        )

        log_client_error_body.additional_properties = d
        return log_client_error_body

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
