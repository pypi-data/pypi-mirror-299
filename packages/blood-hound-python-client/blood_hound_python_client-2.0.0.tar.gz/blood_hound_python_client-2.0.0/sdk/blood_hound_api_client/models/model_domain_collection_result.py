import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelDomainCollectionResult")


@_attrs_define
class ModelDomainCollectionResult:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        job_id (Union[Unset, int]):
        domain_name (Union[Unset, str]): Name of the domain that was enumerated
        success (Union[Unset, bool]): A boolean value indicating whether the domain enumeration succeeded
        message (Union[Unset, str]): A status message for a domain enumeration result
        user_count (Union[Unset, int]): A count of users enumerated
        group_count (Union[Unset, int]): A count of groups enumerated
        computer_count (Union[Unset, int]): A count of computers enumerated
        gpo_count (Union[Unset, int]): A count of gpos enumerated
        ou_count (Union[Unset, int]): A count of ous enumerated
        container_count (Union[Unset, int]): A count of containers enumerated
        aiaca_count (Union[Unset, int]): A count of aiacas enumerated
        rootca_count (Union[Unset, int]): A count of rootcas enumerated
        enterpriseca_count (Union[Unset, int]): A count of enterprisecas enumerated
        ntauthstore_count (Union[Unset, int]): A count of ntauthstores enumerated
        certtemplate_count (Union[Unset, int]): A count of certtemplates enumerated
        deleted_count (Union[Unset, int]): A count of deleted objects enumerated
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    job_id: Union[Unset, int] = UNSET
    domain_name: Union[Unset, str] = UNSET
    success: Union[Unset, bool] = UNSET
    message: Union[Unset, str] = UNSET
    user_count: Union[Unset, int] = UNSET
    group_count: Union[Unset, int] = UNSET
    computer_count: Union[Unset, int] = UNSET
    gpo_count: Union[Unset, int] = UNSET
    ou_count: Union[Unset, int] = UNSET
    container_count: Union[Unset, int] = UNSET
    aiaca_count: Union[Unset, int] = UNSET
    rootca_count: Union[Unset, int] = UNSET
    enterpriseca_count: Union[Unset, int] = UNSET
    ntauthstore_count: Union[Unset, int] = UNSET
    certtemplate_count: Union[Unset, int] = UNSET
    deleted_count: Union[Unset, int] = UNSET
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

        job_id = self.job_id

        domain_name = self.domain_name

        success = self.success

        message = self.message

        user_count = self.user_count

        group_count = self.group_count

        computer_count = self.computer_count

        gpo_count = self.gpo_count

        ou_count = self.ou_count

        container_count = self.container_count

        aiaca_count = self.aiaca_count

        rootca_count = self.rootca_count

        enterpriseca_count = self.enterpriseca_count

        ntauthstore_count = self.ntauthstore_count

        certtemplate_count = self.certtemplate_count

        deleted_count = self.deleted_count

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
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if domain_name is not UNSET:
            field_dict["domain_name"] = domain_name
        if success is not UNSET:
            field_dict["success"] = success
        if message is not UNSET:
            field_dict["message"] = message
        if user_count is not UNSET:
            field_dict["user_count"] = user_count
        if group_count is not UNSET:
            field_dict["group_count"] = group_count
        if computer_count is not UNSET:
            field_dict["computer_count"] = computer_count
        if gpo_count is not UNSET:
            field_dict["gpo_count"] = gpo_count
        if ou_count is not UNSET:
            field_dict["ou_count"] = ou_count
        if container_count is not UNSET:
            field_dict["container_count"] = container_count
        if aiaca_count is not UNSET:
            field_dict["aiaca_count"] = aiaca_count
        if rootca_count is not UNSET:
            field_dict["rootca_count"] = rootca_count
        if enterpriseca_count is not UNSET:
            field_dict["enterpriseca_count"] = enterpriseca_count
        if ntauthstore_count is not UNSET:
            field_dict["ntauthstore_count"] = ntauthstore_count
        if certtemplate_count is not UNSET:
            field_dict["certtemplate_count"] = certtemplate_count
        if deleted_count is not UNSET:
            field_dict["deleted_count"] = deleted_count

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

        job_id = d.pop("job_id", UNSET)

        domain_name = d.pop("domain_name", UNSET)

        success = d.pop("success", UNSET)

        message = d.pop("message", UNSET)

        user_count = d.pop("user_count", UNSET)

        group_count = d.pop("group_count", UNSET)

        computer_count = d.pop("computer_count", UNSET)

        gpo_count = d.pop("gpo_count", UNSET)

        ou_count = d.pop("ou_count", UNSET)

        container_count = d.pop("container_count", UNSET)

        aiaca_count = d.pop("aiaca_count", UNSET)

        rootca_count = d.pop("rootca_count", UNSET)

        enterpriseca_count = d.pop("enterpriseca_count", UNSET)

        ntauthstore_count = d.pop("ntauthstore_count", UNSET)

        certtemplate_count = d.pop("certtemplate_count", UNSET)

        deleted_count = d.pop("deleted_count", UNSET)

        model_domain_collection_result = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            job_id=job_id,
            domain_name=domain_name,
            success=success,
            message=message,
            user_count=user_count,
            group_count=group_count,
            computer_count=computer_count,
            gpo_count=gpo_count,
            ou_count=ou_count,
            container_count=container_count,
            aiaca_count=aiaca_count,
            rootca_count=rootca_count,
            enterpriseca_count=enterpriseca_count,
            ntauthstore_count=ntauthstore_count,
            certtemplate_count=certtemplate_count,
            deleted_count=deleted_count,
        )

        model_domain_collection_result.additional_properties = d
        return model_domain_collection_result

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
