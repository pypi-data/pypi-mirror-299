from __future__ import annotations
from typing import TYPE_CHECKING


import requests



if TYPE_CHECKING:
    from mlx.models.api_response import ApiResponse


class MultiloginApiError(Exception):
    api_response: ApiResponse | None

    def __init__(self, api_response: ApiResponse):
        self.api_response = api_response

    @staticmethod
    def from_exc(exc):
        match type(exc):
            case requests.HTTPError:
                if exc.response.status_code in [401, 403]:
                    return AuthenticationError(exc)
                elif exc.response.status_code in [400,500]:
                    # TODO: impleemnt the CORE_DOWNLOAD_ALREADY_STARTED or something
                    pass
                return CoreDownloadAlreadyStarted(exc)
            case _:
                pass
        return exc



class AuthenticationError(MultiloginApiError):
    pass


class CoreDownloadAlreadyStarted(MultiloginApiError):
    pass
