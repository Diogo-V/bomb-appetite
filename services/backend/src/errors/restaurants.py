from typing import Any, Dict
from fastapi import status

from src.errors._base import Errors


class RestaurantNotFound(Errors):
    def __init__(
        self,
        message: str = "Restaurant not found",
        data: Dict[str, Any] = {},
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, message, data, None)
