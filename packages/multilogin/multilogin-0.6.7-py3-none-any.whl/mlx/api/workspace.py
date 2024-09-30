import json

from mlx.api import Api
from mlx.config import config


class WorkspaceApi(Api):
    def get(self, *args, **kwargs):
        """
        Retrieve a list of workspaces.
        """
        return self.list(*args, **kwargs)

    def list(self, *args, **kwargs):
        """
        List all available workspaces.
        """
        return self.session.request(
            "get",
            f"{config.multilogin}/user/workspaces",
        ).data["workspaces"]
