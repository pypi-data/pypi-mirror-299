import click

from cx_tool.plugin.plugin import (
    Plugin,
    clickable,
    restart_required,
    save_config,
)
from cx_tool.plugin.context import PluginContext


class DXVKPlugin(Plugin):
    """Plugin to manage DXVK."""

    name = "dxvk"

    @property
    def async_enabled(self):
        return self.data.get("async", False)

    @clickable
    @restart_required
    @save_config
    def enable_async(self):
        """Enable async compute."""

        self.data["async"] = True

        self.console_log("Async compute enabled.")

    @clickable
    @restart_required
    @save_config
    def disable_async(self):
        """Disable async compute."""

        self.data.pop("async", None)

        self.console_log("Async compute disabled.")

    def on_load(self):
        self.cli_command("enable-async")(self.enable_async)
        self.cli_command("disable-async")(self.disable_async)

    def on_start(self, ctx: "PluginContext"):
        if self.async_enabled:
            ctx.environment["DXVK_ASYNC"] = "1"
