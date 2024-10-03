import inspect
import os
import time
import typing
import webbrowser
from functools import cached_property
from pathlib import Path
from typing import List

import click
from plumbum import ProcessExecutionError, local
from plumbum.cmd import mv, ditto, rm
from plumbum.commands.base import BoundCommand

from cx_tool.plugin.context import PluginContext
from cx_tool.plugin.plugin import (
    Architecture,
    CrossOverControlPlugin,
    Platform,
    Plugin,
    clickable,
    restart_required,
    save_config, with_status,
)

if typing.TYPE_CHECKING:
    from cx_tool.plugin.plist import PListPlugin


class MacPlugin(Plugin, CrossOverControlPlugin):
    """Plugin to manage macOS specific features.

    \b
    Enables AVX, AVX2, and DirectX Raytracing for Apple Silicon.
    Helps to patch Game Porting Toolkit.
    """

    name = "crossover"
    platforms = [Platform.macos]
    arch = [Architecture.arm64, Architecture.x86_64]

    GPTK_PATH = Path("/Volumes/Evaluation environment for Windows games 2.0")
    APP_PATH = Path("/Applications/CrossOver.app/Contents/MacOS")
    VENV_PATH = APP_PATH.joinpath(".venv")
    LOG_PATH = APP_PATH.joinpath("crossover-util.log")

    @property
    def SITE_PACKAGES_PATH(self) -> Path:
        return self.VENV_PATH.joinpath(f"lib/python{self.python_version}/site-packages")

    @property
    def is_running(self):
        return bool(self.find_pids())

    @cached_property
    def architecture(self) -> BoundCommand:
        return local.get("arch")["-x86_64"]

    @cached_property
    def python(self) -> BoundCommand:
        return self.architecture[self.VENV_PATH.joinpath("bin/python")]

    @cached_property
    def python_version(self):
        return ".".join(self.python["--version"]().split()[-1].split(".")[:2])

    @cached_property
    def venv(self):
        return super().python["-m", "venv"]

    @property
    def pip(self) -> BoundCommand:
        return self.python["-m", "pip"]

    @property
    def bottles_path(self) -> Path:
        return Path(
            self.data.get(
                "bottles_path",
                "~/Library/Application Support/CrossOver/Bottles/",
            )
        ).expanduser()

    @cached_property
    def plist(self) -> "PListPlugin":
        return Plugin.get_plugin("plist")

    @cached_property
    def avx_group(self):
        return self.cli.group("avx", help="Manage AVX settings")(lambda: None)

    @cached_property
    def dxr_group(self):
        return self.cli.group("dxr", help="Manage DXR settings")(lambda: None)

    @cached_property
    def update_group(self):
        return self.cli.group("update", help="Manage CrossOver updates")(lambda: None)

    @cached_property
    def gptk_group(self):
        return self.cli.group("gptk", help="Manage GPTK")(lambda: None)

    @clickable
    @restart_required
    @save_config
    def enable_avx(self):
        """Enable AVX."""

        self.data["ROSETTA_ADVERTISE_AVX"] = True

        self.console_log("AVX enabled.")

    @clickable
    @restart_required
    @save_config
    def enable_dxr(self):
        """Enable DirectX Raytracing."""

        self.data["D3DM_SUPPORT_DXR"] = True

        self.console_log("DirectX Raytracing enabled.")

    @clickable
    @restart_required
    @save_config
    def disable_avx(self):
        """Disable AVX."""

        self.data["ROSETTA_ADVERTISE_AVX"] = False

        self.console_log("AVX disabled.")

    @clickable
    @restart_required
    @save_config
    def disable_dxr(self):
        """Disable DirectX Raytracing."""

        self.data["D3DM_SUPPORT_DXR"] = False

        self.console_log("DirectX Raytracing disabled.")

    @clickable
    def download_gptk(self):
        """Download Game Porting Toolkit."""

        return webbrowser.open(
            "https://developer.apple.com/games/game-porting-toolkit/"
        )

    @clickable
    def patch_gptk(self):
        """Patch Game Porting Toolkit."""

        if not self.GPTK_PATH.exists():
            self.console_log("Mounted GPTK not found.")
            self.console_log("Please download Game Porting Toolkit from Apple's website.")
            self.console_log("Mount downloaded disk image.")
            self.console_log(
                "Then mount `Evaluation environment` and call this command again."
            )

            if click.confirm("Would you like to download GPTK?", abort=True):
                webbrowser.open(
                    "https://developer.apple.com/games/game-porting-toolkit/"
                )
            return

        crossover_gptk_path = Path(
            "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver"
            "/lib64/apple_gptk/external"
        )

        if not os.path.exists(crossover_gptk_path):
            os.makedirs(crossover_gptk_path)

        rm["-rf", crossover_gptk_path.joinpath("D3DMetal.framework-old")]()
        rm["-rf", crossover_gptk_path.joinpath("libd3dshared.dylib-old")]()

        mv[
            crossover_gptk_path.joinpath("D3DMetal.framework"),
            crossover_gptk_path.joinpath("D3DMetal.framework-old"),
        ]()

        mv[
            crossover_gptk_path.joinpath("libd3dshared.dylib"),
            crossover_gptk_path.joinpath("libd3dshared.dylib-old"),
        ]()

        ditto[self.GPTK_PATH.joinpath("redist/lib/external"), crossover_gptk_path]()

        self.console_log("GPTK patched")

    @clickable
    def rollback_gptk(self):
        """Rollback Game Porting Toolkit."""

        crossover_gptk_path = Path(
            "/Applications/CrossOver.app/Contents/SharedSupport/CrossOver"
            "/lib64/apple_gptk/external"
        )

        if not os.path.exists(crossover_gptk_path):
            self.console_log("GPTK not found.")
            return

        old_metal = crossover_gptk_path.joinpath("D3DMetal.framework-old")
        old_shared = crossover_gptk_path.joinpath("libd3dshared.dylib-old")

        if not old_metal.exists() or not old_shared.exists():
            self.console_log("Backup not found.")
            return

        rm["-rf", crossover_gptk_path.joinpath("D3DMetal.framework")]()
        rm["-rf", crossover_gptk_path.joinpath("libd3dshared.dylib")]()

        mv[
            crossover_gptk_path.joinpath("D3DMetal.framework-old"),
            crossover_gptk_path.joinpath("D3DMetal.framework"),
        ]()

        mv[
            crossover_gptk_path.joinpath("libd3dshared.dylib-old"),
            crossover_gptk_path.joinpath("libd3dshared.dylib"),
        ]()

        self.console_log("GPTK rolled back.")

    def on_load(self):
        # AVX
        self.cli_command("enable", self.avx_group)(self.enable_avx)
        self.cli_command("disable", self.avx_group)(self.disable_avx)

        # DXR
        self.cli_command("enable", self.dxr_group)(self.enable_dxr)
        self.cli_command("disable", self.dxr_group)(self.disable_dxr)

        # Update
        self.cli_command("enable", self.update_group)(self.enable_update)
        self.cli_command("disable", self.update_group)(self.disable_update)

        # GPTK
        self.cli_command("patch", self.gptk_group)(self.patch_gptk)
        self.cli_command("download", self.gptk_group)(self.download_gptk)
        self.cli_command("rollback", self.gptk_group)(self.rollback_gptk)

    def on_start(self, ctx: PluginContext):
        if self.data.get("ROSETTA_ADVERTISE_AVX"):
            ctx.environment["ROSETTA_ADVERTISE_AVX"] = "1"

        if self.data.get("D3DM_SUPPORT_DXR"):
            ctx.environment["D3DM_SUPPORT_DXR"] = "1"

    @with_status("Looking for CrossOver processes..")
    def find_pids(self) -> List[int]:
        """Find the PIDs of the CrossOver processes."""

        from plumbum.cmd import ps, grep

        pids = ps["-A"] | grep[self.APP_PATH]

        return [
            int(row.split()[0])
            for row in pids().strip().split("\n")
            if "grep" not in row.split()[3] and int(row.split()[0]) != os.getpid()
        ]

    @with_status("Terminating CrossOver..")
    def kill_crossover(self, silent: bool = False) -> None:
        """Kill the CrossOver processes."""

        from plumbum.cmd import kill

        crossover_pids = self.find_pids()

        if crossover_pids and not silent:
            self.console_log("CrossOver is running. Terminating...")

        for pid in self.find_pids():
            try:
                kill["-15"](pid)
            except ProcessExecutionError:
                pass

        while self.find_pids():
            self.set_status("Waiting for CrossOver to terminate...")
            time.sleep(0.2)
        else:
            if not silent:
                self.console_log("CrossOver has been terminated.")

    @with_status("Running CrossOver...")
    def run_crossover(self, background: bool = False):
        """Run CrossOver."""

        from plumbum.cmd import zsh

        ctx = PluginContext()

        for plugin in Plugin.get_all_running_plugins():
            plugin.on_start(ctx)

        bin_path = self.APP_PATH.joinpath("CrossOver")

        if self.APP_PATH.joinpath("CrossOver.origin").exists():
            bin_path = self.APP_PATH.joinpath("CrossOver.origin")

        cmd = zsh["-c"][f"{ctx.env_str} {bin_path.expanduser()} {ctx.args_str}"]

        crossover_log = self.APP_PATH.joinpath("crossover.log")

        if background:
            cmd.nohup(
                stdout=crossover_log,
                stderr=crossover_log,
            )
        else:
            cmd()

    @with_status("Installing CrossOver patch...")
    def install(self):
        """Inject self as the CrossOver process."""

        from plumbum.cmd import chmod

        self.kill_crossover(silent=True)

        bin_path = self.APP_PATH.joinpath("CrossOver")

        if not self.APP_PATH.joinpath("CrossOver.origin").exists():
            mv[bin_path, bin_path.with_suffix(".origin")]()
        else:
            self.console_log("CrossOver is already injected. Updating...")

        self.set_status("Removing virtual environment...")
        rm["-rf", self.VENV_PATH]()
        self.console_log("Current virtual environment has been removed.")

        self.set_status("Creating virtual environment...")
        self.venv(self.VENV_PATH)
        self.console_log("Virtual environment has been created.")

        self.set_status("Updating pip")
        self.pip["install", "--upgrade", "pip"]()
        self.console_log("Updated pip.")

        self.set_status("Installing cx-tool")
        self.pip["install", "--ignore-installed", "cx-tool"]()
        self.console_log("Installed cx-tool.")

        self.set_status("Injecting CrossOver patch...")

        entrypoint = inspect.cleandoc(
            f"""
                #!{self.python}
                import syslog
                import logging
                import sys

                LOG_PATH = "{self.LOG_PATH}"

                syslog.openlog("CrossOverUtil")
                logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)

                import cx_tool
                from cx_tool.config import config

                config.init_plugins()

                if __name__ == "__main__":
                    sys.exit(config.crossover_plugin.run_crossover())
            """
        )

        with open(bin_path, "w") as entrypoint_file:
            entrypoint_file.write(entrypoint)

        chmod["+x"](bin_path)
        chmod["+x"](bin_path.with_suffix(".origin"))

        self.console_log("CrossOver patch has been injected.")

    @with_status("Uninstalling CrossOver patch...")
    def uninstall(self):
        self.kill_crossover(silent=True)

        bin_path = self.APP_PATH.joinpath("CrossOver")

        if self.APP_PATH.joinpath("CrossOver.origin").exists():
            mv[bin_path.with_suffix(".origin"), bin_path]()
            self.console_log("CrossOver has been restored.")

    @clickable
    def disable_update(self):
        """Disable CrossOver updates."""

        ctx = click.get_current_context()

        ctx.invoke(self.plist.set, key="SUFeedURL", value="")

        self.console_log("CrossOver updates disabled.")

    @clickable
    def enable_update(self):
        """Enable CrossOver updates."""

        ctx = click.get_current_context()

        ctx.invoke(self.plist.set, key="SUFeedURL", value=None)

        self.console_log("CrossOver updates enabled.")
