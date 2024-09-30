from __future__ import annotations
import logging
from typing import TypedDict

from mlx.api import Api
from mlx.models.profile import Profile
from mlx.config import config


class ProfileApi(Api):
    def get(self, id: str | None = None):
        if not id:
            return self.status()
        endpoint = f"{config.multilogin}/profile/statuses/{id}"
        return self.session.request("get", endpoint)

    def status(self, *args, **kwargs) -> ProfileStateResponse:
        """
        Get the status of all profiles.
        """
        endpoint = f"{config.launcher_v1}/profile/statuses"
        return self.session.request("get", endpoint)

    def start(self, id: str):
        """
        Start a profile by its ID.

        Args:
            id (str): The ID of the profile to start.
        """
        endpoint = f"{config.launcher_v1}/profile/start/{id}"
        return self.session.request("get", endpoint)

    
    def stop(self, id: str | None = None, *types):
        """
        Stop a profile by its ID or stop all profiles of specified types.

        Args:
            id (str | None): The ID of the profile to stop. If None, stop all profiles.
            types: The types of profiles to stop if no ID is provided.
        """
        if id:
            endpoint = f"{config.launcher_v1}/profile/stop/{id}"
        else:
            confirm = input("Are you sure you want to stop all profiles? [yes]: ").strip().lower() or 'yes'
            if not confirm.startswith('y'):
                print("Operation cancelled.")
                return {"status": "cancelled", "message": "Operation cancelled by user."}
            endpoint = f"{config.launcher_v1}/profile/stop_all"
            if types:
                # Convert to URL encoded params
                joined = ",".join(map(str, types))
                endpoint = f"{endpoint}?types={joined}"
        return self.session.request("get", endpoint)


    def default(self, body: dict | Profile = {}):
        """
        Create a new profile with default settings.

        Args:
            body_ (dict | Profile): The profile data or Profile object.

        Returns:
            Profile: A new profile with defaults applied.
        """
        """
        Create a new profile on top of the defaults
        """
        body_ = body
        if isinstance(body, Profile):
            body_ = body.dict()

        logging.debug("Request launch with body: %s", body_)

        return Profile.with_defaults(body_)


class State(TypedDict):
    message: str
    status: str
    timestamp: int


class ActiveCounter(TypedDict):
    cloud: int
    local: int
    quick: int


class Data(TypedDict):
    active_counter: ActiveCounter
    states: dict[str, State]


class Status(TypedDict):
    error_code: str
    http_code: int
    message: str


class ProfileStateResponse(TypedDict):
    data: Data
    status: Status
