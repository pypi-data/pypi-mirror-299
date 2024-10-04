import sys
import typing
from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List

import click
import vdf
from click import Context
from plumbum.cmd import curl, unzip

from cx_tool.misc import LazyChoice, to_windows_path
from cx_tool.plugin.plugin import Plugin, clickable, save_config, with_status


if typing.TYPE_CHECKING:
    from cx_tool.plugin.bottle import BottlePlugin


def get_bottle_names():
    return Plugin.get_plugin("bottle").bottle_names


class SteamPlugin(Plugin):
    """Plugin to manage Steam local config."""

    name = "steam"
    requires = ["bottle"]

    STEAM_BOTTLE_PATH = Path("drive_c/Program Files (x86)/Steam")
    STEAM_USERDATA_PATH = STEAM_BOTTLE_PATH.joinpath("userdata")
    LOCALCONFIG_USERDATA_PATH = Path("config/localconfig.vdf")

    STEAM_CMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    STEAM_CMD_BOTTLE_PATH = Path("Program Files (x86)/SteamCMD")

    patches = {
        "632360": {"LaunchOptions": "-disable-gpu-skinning"}  # Risk of Rain 2
    }

    @cached_property
    def bottle(self) -> "BottlePlugin":
        return Plugin.get_plugin("bottle")

    @cached_property
    def cli(self):
        return self.bottle.cli.group("steam", help="Steam tools.")(lambda: None)

    @cached_property
    def steam_cmd_group(self):
        return self.cli.group("cmd", help="Steam command line tools.")(lambda: None)

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

    @clickable
    @save_config
    def watch(self, bottle: str):
        """Watch the Steam configuration file."""

        if bottle not in self.bottle.bottle_names:
            raise click.UsageError(f"Bottle {bottle} not found.")

        if bottle not in self.data.get("watching", []):
            self.data.setdefault("watching", []).append(bottle)

        self.console_log(f"Watching {bottle}.")

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

    @clickable
    @with_status("Installing SteamCMD...")
    def install_cmd(self, bottle: str):
        """Install Steam command line tools."""

        # TODO: download and install steamcmd
        self.set_status("Downloading SteamCMD...")

        bottle_path = self.bottle.get_bottle_path(bottle)
        cmd_path = bottle_path.joinpath("drive_c", self.STEAM_CMD_BOTTLE_PATH)

        cmd_path.mkdir(parents=True, exist_ok=True)

        curl[
            "-o",
            cmd_path.joinpath("steamcmd.zip"),
            self.STEAM_CMD_URL,
        ].run(stdout=self.console.stderr)

        self.console_log("SteamCMD downloaded.")

        self.set_status("Extracting SteamCMD...")

        unzip[
            "-o",
            cmd_path.joinpath("steamcmd.zip"),
            "-d",
            cmd_path,
        ].run(stdout=self.console.stderr)

        self.console_log("SteamCMD installed.")

    @Plugin.pass_click_context
    @clickable
    def cmd_cli(self, ctx: Context, bottle: str):
        """Steam CLI."""

        bottle_path = self.bottle.get_bottle_path(bottle)
        cmd_path = bottle_path.joinpath("drive_c", self.STEAM_CMD_BOTTLE_PATH)

        if not cmd_path.exists():
            self.console_log("SteamCMD not installed.", err=True)
            sys.exit(1)

        ctx.invoke(
            self.bottle.run,
            self.bottle,
            bottle,
            to_windows_path(self.STEAM_CMD_BOTTLE_PATH.joinpath("steamcmd.exe")),
        )

    @click.argument("bottle", type=LazyChoice(get_bottle_names))
    @click.argument("command", nargs=-1)
    @Plugin.pass_click_context
    @clickable
    def run(self, ctx: Context, bottle: str, command: list[str]):
        """Run SteamCMD command."""

        bottle_path = self.bottle.get_bottle_path(bottle)
        cmd_path = bottle_path.joinpath("drive_c", self.STEAM_CMD_BOTTLE_PATH)

        if not cmd_path.exists():
            self.console_log("SteamCMD not installed.", err=True)
            sys.exit(1)

        ctx.invoke(
            self.bottle.run,
            self.bottle,
            bottle,
            to_windows_path(self.STEAM_CMD_BOTTLE_PATH.joinpath("steamcmd.exe")),
            arguments=" ".join(command),
        )

    def on_load(self):
        for bottle in self.bottle.bottles:
            bottle_group = self.bottle.bottle_cli_group(bottle.name)
            steam_group = bottle_group.group("steam", help="Steam tools.")(lambda: None)

            self.cli_command("watch", steam_group)(
                self.watch.partial(bottle=bottle.name)
            )
            self.cli_command("unwatch", steam_group)(
                self.unwatch.partial(bottle=bottle.name)
            )
            self.cli_command("watching", steam_group)(
                self.watching.partial(bottle=bottle.name)
            )

            cmd_group = steam_group.group("cmd", help="Steam command line tools.")(
                lambda: None
            )

            # Steamcmd commands
            self.cli_command("install", cmd_group, no_args_is_help=False)(
                self.install_cmd.partial(bottle=bottle.name)
            )
            self.cli_command("cli", cmd_group, no_args_is_help=False)(
                self.cmd_cli.partial(bottle=bottle.name)
            )
            self.cli_command("run", cmd_group, no_args_is_help=False)(
                self.run.partial(bottle=bottle.name)
            )

        # run in thread watcher
        # self.config.thread_manager.add_thread(self.run)
