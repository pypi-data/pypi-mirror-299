import copy
import importlib
import inspect
import sys
import importlib.util

import typing
from enum import Enum
from functools import cached_property, lru_cache, partial, wraps
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import List, Type, Optional, ClassVar

import click
from plumbum import local
from plumbum.commands.base import BoundCommand
from rich.console import Console


if typing.TYPE_CHECKING:
    from cx_tool.config import UtilConfig
    from cx_tool.plugin.context import PluginContext
    from click import Group


class Platform(str, Enum):
    linux = "linux"
    macos = "darwin"


class Architecture(str, Enum):
    x86_64 = "x86_64"
    arm64 = "arm64"


class Plugin:
    name: str
    platforms: List[Platform] = [Platform.macos, Platform.linux]
    arch: List[Architecture] = [Architecture.x86_64, Architecture.arm64]

    __REGISTRY__ = {}
    __ALL__ = []

    def __init__(self, config: "UtilConfig"):
        self.config = config
        self._cli = None
        self._status = None

    @property
    def data(self):
        return self.config.get_plugin_data(self)

    @property
    def cli(self) -> "Group":
        from click import Group

        if self._cli is None:
            self._cli = Group(self.name, help=self.__doc__)
            self.config.plugin_cli.add_command(self._cli)

        return self._cli

    @property
    def python(self) -> BoundCommand:
        return local.get(sys.executable)

    @classmethod
    @lru_cache
    def get_arch(cls) -> str:
        return local.get(sys.executable)[
            "-c", "import platform;print(platform.machine())"
        ]().strip()

    @classmethod
    @lru_cache
    def get_platform(cls) -> str:
        return local.get(sys.executable)[
            "-c", "import sys;print(sys.platform)"
        ]().strip()

    def cli_command(
        self,
        name: str,
        cli: Optional["Group"] = None,
        no_args_is_help: Optional[bool] = None,
        **kwargs,
    ):
        def wrapper(f: clickable):
            cli_ = cli or self.cli

            if name in cli_.commands:
                return

            return cli_.command(
                name,
                context_settings=dict(
                    allow_extra_args=True,
                ),
                no_args_is_help=(
                    no_args_is_help
                    if no_args_is_help is not None
                    else bool(set(inspect.signature(f.f).parameters) - {"self"})
                ),
                **kwargs,
            )(f.with_plugin(self))

        return wrapper

    def on_load(self): ...

    def on_unload(self): ...

    def on_start(self, ctx: "PluginContext"): ...

    def on_stop(self, ctx: "PluginContext"): ...

    @staticmethod
    def import_from_file(name: str, path: Path):
        """Import module from file."""

        loader = SourceFileLoader(name, str(path))

        spec = importlib.util.spec_from_file_location(
            name,
            loader=loader,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    @cached_property
    def console(self):
        return Console()

    @property
    def is_silent(self) -> bool:
        """Check if the plugin is running in silent mode."""

        if ctx := get_main_ctx():
            return ctx.params.get("silent", False)
        return True

    def console_log(self, message: str, err: bool = False, warn: bool = False) -> None:
        """Log message to console."""

        if self.is_silent:
            return

        match err, warn:
            case True, False:
                message = f"[red bold]{message}"
            case False, True:
                message = f"[yellow bold]{message}"

        self.console.log(message)

    def set_status(self, message: str):
        """Update status message."""

        if self.is_silent:
            return

        if self._status is not None:
            self._status.update(message)
        else:
            self._status = self.console.status(message).__enter__()

    def reset_status(self):
        """Reset status message."""

        if self._status is not None:
            self._status.__exit__(None, None, None)
            self._status = None

    @classmethod
    def find_plugins_in_module(
        cls, module_name: str, module_path: Path
    ) -> List[Type["Plugin"]]:
        """Find Plugins in module."""

        plugins = []

        try:
            for item in cls.import_from_file(
                module_name, module_path
            ).__dict__.values():
                if (
                    isinstance(item, type)
                    and issubclass(item, Plugin)
                    and item is not Plugin
                ):
                    item.__module_path__ = module_path
                    plugins.append(item)
        except ImportError:
            pass

        return plugins

    @classmethod
    def get_plugin(cls, name: str):
        """Get plugin by name."""

        return cls.__REGISTRY__.get(name)

    @classmethod
    def check_platform(cls) -> bool:
        """Check if the plugin is compatible with the current platform."""

        if cls.get_platform() not in cls.platforms:
            return False

        if cls.get_arch() not in cls.arch:
            return False

        return True

    @classmethod
    def add_plugin(cls, plugin: "Plugin", enabled: bool = True):
        cls.__ALL__.append(plugin)

        if not plugin.check_platform() or not enabled:
            return

        if plugin.name in cls.__REGISTRY__:
            Console().log(
                f"Plugin with name `{plugin.name}` already exists in other package.",
            )
        else:
            cls.__REGISTRY__[plugin.name] = plugin

    @classmethod
    def get_all_running_plugins(cls) -> List["Plugin"]:
        """List all running plugins."""

        return list(cls.__REGISTRY__.values())

    @classmethod
    def get_all_plugins(cls) -> List["Plugin"]:
        """Return all plugins even unsupported ones."""

        return cls.__ALL__

    @classmethod
    def import_plugins(cls, config: "UtilConfig"):
        """Import and init plugins."""

        for plugin_data in config.plugins.values():
            for plugin in cls.find_plugins_in_module(
                plugin_data["module"], plugin_data["path"]
            ):
                cls.add_plugin(plugin(config), enabled=plugin_data["enabled"])

    @classmethod
    def pass_click_context(cls, c: "clickable"):
        """Pass click context to the clickable function."""

        c.lazy_partial("ctx", click.get_current_context)

        return c


class clickable:  # noqa
    def __init__(self, f):
        self.f = f
        self.args = []
        self.kwargs = {}
        self.orig_func = f
        self.lazy = {}

    def with_plugin(self, plugin: "Plugin") -> "clickable":
        if not isinstance(self.f, partial):
            self.f = partial(self.f, *[plugin, *self.args], **self.kwargs)
        return self

    def partial(self, *args, **kwargs):
        clickable_ = copy.deepcopy(self)
        clickable_.args.extend(args)
        clickable_.kwargs.update(kwargs)
        return clickable_

    def lazy_partial(self, name, callback):
        self.lazy[name] = callback
        return self

    def __call__(self, *args, **kwargs):
        for name, callback in self.lazy.items():
            kwargs[name] = callback()
        return self.f(*args, **kwargs)

    @property
    def __doc__(self):
        return self.orig_func.__doc__


class CrossOverControlPlugin:
    VENV_PATH: ClassVar[Path]
    LOG_PATH: ClassVar[Path]
    SITE_PACKAGES_PATH: ClassVar[Path]

    @property
    def is_running(self):
        raise NotImplementedError()

    @property
    def bottles_path(self) -> Path:
        raise NotImplementedError()

    @property
    def python(self) -> BoundCommand:
        raise NotImplementedError()

    @property
    def python_version(self) -> str:
        raise NotImplementedError()

    @property
    def venv(self) -> BoundCommand:
        raise NotImplementedError()

    @property
    def pip(self) -> BoundCommand:
        raise NotImplementedError()

    def kill_crossover(self):
        raise NotImplementedError()

    def install(self):
        raise NotImplementedError()

    def uninstall(self):
        raise NotImplementedError()

    def run_crossover(self, background: bool = False):
        raise NotImplementedError()


def restart_required(f):
    @wraps(f)
    def wrapper(self: "Plugin", *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        finally:
            if self.config.crossover_plugin.is_running:
                self.config.crossover_plugin.kill_crossover()
                self.config.crossover_plugin.run_crossover(background=True)

    return wrapper


def save_config(f):
    @wraps(f)
    def wrapper(self: "Plugin", *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        finally:
            self.config.write()

    return wrapper


def get_main_ctx() -> Optional[click.Context]:
    try:
        ctx = click.get_current_context()
        while ctx.parent:
            ctx = ctx.parent
        return ctx
    except RuntimeError:
        return None


def with_status(message: str):
    """Set status message."""

    def decorator(f):
        @wraps(f)
        def wrapper(self: "Plugin", *args, **kwargs):
            self.set_status(message)

            try:
                return f(self, *args, **kwargs)
            finally:
                self.reset_status()

        return wrapper

    return decorator
