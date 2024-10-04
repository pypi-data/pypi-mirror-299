from pathlib import Path
from typing import Any, ClassVar, Dict

import click
from click import Group
from pydantic import BaseModel, Field

from cx_tool.plugin.completions import CompletionsPlugin
from cx_tool.plugin.deps import DepsPlugin
from cx_tool.plugin.bottle import BottlePlugin
from cx_tool.plugin.dxvk import DXVKPlugin
from cx_tool.plugin.fastmath import FastMathPlugin
from cx_tool.plugin.linux import LinuxPlugin
from cx_tool.plugin.mac import MacPlugin
from cx_tool.plugin.plist import PListPlugin
from cx_tool.plugin.plugin import Plugin
from cx_tool.plugin.ue4 import UE4Plugin
from cx_tool.plugin.reset import ResetPlugin
from cx_tool.plugin.steam import SteamPlugin


class UtilConfig(BaseModel):
    plugins: Dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Installed plugins"
    )

    plugins_data: Dict[str, Any] = Field(
        default_factory=dict, description="Plugins Data"
    )

    CONFIG_PATH: ClassVar[Path] = Path("~/.cx-tool/config.json").expanduser()
    PLUGIN_CLI: ClassVar[Group] = Group("plugin")

    @property
    def plugin_cli(self):
        return self.PLUGIN_CLI

    @property
    def crossover_plugin(self):
        plugin = Plugin.get_plugin("crossover")
        if plugin is None:
            raise click.UsageError("Unsupported platform.")
        return plugin

    @staticmethod
    def _sort_plugins_by_depends(plugins):
        """Plugins that are dependent on other plugins should be loaded after."""

        added_plugins = Plugin.get_all_running_plugins()

        ok_plugins = [p for p in plugins if not p.requires]
        dependant_plugins = [p for p in plugins if p.requires]

        for plugin in dependant_plugins:
            if not set(
                [p.name for p in [*ok_plugins, *dependant_plugins, *added_plugins]]
            ) & set(plugin.requires):
                plugin.console_log(
                    f"Plugin {plugin.name} requires {plugin.requires}. It will not be loaded.",
                    err=True,
                )
                dependant_plugins.remove(plugin)

        while dependant_plugins:
            ok_plugin_names = [p.name for p in [*ok_plugins, *added_plugins]]
            for plugin in dependant_plugins:
                if all(dep in ok_plugin_names for dep in plugin.requires):
                    ok_plugins.append(plugin)
                    dependant_plugins.remove(plugin)

        return ok_plugins

    def init_plugins(self):
        """Initialize plugins."""

        Plugin.add_plugin(DepsPlugin(self))  # Ensure deps are installed

        builtin_plugins = [
            MacPlugin,
            LinuxPlugin,
            DXVKPlugin,
            FastMathPlugin,
            UE4Plugin,
            PListPlugin,
            ResetPlugin,
            SteamPlugin,
            BottlePlugin,
            CompletionsPlugin,
        ]

        self._sort_plugins_by_depends(builtin_plugins)

        for plugin in builtin_plugins:
            Plugin.add_plugin(plugin(self))

        # Load deps plugin
        Plugin.get_plugin("deps").on_load()

        Plugin.import_plugins(self)

        for plugin in self._sort_plugins_by_depends(Plugin.get_all_running_plugins()):
            plugin.on_load()

    @classmethod
    def read(cls) -> "UtilConfig":
        try:
            with open(cls.CONFIG_PATH, "r") as file:
                data = file.read() or "{}"
        except FileNotFoundError:
            data = "{}"

        return cls.model_validate_json(data)

    def write(self):
        """Write the config to disk."""

        config_path = Path("~/.cx-tool/config.json").expanduser()

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True)

        with open(config_path, "w") as file:
            file.write(self.model_dump_json(by_alias=True, indent=2))

    def get_plugin_data(self, plugin: "Plugin") -> Dict[str, Any]:
        self.plugins_data.setdefault(plugin.name, {})

        return self.plugins_data[plugin.name]


config = UtilConfig.read()
