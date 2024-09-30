from __future__ import annotations

import logging

from mlx.api import Api
from mlx.config import config
from mlx.exceptions import CoreDownloadAlreadyStarted
from mlx.models.profile import Profile

import requests.exceptions
import time


class BrowserCoreApi(Api):
    """
    Manage the browser core
    """

    def download(self, browser_type: str = "mimic", version: str = "128", wait=False):
        """
        Load the browser core.

        Args:
            browser_type (str): The type of browser to load (e.g., mimic, stealthfox).
            version (str): The version of the browser core to load.
            wait (bool, optional): Wait for the download to complete. Defaults to `false`.

        Returns:
            dict: The response from the API.
        """
        url = f"{str(config.launcher_v1)}/load_browser_core"
        params = {"browser_type": browser_type, "version": version}

        logging.debug("Loading browser core with params: %s", params)

        response = self.session.request("get", url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if (
                e.response.status_code == 500
                and "downloading of core already started" in e.response.text
            ):
                if wait:
                    print("Core download in progress")
                else:
                    raise RuntimeError(
                        "Failed to download core: downloading of core already started"
                    )
            else:
                raise e

        if wait:
            print("Waiting for download to complete; this may take a few seconds")

            def short_ver(_ver):
                return str(_ver).split(".")[0]

            def has_version(_ver, _data):
                for it in _data:
                    if (
                        it["type"] == browser_type
                        and it["is_latest"] == True
                        and any(short_ver(_ver) == _ver for x in it["versions"])
                    ):
                        return True
                return False

            condition = False
            retries = 0

            while not condition:
                retries += 1
                try:
                    data = self.inspect().data

                # requests.exceptions.HTTPError: 500 Server Error: Internal Server Error for url: https://launcher.mlx.yt:45001/api/v1/load_browser_core?browser_type=mimic&version=128: {"status":{"error_code":"INTERNAL_SERVER_ERROR","http_code":500,"message":"Failed to download core: downloading of core already started"}}
                except CoreDownloadAlreadyStarted as exc:
                    print(exc)
                else:
                    condition = has_version(version, data)
                    if condition:
                        return data
                    if retries % 5 == 0:
                        print(
                            f"Still waiting for download to complete; elapsed: {retries} seconds"
                        )

        return response

    def inspect(self):
        """
        Inspect downloaded browser cores.

        Returns:
            dict: The response from the API.
        """
        url = f"{str(config.launcher_v1)}/loaded_browser_cores"

        logging.debug("Listing browser cores")

        return self.session.request("get", url, use_backoff=False)


class LauncherApi(Api):
    core: BrowserCoreApi

    def version(self):
        """
        Get the agent's version
        """
        url = f"{str(config.launcher_v1)}/version"

        print(f"Fetching API version from: {url}")
        return self.session.request("get", url, use_backoff=False)

    def quick(self, body: dict | Profile = {}, forward: bool = False):
        """
        Launch a quick profile.

        Args:
            body (dict | Profile): Profile JSON to launch. Will overlay on top of default values.
            forward (bool, optional): Forward the automation port to `MLX_AUTOMATION_PORT` or `4444`. Defaults to `False`.

        Returns:
            Profile: The profile object.
        """
        url = f"{config.launcher_v3}/profile/quick"

        if isinstance(body, dict):
            body = Profile.with_defaults(body)

        logging.debug("with_defaults: %s", body)

        response = self.session.request("post", url, json=body.dict())

        if forward:
            import subprocess

            port = response.data.get("port", 4444)
            socat_command = f"socat TCP-LISTEN:4444,fork TCP:localhost:{port}"
            print(response)
            logging.debug(f"Running socat for port-forwarding on port {port}")
            try:
                subprocess.run(socat_command, shell=True, check=True)
            # catch sigterm sigint
            except KeyboardInterrupt:
                print("Exiting port forward. WARNING: profile still running")

        return response

    def ready(self, wait=180):
        """
        Block until the API is ready or timeout is reached.

        Params:
        wait: int = 180 - Timeout (in seconds) to wait for the API to become ready. Don't like waiting? Make it 0.
        """

        start_time = time.time()
        while time.time() - start_time < wait:
            ver = self.version()
            if str(ver["status"]["http_code"]) == "200":
                return "API is ready"
            time.sleep(1)

        raise TimeoutError("Launcher not ready after {} seconds".format(wait))

    def body(self, override: dict = {}):
        """
        Validate a profile JSON with defaults applied.
        """

        return Profile.with_defaults(override).dict()
