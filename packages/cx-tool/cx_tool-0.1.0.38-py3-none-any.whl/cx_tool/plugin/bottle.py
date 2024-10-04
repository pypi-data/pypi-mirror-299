import sys
import typing
from functools import cached_property
from pathlib import Path
from typing import List
import configparser


import click
from plumbum import ProcessExecutionError
from rich.console import Console

from cx_tool.plugin.plugin import Plugin, clickable
from rich.table import Table

if typing.TYPE_CHECKING:
    from cx_tool.plugin.wine import WinePlugin


class BottlePlugin(Plugin):
    """Plugin to manage bottles."""

    name = "bottle"
    requires = ["wine"]

    @cached_property
    def wine(self) -> "WinePlugin":
        return Plugin.get_plugin("wine")

    @property
    def bottles(self) -> List[Path]:
        bottles_path: Path = self.config.crossover_plugin.bottles_path

        return [
            item
            for item in bottles_path.iterdir()
            if item.is_dir() and item.joinpath("cxbottle.conf").exists()
        ]

    @staticmethod
    def get_bottle_config(
        bottle_path: Path, conf_name: str
    ) -> configparser.ConfigParser:
        """Get bottle config."""

        config = configparser.ConfigParser()
        config.read(bottle_path.joinpath(conf_name))

        return config

    @property
    def bottle_names(self) -> List[str]:
        return [bottle.name for bottle in self.bottles]

    def bottle_cli_group(self, name: str):
        """Create bottle cli group."""

        if self.cli.commands.get(name):
            return self.cli.commands[name]

        return self.cli.group(name, help=f"`{name}` bottle tools and settings")(
            lambda: None
        )

    def get_bottle_path(self, name: str):
        """Get bottle by name."""

        for bottle in self.bottles:
            if bottle.name == name:
                return bottle

        raise click.UsageError(f"Bottle {name} not found.")

    @clickable
    def list(self):
        """List all bottles."""

        table = Table(title="Bottles", show_header=True, header_style="bold magenta")

        console = Console()
        console.print(table)

    @click.option("--edit", is_flag=True, help="Edit the bottle configuration file.")
    @clickable
    def show_conf(self, bottle_path: Path, conf_name: str, edit: bool):
        """Open bottle configuration file."""

        if edit:
            return click.edit(
                filename=bottle_path.joinpath(conf_name), require_save=False
            )

        conf = self.get_bottle_config(bottle_path, conf_name)
        console = Console()

        for section in conf.sections():
            table = Table(
                title=f"{bottle_path.name}/{conf_name}/{section}",
                show_header=True,
                header_style="bold magenta",
            )

            table.add_column("Key")
            table.add_column("Value")

            for key, value in conf[section].items():
                table.add_row(key, value)

            console.print(table)

    @click.argument("cmd")
    @clickable
    def run(self, bottle: str, cmd: str, arguments: str | None = None):
        """Run command in the bottle."""

        try:
            self.wine.run(cmd, bottle=bottle, arguments=arguments).run(
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin,
            )
        except ProcessExecutionError as e:
            sys.exit(e.retcode)

    def on_load(self):
        for bottle in self.bottles:
            conf_group = self.bottle_cli_group(bottle.name).group(
                "conf", help="Manage bottle conf " "files"
            )(lambda: None)

            self.cli_command("cxbottle", conf_group, no_args_is_help=False)(
                self.show_conf.partial(bottle_path=bottle, conf_name="cxbottle.conf")
            )
            self.cli_command("cxassoc", conf_group, no_args_is_help=False)(
                self.show_conf.partial(bottle_path=bottle, conf_name="cxassoc.conf")
            )
            self.cli_command("cxmenu", conf_group, no_args_is_help=False)(
                self.show_conf.partial(bottle_path=bottle, conf_name="cxmenu.conf")
            )

            self.cli_command(
                "run",
                self.bottle_cli_group(bottle.name),
                no_args_is_help=False,
            )(self.run.partial(bottle=bottle.name))
