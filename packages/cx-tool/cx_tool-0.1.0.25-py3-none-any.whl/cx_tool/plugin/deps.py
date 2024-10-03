import importlib
import json
import sys
from functools import cached_property
import importlib.metadata
from pathlib import Path
from typing import Any, Dict

from plumbum import ProcessExecutionError
from pydantic import AnyUrl, validate_call
from rich.console import Console
from rich.table import Table

from crossover_util.plugin.plugin import (
    CrossOverControlPlugin,
    Plugin,
    clickable,
    save_config,
)

import click


class DepsPlugin(Plugin):
    """Plugin to manage dependencies.

    \b
    Checks for missing dependencies and installs them.
    Handles adding and removing plugins.
    """

    name = "deps"

    @property
    def crossover(self) -> CrossOverControlPlugin:
        return Plugin.get_plugin("crossover")

    @property
    def requirements(self) -> dict[str, dict[str, Any]]:
        return self.data.setdefault("requirements", {})

    @cached_property
    def req_group(self):
        return self.cli.group("r", help="Manage plugin requirements.")(lambda: None)

    @cached_property
    def plugin_group(self):
        return self.cli.group("p", help="Manage plugin modules.")(lambda: None)

    @cached_property
    def installed_packages(self) -> Dict[str, Dict[str, Any]]:
        """Get installed packages in venv."""

        return {
            p["name"]: p
            for p in json.loads(self.crossover.pip["list", "--format", "json"]())
        }

    @cached_property
    def pip_inspect(self) -> Dict[str, Any]:
        return json.loads(self.crossover.pip("inspect"))

    def inspect_installed_package(self, package: AnyUrl | Path | str) -> Dict[str, Any]:
        """Inspect installed package."""

        for p in self.pip_inspect["installed"]:
            if (
                isinstance(package, AnyUrl)
                and p.get("direct_url", {}).get("url") == package
            ):
                return p

            elif (
                isinstance(package, Path)
                and p.get("direct_url", {}).get("url", "").startswith("file://")
                and Path(p["direct_url"]["url"][7:]).resolve() == package.resolve()
            ):
                return p

            elif p["metadata"]["name"] == package:
                return p

        return {}

    @staticmethod
    def find_package_in_metadata(metadata_path: Path):
        metadata = importlib.metadata.PathDistribution(metadata_path)

        return [f for f in metadata.files if ".dist-info" not in f.as_posix()]

    def pip_install(self, *packages: str, allow_error: bool = False):
        """Install package using pip."""

        try:
            self.crossover.pip["install", "--ignore-installed", *packages].run(
                stderr=sys.stderr
            )
        except ProcessExecutionError as e:
            if allow_error:
                return

            sys.exit(e.retcode)

    @clickable
    def list_requirements(self):
        """List all requirements."""

        table = Table(
            title="Requirements", show_header=True, header_style="bold magenta"
        )

        table.add_column("Package", max_width=30)
        table.add_column("Source", max_width=30)
        table.add_column("Version")
        table.add_column("Installed")
        table.add_column("Modules")

        installed = self.installed_packages

        for name, req in self.requirements.items():
            table.add_row(
                name,
                req.get("source"),
                req.get("version", "*"),
                installed.get(name, {}).get("version", ""),
                "\n".join(req.get("modules", [])),
            )

        console = Console()
        console.print(table)

    @click.argument("package")
    @click.option("--version", help="Version of the package.")
    @clickable
    @save_config
    @validate_call
    def add_requirement(self, package: AnyUrl | Path, version: str | None = None):
        """Add a plugin to the list of plugins to load."""

        if isinstance(package, Path) and not package.exists():
            package = str(package)

        if version is not None:
            if version[0] not in ("=", "<", ">", "!"):
                version = f"=={version}"

        self.pip_install(f"{package}{version}" if version else package)

        modules = set()
        if pkg := self.inspect_installed_package(package):
            for path in self.find_package_in_metadata(Path(pkg["metadata_location"])):
                modules.add(path.parts[0])

        package_name = pkg["metadata"]["name"]

        self.requirements[package_name] = {
            "modules": list(modules),
            "source": package,
        }

        if version is not None:
            self.requirements[package_name]["version"] = version

        click.echo("Requirement added and installed.")

    @click.argument("package")
    @clickable
    @save_config
    def remove_requirement(self, package: str):
        """Remove a plugin from the list of plugins to load."""

        if package not in self.requirements:
            raise click.UsageError(
                f"Package `{package}` not found in list of requirements."
            )

        self.crossover.pip["uninstall", package, "-y"].run(stderr=sys.stderr)
        self.requirements.pop(package)

        click.echo("Requirement removed and uninstalled.")

    @click.argument("module")
    @clickable
    @save_config
    def enable_plugin(self, module: str):
        """Enable a plugin module."""

        try:
            plugins = self.find_plugins_in_module(module)
            if not plugins:
                raise click.UsageError(
                    f"Module `{module}` is not a crossover-util plugin library."
                )
        except ImportError:
            raise click.UsageError(f"Package `{module}` not found.")

        self.config.plugins.add(module)

        click.echo("Plugin enabled.")

    @click.argument("module")
    @clickable
    @save_config
    def disable_plugin(self, module: str):
        """Disable a plugin module."""

        if module not in self.config.plugins:
            raise click.UsageError(f"Module `{module}` not found in list of plugins.")

        self.config.plugins.remove(module)

    @clickable
    def list_plugins(self):
        """List all plugins."""

        table = Table(title="Plugins", show_header=True, header_style="bold magenta")

        table.add_column("Name", max_width=30)
        table.add_column("Platform")
        table.add_column("Summary")

        for plugin in self.all_plugins():
            table.add_row(
                plugin.name,
                ", ".join(plugin.platforms),
                plugin.__doc__.strip().split("\n")[0],
            )

        console = Console()
        console.print(table)

    @clickable
    def reset(self):
        """Reset all requirements and plugins."""

        ctx = click.get_current_context()

        self.data.clear()
        self.config.plugins.clear()
        self.config.write()

        click.echo("All requirements and plugins reset.")

        ctx.invoke(self.crossover.install)

    def setup_cli(self):
        if self.config is None:
            return

        self.cli_command("list", self.req_group)(self.list_requirements)
        self.cli_command("add", self.req_group)(self.add_requirement)
        self.cli_command("del", self.req_group)(self.remove_requirement)
        self.cli_command("enable", self.plugin_group)(self.enable_plugin)
        self.cli_command("disable", self.plugin_group)(self.disable_plugin)
        self.cli_command("list", self.plugin_group)(self.list_plugins)
        self.cli_command("reset")(self.reset)

    def on_load(self):
        self.ensure_plugins()
        self.setup_cli()

    def ensure_plugins(self):
        """Ensure dependencies are installed."""

        if self.config is None:
            return

        installed = self.installed_packages
        plugins_to_install = set()

        for name, req in self.requirements.items():
            pkg = installed.get(name)

            if pkg is None:
                plugins_to_install.add(req["source"])
                continue

            if req.get("version") is not None and pkg["version"] != req["version"]:
                plugins_to_install.add(req["source"])

        if plugins_to_install:
            self.pip_install(*plugins_to_install, allow_error=True)
