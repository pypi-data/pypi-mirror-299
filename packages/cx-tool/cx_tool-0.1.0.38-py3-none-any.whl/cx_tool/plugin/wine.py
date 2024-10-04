from functools import cached_property

from plumbum import local
from plumbum.commands.base import BoundCommand

from cx_tool.plugin import Plugin


class WinePlugin(Plugin):
    """Wine tools."""

    name = "wine"
    requires = ["crossover"]

    @cached_property
    def wine(self) -> BoundCommand:
        return local.get(self.config.crossover_plugin.BIN_PATH.joinpath("wine"))

    def run(
        self,
        cmd: str,
        arguments: str | None = None,
        bottle: str | None = None,
    ) -> BoundCommand:
        """Run wine command."""

        wine = self.wine

        if bottle is not None:
            wine = wine["--bottle", bottle]

        wine = wine["--cx-app"][cmd]

        if arguments is not None:
            wine = wine[arguments]

        return wine
