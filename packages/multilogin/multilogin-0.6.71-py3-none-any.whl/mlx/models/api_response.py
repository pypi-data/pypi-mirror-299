from pydantic import BaseModel
from typing import Dict, Optional, Any
import requests

from mlx.exceptions import AuthenticationError


class ApiResponseStatus(BaseModel):
    error_code: Optional[str] = ""  # Multilogin ERROR code
    http_code: Optional[int] = None  # HTTP status code
    message: Optional[str] = ""


class ApiResponse(BaseModel):
    status: ApiResponseStatus
    data: Optional[Dict[str, Any] | list] = None

    _response: requests.Response

    @property
    def response(self):
        return self._response

    @property
    def request(self):
        return self._response.request

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def text(self):
        return self._response.text

    def raise_for_status(self):
        from mlx.exceptions import MultiloginApiError

        try:
            self._response.raise_for_status()
        except requests.HTTPError as e:
            # We only handle HTTPErorr as anything else is not application related
            raise MultiloginApiError.from_exc(e)

    @classmethod
    def from_response(cls, response: requests.Response):
        try:
            obj = cls.parse_raw(response._content)
        except Exception as e:
            breakpoint()
            a = 1
            # Return deafult
            # FIXME: This shouldn't happen

        obj._response = response
        return obj
