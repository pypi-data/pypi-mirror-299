from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
import json
import requests
import uuid
from typing import (
    Any,
    BinaryIO,
    Dict,
    Generic,
    Iterator,
    Optional,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
    TYPE_CHECKING,
)
from typing_extensions import NotRequired, Self
from urllib.parse import urlencode
import urllib3

from .exception import MissingClientException
from .utils import to_datetime

if TYPE_CHECKING:  # pragma: no cover
    from .auth_client import AuthClient
    from .dataset_client import DatasetClient


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------


DEFAULT_CHUNK_SIZE = 50

# ------------------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------------------


class AccessLevel(Enum):
    """
    The access level of an account

    Attributes:
        EXTERNAL  enum value for an external user
        INTERNAL  enum value for an internal user with a @npolar.no email address
        ADMIN     enum value for an admin user
    """

    EXTERNAL = "external"
    INTERNAL = "internal"
    ADMIN = "admin"


class DatasetType(Enum):
    """
    The type of a dataset

    Attributes:
        DRAFT     enum value for a draft dataset. It can be made internal or
                  public in the frontend
        INTERNAL  enum value for an internal dataset
        PUBLIC    enum value for a public dataset
    """

    DRAFT = "draft"
    INTERNAL = "internal"
    PUBLIC = "public"


# ------------------------------------------------------------------------------
# Type aliases
# ------------------------------------------------------------------------------


Content = Dict[str, Any]


# ------------------------------------------------------------------------------
# API Responses (TypedDict)
# ------------------------------------------------------------------------------


class AccountAPIResponse(TypedDict):
    id: str
    email: str
    accessLevel: AccessLevel
    directoryUser: bool


class AccountWithTokenAPIResponse(AccountAPIResponse):
    token: str


class KeepaliveAPIResponse(TypedDict):
    token: str


class PermissionAPIResponse(TypedDict):
    objectId: str
    userId: str
    mayDelete: bool
    mayRead: bool
    mayUpdate: bool


class BaseModelAPIResponse(TypedDict):
    created: str
    createdBy: str
    id: str
    modified: str
    modifiedBy: str
    permissions: PermissionAPIResponse


class AttachmentAPIResponse(BaseModelAPIResponse):
    byteSize: int
    datasetId: str
    description: str
    filename: str
    mimeType: str
    prefix: str
    released: str
    sha256: str
    title: str


class DatasetAPIResponse(BaseModelAPIResponse):
    content: Content
    doi: Union[str, None]
    published: str
    publishedBy: str
    type: str


class RecordAPIResponse(BaseModelAPIResponse):
    content: Content
    datasetId: str
    parentId: Union[str, None]
    type: str


class RecordInfoAPIResponse(TypedDict):
    id: str
    statusCode: int


class UploadInfoAPIResponse(TypedDict):
    id: str
    fileName: str
    sha256: str


# ------------------------------------------------------------------------------
# Account and auth models
# ------------------------------------------------------------------------------


class Account:
    """
    A basic account object.

    Attributes:
        raw (AccountAPIResponse): The API response data parsed from JSON
        client (AuthClient | None): The client for the auth module
    """

    client: Optional[AuthClient]
    access_level: AccessLevel
    directory_user: bool
    email: str
    id: str

    def __init__(
        self, raw: AccountAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of the Account model class.

        Args:
            raw (AccountAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """
        self.client = client
        self.access_level = AccessLevel(raw["accessLevel"])
        self.directory_user = raw.get("directoryUser", False)
        self.email = raw["email"]
        self.id = raw["id"]


class AuthContainer:
    """
    A container that can be used for authentification.

    Attributes:
        token (str): the auth token used for authentification

    """

    token: str

    def __init__(self, token: str) -> None:
        """
        Initialize an instance of the AuthContainer class.

        Args:
            token (str): the auth token used for authentification
        """
        self.token = token

    @property
    def headers(self) -> dict[str, str]:
        """
        Retreive the header(s) for an authorized HTTP request

        Returns:
            dict[str, str]: The auth headers
        """
        return {"Authorization": f"Bearer {self.token}"}


class AccountWithToken(AuthContainer, Account):
    """
    A logged in account with token. Inherits from AuthContainer and Account

    Attributes:
        raw (AccountWithTokenAPIResponse): The API response data parsed from JSON
        client (AuthClient | None): The client for the auth module
    """

    raw: AccountWithTokenAPIResponse

    def __init__(
        self, raw: AccountWithTokenAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of the AccountWithToken model class.

        Args:
            raw (AccountWithTokenAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """

        Account.__init__(self, raw, client=client)
        AuthContainer.__init__(self, raw["token"])


# ------------------------------------------------------------------------------
# Permission model
# ------------------------------------------------------------------------------


class Permission:
    object_id: str
    user_id: Optional[str]
    may_read: bool
    may_update: bool
    may_delete: bool

    def __init__(self, raw: PermissionAPIResponse):
        """
        Initialize an instance of a Permission.

        Args:
            raw (PermissionAPIResponse): The API response as parsed JSON
        """

        self.object_id = raw["objectId"]
        self.user_id = raw.get("userId")
        self.may_read = raw["mayRead"]
        self.may_update = raw["mayUpdate"]
        self.may_delete = raw["mayDelete"]


# ------------------------------------------------------------------------------
# Generic data models
# ------------------------------------------------------------------------------

R = TypeVar("R", AttachmentAPIResponse, DatasetAPIResponse, RecordAPIResponse)


class Model(Generic[R], ABC):
    """
    A single Model as Dataset or Attachment, that has been retrieved using the
    DatasetClient.

    Attributes:
        client (DatasetClient | None) The client for the dataset module
    """

    client: Optional[DatasetClient]

    created: Optional[datetime]
    created_by: str
    id: str
    modified: Optional[datetime]
    modified_by: str
    permissions: Optional[Permission]

    def __init__(self, raw: R, *, client: Optional[DatasetClient] = None):
        """
        Initialize an instance of a model class as Dataset or Attachment.

        Args:
            raw (R): The API response as parsed JSON
            client (DatasetClient): The used dataset client
        """

        self.client = client

        self.created = to_datetime(raw["created"])
        self.created_by = raw["createdBy"]
        self.id = raw["id"]
        self.modified = to_datetime(raw["modified"])
        self.modified_by = raw["modifiedBy"]
        if "permissions" in raw:
            self.permissions = Permission(raw["permissions"])


class Attachment(Model[AttachmentAPIResponse]):
    """
    The metadata of a single Attachment retrieved from the NPDC dataset module.
    """

    byte_size: int
    dataset_id: str
    description: str
    filename: str
    mime_type: str
    prefix: str
    released: Optional[datetime]
    sha256: str
    title: str

    def __init__(
        self, raw: AttachmentAPIResponse, *, client: Optional[DatasetClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.byte_size = raw["byteSize"]
        self.dataset_id = raw["datasetId"]
        self.description = raw["description"]
        self.filename = raw["filename"]
        self.mime_type = raw["mimeType"]
        self.prefix = raw["prefix"]
        self.released = to_datetime(raw["released"])
        self.sha256 = raw["sha256"]
        self.title = raw["title"]

    def reader(self) -> urllib3.response.HTTPResponse:
        """
        Retrieve a reader to stream the attachment content.

        This is a shortcut for DatasetClient.get_attachment_reader.

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            urllib3.response.HTTPResponse: a response object with read access to
                the body

        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_attachment_reader(self.dataset_id, self.id)


class Dataset(Model[DatasetAPIResponse]):
    """
    The metadata of a single Dataset retrieved from the NPDC dataset module.

    The user generated metadata as dataset title, geographical information,
    contributors or timeframes are found in the content property.
    """

    content: Content
    doi: Optional[str]
    published: Optional[datetime]
    published_by: Optional[str] = None
    type: DatasetType

    def __init__(
        self, raw: DatasetAPIResponse, *, client: Optional[DatasetClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.content = raw["content"]
        self.doi = raw["doi"]
        self.published = to_datetime(raw["published"])
        self.type = DatasetType(raw["type"])

        published_by = raw["publishedBy"]
        if published_by != "":
            self.published_by = published_by

    def get_attachments(self, **query: Any) -> "AttachmentCollection":
        """
        Retrieve attachment metadata filtered by query for the dataset.

        This is a shortcut for DatasetClient.get_attachments.

        Args:
            query (dict): optional query parameters for filtering

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            AttachmentCollection: a lazy collection of attachments
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_attachments(self.id, **query)

    def get_records(self, **query: Any) -> "RecordCollection":
        """
        Retrieve records by query for the dataset.

        This is a shortcut for DatasetClient.get_records.

        Args:
            query (dict): optional query parameters for filtering

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            RecordCollection: a lazy collection of records
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_records(self.id, **query)

    def download_attachments_as_zip(self, target_dir: str) -> str:
        """
        Download all dataset attachments as a zip file.

        This is a shortcut for DatasetClient.download_attachments_as_zip.

        Args:
            target_dir (str): the target directory where the ZIP file should be
                saved.

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            str: The path of the downloaded ZIP file
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.download_attachments_as_zip(self.id, target_dir)


class Record(Model[RecordAPIResponse]):
    """
    The metadata of a single record retrieved from the NPDC dataset module.
    """

    content: Content
    dataset_id: str
    id: str
    parent_id: str | None = None
    type: str

    def __init__(
        self, raw: RecordAPIResponse, *, client: Optional[DatasetClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.content = raw["content"]
        self.dataset_id = raw["datasetId"]
        self.id = raw["id"]
        if "parentId" in raw:
            self.parent_id = raw["parentId"]
        self.type = raw["type"]


# ------------------------------------------------------------------------------
# Queries
# ------------------------------------------------------------------------------

AttachmentQuery = TypedDict(
    "AttachmentQuery",
    {
        # see https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetID__attachment_
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
        "q": NotRequired[str],
        "prefix": NotRequired[str],  # starts and ends with /
        "recursive": NotRequired[bool],
        "from": NotRequired[date],
        "until": NotRequired[date],
    },
)


DatasetQuery = TypedDict(
    "DatasetQuery",
    {
        # see https://beta.data.npolar.no/-/docs/dataset/#/dataset/get_dataset_
        "q": NotRequired[str],
        "location": NotRequired[str],  # WTF format
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
        "type": NotRequired[DatasetType],
        "from": NotRequired[date],
        "until": NotRequired[date],
    },
)


RecordQuery = TypedDict(
    "RecordQuery",
    {
        # https://beta.data.npolar.no/-/docs/dataset/#/record/get_dataset__datasetID__record_
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
    },
)

Q = TypeVar("Q", AttachmentQuery, DatasetQuery, RecordQuery)


class QuerySerializer(Generic[Q], ABC):
    @abstractmethod
    def prepare(self, query: Q) -> dict[str, Any]:
        kv = {**query}

        if query.get("count"):
            kv["count"] = "true"
        else:
            kv.pop("count", False)

        return kv

    def __call__(self, query: Q) -> str:
        if len(query) == 0:
            return ""
        return "?" + urlencode(self.prepare(query))


class AttachmentQuerySerializer(QuerySerializer[AttachmentQuery]):
    def prepare(self, query: AttachmentQuery) -> dict[str, Any]:
        kv = super().prepare(query)

        if query.get("recursive"):
            kv["recursive"] = "true"
        else:
            kv.pop("recursive", False)

        if query.get("from"):
            kv["from"] = query["from"].isoformat()

        if query.get("until"):
            kv["until"] = query["until"].isoformat()

        return kv


class DatasetQuerySerializer(QuerySerializer[DatasetQuery]):
    def prepare(self, query: DatasetQuery) -> dict[str, Any]:
        kv = super().prepare(query)

        if query.get("type"):
            kv["type"] = query["type"].value

        if query.get("from"):
            kv["from"] = query["from"].isoformat()

        if query.get("until"):
            kv["until"] = query["until"].isoformat()

        return kv


class RecordQuerySerializer(QuerySerializer[RecordQuery]):
    def prepare(self, query: RecordQuery) -> dict[str, Any]:
        kv = super().prepare(query)
        return kv


QS = TypeVar(
    "QS", AttachmentQuerySerializer, DatasetQuerySerializer, RecordQuerySerializer
)

# ------------------------------------------------------------------------------
# Collections
# ------------------------------------------------------------------------------

T = TypeVar("T", Attachment, Dataset, Record)


class LazyCollection(Generic[T, Q, QS], ABC):
    chunk_size: int
    client: DatasetClient
    model_class: type[T]
    _generator: Iterator[T]
    # request
    query_serializer: QS
    query: Q
    # response
    count: int | None = None

    def __init__(
        self,
        *,
        client: DatasetClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: Q,
    ) -> None:
        if chunk_size < 1 or chunk_size > 255:
            raise ValueError("Chunk size have to be between 1 and 255")

        self.client = client
        self.chunk_size = chunk_size
        self.query = query
        self._generator = self._generate()

    @property
    @abstractmethod
    def _endpoint(self) -> str:
        pass

    def _request(self, query: Q) -> requests.Response:
        # TODO: fix typing issue and remove type:ignore flag
        url = self._endpoint + self.query_serializer(query)  # type:ignore
        return self.client._exec_request("GET", url)

    def _generate(self) -> Iterator[T]:
        skip = self.query.get("skip", 0)
        take = self.query.get("take")  # if not set, fetch all items
        fetch_count = self.query.get("count")
        chunk_size = self.chunk_size
        if take is not None and take < chunk_size:
            chunk_size = take

        query = self.query.copy()
        query["take"] = chunk_size
        query["skip"] = skip

        c = 0
        while True:
            resp = self._request(query)
            raw = resp.json()

            if fetch_count:
                self.count = raw["count"]
                fetch_count = None

            items = raw["items"]
            for data in items:
                yield self.model_class(data, client=self.client)
                c += 1
                if take is not None and c >= take:
                    return  # data complete

            if len(items) < chunk_size:
                break  # no more chunks

            query["skip"] += query["take"]

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        return next(self._generator)


class AttachmentCollection(
    LazyCollection[Attachment, AttachmentQuery, AttachmentQuerySerializer]
):
    """
    A generator to retrieve Attachment models in a lazy way.

    LazyCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        dataset_id (str): the ID of the dataset the attachment is related to
        client (DatasetClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetId__attachment_
    """

    model_class = Attachment

    def __init__(
        self,
        dataset_id: str,
        *,
        client: DatasetClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: AttachmentQuery,
    ) -> None:
        super().__init__(client=client, chunk_size=chunk_size, query=query)
        self.dataset_id = dataset_id
        self.query_serializer = AttachmentQuerySerializer()

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/{self.dataset_id}/attachment/"


class DatasetCollection(LazyCollection[Dataset, DatasetQuery, DatasetQuerySerializer]):
    """
    A generator to retrieve Dataset models in a lazy way.

    LazyCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DatasetClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/dataset/get_dataset_
    """

    model_class = Dataset

    def __init__(
        self,
        *,
        client: DatasetClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: DatasetQuery,
    ) -> None:
        super().__init__(client=client, chunk_size=chunk_size, query=query)
        self.query_serializer = DatasetQuerySerializer()

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/"


class PermissionCollection:
    def __init__(self, raw_permission_list: list[PermissionAPIResponse]) -> None:
        self._generator = iter(raw_permission_list)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Permission:
        return Permission(next(self._generator))


class RecordCollection(LazyCollection[Record, RecordQuery, RecordQuerySerializer]):
    """
    A generator to retrieve Record models in a lazy way.

    RecordCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DatasetClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/record/get_dataset__datasetID__record_
    """

    model_class = Record

    def __init__(
        self,
        dataset_id: str,
        *,
        client: DatasetClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: RecordQuery,
    ) -> None:
        super().__init__(client=client, chunk_size=chunk_size, query=query)
        self.dataset_id = dataset_id
        self.query_serializer = RecordQuerySerializer()

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/{self.dataset_id}/record/"


# ------------------------------------------------------------------------------
# Attachment DTOs
# ------------------------------------------------------------------------------


class AttachmentCreateDTO:
    description: str | None
    filename: str
    mime_type: str
    reader: BinaryIO
    title: str | None

    """
    A file upload containing a reader to retrieve the content as well as
    metadata.

    Attributes:
        reader (BinaryIO): a reader
        filename (str): the file name
        description (str | None): an optional description
        title (str | None): an optional title
        mime_type (str) the mime type (a.k.a. content type) of the file
    """

    def __init__(
        self,
        reader: BinaryIO,
        filename: str,
        description: Optional[str] = None,
        title: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> None:
        """
        Initialize an AttachmentCreateDTO instance

        Args:
            reader (BinaryIO): reader to fetch the data
            filename (str): the file name
            description (str | None): an optional description
            title (str | None): an optional title
            mime_type (str | None):
                the mime type (a.k.a. content type) of the file. When None it
                will be set to ""application/octet-stream"
        """

        self.reader = reader
        self.filename = filename
        self.description = description
        self.title = title
        if mime_type is None:
            self.mime_type = "application/octet-stream"
        else:
            self.mime_type = mime_type

    def _get_multiparts(self) -> list[Tuple[Any, ...]]:
        data: list[Tuple[Any, ...]] = []

        if self.description is not None:
            data.append(
                ("description", self.description),
            )
        if self.title is not None:
            data.append(
                ("title", self.title),
            )
        # blob has to be the last tuple to add to the list
        data.append(
            ("blob", (self.filename, self.reader, self.mime_type)),
        )

        return data


class AttachmentCreationInfo:
    """
    Information of an uploaded attachment
    """

    id: str
    filename: str
    sha256: str

    def __init__(self, raw: UploadInfoAPIResponse) -> None:
        self.id = raw["id"]
        self.filename = raw["fileName"]
        self.sha256 = raw["sha256"]


# ------------------------------------------------------------------------------
# Record DTOs
# ------------------------------------------------------------------------------


class RecordCreateDTO:
    content: Content
    type: str
    id: str
    parent_id: Optional[str]

    """
    A record upload containing data and metadata for a record to add.

    Attributes:
        content (Content): the content of the record,
        type (str): the type of the content
        id (str): an optional UUID.
        parent_id (str): an optional parent record id
    """

    def __init__(
        self,
        content: Content,
        type: str,
        id: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> None:
        """
        Initialize a RecordCreateDTO instance

        Args:
            content (Content): the content of the record,
            type (str): the type of the content
            id (str): an optional UUID. A id be created when not provided here
            parent_id (str): an optional parent record id
        """

        self.content = content
        self.type = type
        if id is None:
            id = str(uuid.uuid4())
        self.id = id
        self.parent_id = parent_id


class RecordCreateDTOEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, RecordCreateDTO):
            return {
                "content": obj.content,
                "type": obj.type,
                "id": obj.id,
                "parentId": obj.parent_id,
            }
        return super().default(obj)  # pragma: no cover


class RecordCreationInfo:
    """
    Information of an added record
    """

    id: str
    status_code: int

    def __init__(self, raw: RecordInfoAPIResponse) -> None:
        self.id = raw["id"]
        self.status_code = raw["statusCode"]
