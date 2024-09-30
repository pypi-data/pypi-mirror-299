import logging

import fire
import rich

from mlx.api import Api
from mlx.api.launcher import BrowserCoreApi, LauncherApi
from mlx.agent import AgentController
from mlx.api.profile import ProfileApi
from mlx.api.workspace import WorkspaceApi
from mlx.config import CredentialsConfig, config
from mlx.models.api_response import ApiResponse
from mlx.session import SessionManager

# builtins.print = rich.print  # type: ignore

session = SessionManager()


class CLI(LauncherApi):
    """
    Client interface with the MLX agent.
    """

    def __init__(self) -> None:
        # self.launcher = LauncherApi()
        self.core = BrowserCoreApi()
        self.agent = AgentController()
        self.profile = ProfileApi()

        super().__init__()

    def whoami(self):
        """Print the current user."""
        return WorkspaceApi().get()

    def credentials(self, email: str | None = None, password: str | None = None):
        """Set or print current username and password"""

        cfg = CredentialsConfig()
        if email is None and password is None:
            # PRINT & RETURN
            return {
                "email": cfg.email,
                "password": cfg.password,
            }
        raise NotImplementedError(
            "Setting credentials is not yet implemented. Use MLX_ env vars"
        )

    def start(self):
        """Start the MLX agent."""
        return self.agent.start()

    def logs(self):
        """Retrieve agent logs."""
        return self.agent.logs()

    def ps(self):
        """Alias for agent status."""
        return self.agent.status()

    def cores(self):
        """Retrieve core status."""
        return self.core.inspect()

    def token(self, token: str | None = None):
        """Set or print the current authentication token."""

        cfg = CredentialsConfig()

        if token is None:
            # PRINT & RETURN

            return cfg.token

        raise NotImplementedError(
            "Setting token is not yet implemented. Use MLX_ env vars."
        )

    def ping(self):
        """Test launcher connectivity. Expect 'pong' as a response when API returns 200"""
        ver = self.version()

        assert str(ver["status"]["http_code"]) == "200"

        return "pong"

    def sessions(self):
        """
        List all sessions.
        """
        url = f"{config.launcher_v1}/profile/statuses"

        return session.request("get", url)


def main():
    logging.basicConfig(level=logging.CRITICAL)
    import json

    def serialize(obj):
        """
        Uses rich to pretty print objects that can be serialized to JSON.
        If the object is not a primitive, return as-is
        """

        if isinstance(obj, ApiResponse):
            obj = obj.json()
        elif isinstance(obj, (dict,list)):
            obj = json.dumps(obj, indent=2)


        if not isinstance(obj, (dict, list, tuple, str, int, float, bool)):
            return obj

        def _format(response):
            """Picks up the [data] key's value from response JSON objects"""

            # Verify that the protocol of the response matches
            # By checking whether it contains only the 'data' and 'status' keys

            def is_valid_api_response(obj: dict) -> bool:
                if not isinstance(obj, dict):
                    return False
                if "status" not in obj or "data" not in obj:
                    return False
                if not isinstance(obj["status"], dict):
                    return False
                if not isinstance(obj["data"], (list, dict)):
                    return False
                return True

            if is_valid_api_response(response):
                return json.dumps(response["data"], indent=2)
            return response

        rich.print(_format(obj))

    fire.Fire(CLI, serialize=serialize)


if __name__ == "__main__":
    main()
