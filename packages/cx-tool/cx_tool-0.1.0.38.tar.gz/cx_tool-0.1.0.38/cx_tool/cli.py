import click
from click import Context

from cx_tool.config import config


@click.group
@click.option("-s", "--silent", is_flag=True, help="Silent mode.")
@click.pass_context
def cli(ctx: Context, silent: bool):
    """CrossOver CLI."""

    if ctx.invoked_subcommand is None:
        config.crossover_plugin.run_crossover()


@cli.command(
    "run",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
def run():
    """Run CrossOver."""

    config.crossover_plugin.run_crossover(background=True)


@cli.command("install")
def install():
    """Inject self as the CrossOver process."""

    config.crossover_plugin.install()


@cli.command("uninstall")
def uninstall():
    """Restore the original CrossOver process."""

    config.crossover_plugin.uninstall()


def main():
    config.init_plugins()

    for name, command in config.plugin_cli.commands.items():
        cli.add_command(command, name=name)

    cli()


if __name__ == "__main__":
    run()
