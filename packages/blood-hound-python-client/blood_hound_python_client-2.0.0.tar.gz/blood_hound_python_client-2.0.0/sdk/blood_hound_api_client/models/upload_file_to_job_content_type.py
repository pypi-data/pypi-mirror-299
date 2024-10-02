from enum import Enum


class UploadFileToJobContentType(str, Enum):
    APPLICATIONJSON = "application/json"
    APPLICATIONX_ZIP_COMPRESSED = "application/x-zip-compressed"
    APPLICATIONZIP = "application/zip"
    APPLICATIONZIP_COMPRESSED = "application/zip-compressed"

    def __str__(self) -> str:
        return str(self.value)
