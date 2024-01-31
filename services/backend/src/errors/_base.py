from typing import Any, Dict
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from src.utils.logger import logger


class Errors(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code, HTTPDetail(message=message, data=data).dict(), headers
        )
        self.__log(message)

    def __log(self, message: str):
        logger.info(
            "http exception", error_message=message, status_code=self.status_code
        )


class HTTPDetail(BaseModel):
    message: str
    data: Dict[str, Any]
