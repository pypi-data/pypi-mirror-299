import plistlib
from functools import cached_property
from pathlib import Path
from typing import Any

import click

from cx_tool.plugin.plugin import Platform, Plugin, clickable, with_status


class PListPlugin(Plugin):
    """Plugin to manage macOS CrossOver plist file."""

    name = "plist"
    platforms = [Platform.macos]

    PLIST_PATH = Path(
        "~/Library/Preferences/com.codeweavers.CrossOver.plist"
    ).expanduser()

    @cached_property
    @with_status("Loading plist data...")
    def plist_data(self):
        return plistlib.loads(self.PLIST_PATH.read_bytes())

    @with_status("Saving plist data...")
    def save_plist_data(self):
        self.PLIST_PATH.write_bytes(plistlib.dumps(self.plist_data))

    @click.argument("key")
    @click.argument("value")
    @clickable
    def set(self, key: str, value: Any):
        """Set a key value pair in the plist."""

        if value is not None:
            self.plist_data[key] = value
        else:
            del self.plist_data[key]

        self.save_plist_data()

        self.console_log(f"Set {key} to {value}.")

    @click.argument("key")
    @clickable
    def get(self, key):
        """Get a value from the plist."""

        self.console_log(f"{key}: {self.plist_data.get(key)}")

    def on_load(self):
        self.cli_command("set")(self.set)
        self.cli_command("get")(self.get)
