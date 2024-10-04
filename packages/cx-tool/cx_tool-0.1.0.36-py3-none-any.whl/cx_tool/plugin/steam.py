import typing
from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List

import click
import vdf

from cx_tool.plugin.plugin import Plugin, clickable, save_config

if typing.TYPE_CHECKING:
    from cx_tool.plugin.bottle import BottlePlugin


class SteamPlugin(Plugin):
    """Plugin to manage Steam local config."""

    name = "steam"

    STEAM_BOTTLE_PATH = Path("drive_c/Program Files (x86)/Steam")
    STEAM_USERDATA_PATH = STEAM_BOTTLE_PATH.joinpath("userdata")
    LOCALCONFIG_USERDATA_PATH = Path("config/localconfig.vdf")

    patches = {
        "632360": {"LaunchOptions": "-disable-gpu-skinning"}  # Risk of Rain 2
    }

    @cached_property
    def bottle(self) -> "BottlePlugin":
        return Plugin.get_plugin("bottle")

    @property
    def watching_bottles(self) -> List[str]:
        return self.data.get("watching", [])

    @contextmanager
    def localconfig(self, bottle_path: Path) -> Dict[str, Any]:
        """Find localconfig.vdf in the bottle."""

        for item in bottle_path.joinpath(self.STEAM_USERDATA_PATH).iterdir():
            if item.joinpath(self.LOCALCONFIG_USERDATA_PATH).exists():
                with open(item.joinpath(self.LOCALCONFIG_USERDATA_PATH)) as f:
                    data = vdf.load(f)
                    yield data

                    with open(item.joinpath(self.LOCALCONFIG_USERDATA_PATH), "w") as fw:
                        vdf.dump(data, fw, pretty=True)

    @staticmethod
    def get_apps(localconfig: Dict[str, Any]) -> Dict[str, Any]:
        return localconfig["UserLocalConfigStore"]["Software"]["Valve"]["Steam"]["apps"]

    @click.argument("bottle")
    @clickable
    @save_config
    def watch(self, bottle: str):
        """Watch the Steam configuration file."""

        if bottle not in self.bottle.bottle_names:
            raise click.UsageError(f"Bottle {bottle} not found.")

        if bottle not in self.data.get("watching", []):
            self.data.setdefault("watching", []).append(bottle)

        self.console_log(f"Watching {bottle}.")

    @click.argument("bottle")
    @clickable
    @save_config
    def unwatch(self, bottle: str):
        """Unwatch the Steam configuration file."""

        self.data["watching"].remove(bottle)

        self.console_log(f"Not watching for Steam config in {bottle}.")

    @clickable
    def watching(self):
        """List the bottles being watched."""

        for bottle in self.data.get("watching", []):
            self.console_log(bottle)

        self.patch_localconfig(self.bottle.get_bottle_path("Steam-2"))

    def patch_localconfig(self, bottle_path: Path):
        """Patch the localconfig.vdf file."""

        with self.localconfig(bottle_path) as localconfig:
            for app_id, app_data in self.get_apps(localconfig).items():
                if app_id in self.patches:
                    for key, value in self.patches[app_id].items():
                        app_data[key] = value

    def run(self):
        for bottle_name in self.watching_bottles:
            bottle_path = self.bottle.get_bottle_path(bottle_name)

    def on_load(self):
        self.cli_command("watch")(self.watch)
        self.cli_command("unwatch")(self.unwatch)
        self.cli_command("watching")(self.watching)

        # run in thread watcher
        # self.config.thread_manager.add_thread(self.run)
