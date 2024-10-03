import importlib
import json
import sys
from functools import cached_property
import importlib.metadata
import inspect
from pathlib import Path
from typing import Any, Dict

from plumbum import ProcessExecutionError
from pydantic import AnyUrl, validate_call
from rich.console import Console
from rich.table import Table

from cx_tool.plugin.plugin import (
    CrossOverControlPlugin,
    Platform,
    Plugin,
    clickable,
    save_config, with_status,
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
    @with_status("Finding installed packages...")
    def installed_packages(self) -> Dict[str, Dict[str, Any]]:
        """Get installed packages in venv."""

        try:
            return {
                p["name"]: p
                for p in json.loads(self.crossover.pip["list", "--format", "json"]())
            }
        except ProcessExecutionError as e:
            self.console_log(f"Error finding installed packages: {e}", err=True)
            return {}

    @cached_property
    def pip_inspect(self) -> Dict[str, Any]:
        self.set_status("Finding plugins in module...")

        return json.loads(self.crossover.pip("inspect"))

    @with_status("Finding plugins in module...")
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

    @with_status("Finding plugins in module...")
    def find_package_in_metadata(self, metadata_path: Path):
        metadata = importlib.metadata.PathDistribution(metadata_path)

        return [f for f in metadata.files if ".dist-info" not in f.as_posix()]

    @with_status("Installing packages...")
    def pip_install(self, *packages: str, allow_error: bool = False):
        """Install package using pip."""

        try:
            self.crossover.pip["install", "--ignore-installed", *packages].run(
                stderr=sys.stderr
            )
            self.console_log(f"Installed packages using pip.")
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
    @with_status("Adding package...")
    def add_requirement(self, package: AnyUrl | Path, version: str | None = None):
        """Add a plugin to the list of plugins to load.

        \b
        PACKAGE can be a URL, a path to a local package, or a package name, or git repo.
        VERSION can be a specific version or a version specifier like >=1.0.0, <2.0.0, etc.

        \b
        cx-tool will look for plugins in package, and add them to the list of available plugins.
        If the package does not contain any plugins, it will be uninstalled.

        \b
        Examples:
            cx-tool deps add git+https://example.com/user/package-repo.git
            cx-tool deps add git+git@example.com:user/package-repo.git
            cx-tool deps add https://example.com/package.whl
            cx-tool deps add /path/to/package.whl
            cx-tool deps add package-name
            cx-tool deps add package-name --version >=1.0.0
        """

        self.set_status("Starting installation...")
        self.console_log(f"Adding requirement {package}")

        if isinstance(package, Path) and not package.exists():
            package = str(package)

        if version is not None:
            if version[0] not in ("=", "<", ">", "!"):
                version = f"=={version}"

        self.pip_install(f"{package}{version}" if version else package)

        modules = set()
        plugins = set()

        if pkg := self.inspect_installed_package(package):
            self.console_log(f"Found package {pkg['metadata']['name']}")

            pkg_modules = set([
                (self.crossover.SITE_PACKAGES_PATH.joinpath(path), path.parts[0])
                for path in self.find_package_in_metadata(Path(pkg["metadata_location"]))
                if path.name == "__init__.py"
            ])

            for path, name in pkg_modules:
                if found_plugins := self.find_plugins_in_module(name, path):
                    self.console_log(f"Found plugins in module {name}")

                    plugins.update(found_plugins)

        if not plugins:
            self.set_status("Uninstalling package...")
            self.crossover.pip["uninstall", pkg["metadata"]["name"], "-y"].run(stderr=sys.stderr)

            self.console_log("No plugins found in package.", err=True)
            sys.exit(1)

        for plugin in plugins:
            self.config.plugins[plugin.name] = {
                "enabled": False,
                "name": plugin.name,
                "arch": plugin.arch,
                "platforms": plugin.platforms,
                "module": plugin.__module__,
                "path": plugin.__module_path__,
            }

        package_name = pkg["metadata"]["name"]

        self.requirements[package_name] = {
            "source": package,
        }

        if version is not None:
            self.requirements[package_name]["version"] = version

        self.console_log("Requirement added and installed.")

    @click.argument("package")
    @clickable
    @save_config
    @with_status("Removing package...")
    def remove_requirement(self, package: str):
        """Remove a plugin from the list of plugins to load."""

        if package not in self.requirements:
            self.console_log(
                f"Package `{package}` not found in list of requirements.",
                err=True,
            )
            sys.exit(1)

        self.crossover.pip["uninstall", package, "-y"].run(stderr=sys.stderr)
        self.requirements.pop(package)

        self.console_log("Requirement removed and uninstalled.")

    @click.argument("name")
    @clickable
    @save_config
    def enable_plugin(self, name: str):
        """Enable a plugin module."""

        if name in self.config.plugins:
            self.config.plugins[name]["enabled"] = True

        self.console_log("Plugin enabled.")

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

        table.add_column("", max_width=2)  # status
        table.add_column("Name", max_width=40)

        table.add_column("🍏", max_width=2)  # macos
        table.add_column("🐧", max_width=2)  # linux

        table.add_column("Arch")
        table.add_column("Summary")

        running_plugins = self.get_all_running_plugins()

        for plugin in self.get_all_plugins():
            icon = "🏠" if plugin.__module__.startswith("cx_tool") else "📦"
            table.add_row(
                "⚡️"
                if plugin in running_plugins
                else ("🔌" if plugin.check_platform() else "💀"),
                f"{icon} {plugin.name}",
                "💡" if Platform.macos in plugin.platforms else "🔌",
                "💡" if Platform.linux in plugin.platforms else "🔌",
                ", ".join(sorted(plugin.arch)),
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

        self.console_log("All requirements and plugins reset.")

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
