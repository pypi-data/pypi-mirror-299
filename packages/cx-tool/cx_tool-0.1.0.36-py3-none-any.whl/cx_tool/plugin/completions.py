import inspect
import os
import sys
import time
from functools import cached_property
from pathlib import Path
from typing import List

import click
from click import Context
from plumbum.cmd import cp
from rich.table import Table

from cx_tool.plugin.plugin import Plugin, clickable, with_status


class CompletionsPlugin(Plugin):
    """Manage cx-tool completions for your shell."""

    name = "completions"

    @cached_property
    def backups_group(self):
        return self.cli.group(
            "shell-backups", help="Manage shell configuration backups."
        )(lambda: None)

    @staticmethod
    def get_script_name(ctx: Context | None = None) -> str:
        """Get the script name from the context."""

        if ctx is None:
            return sys.argv[0].split("/")[-1]

        while ctx.parent is not None:
            ctx = ctx.parent

        return ctx.info_name

    def get_shell_info(
        self, script_name, shell="autodetect"
    ) -> tuple[Path, str, Path, str]:
        """Detect the current shell and source file and completion command."""

        supported_shells = ["bash", "zsh", "fish"]

        real_script_name = script_name
        script_name = script_name.replace("-", "_")
        command_name = script_name.upper()

        if shell == "autodetect":
            self.console_log("Detecting shell...")

            shell = os.environ.get("SHELL", "").split("/")[-1]

            self.console_log(
                f"Detected shell: {shell}", err=shell not in supported_shells
            )

        rc_path = None
        rc_command = None
        script_rc_path = None

        if shell == "bash":
            rc_path = Path("~/.bashrc")
            script_rc_command = (
                f'eval "$(_{command_name}_COMPLETE=zsh_source {real_script_name})"'
            )
        elif shell == "zsh":
            rc_path = Path("~/.zshrc")
            script_rc_command = (
                f'eval "$(_{command_name}_COMPLETE=zsh_source {real_script_name})"'
            )
        elif shell == "fish":
            script_rc_path = Path(f"~/.config/fish/completions/{script_name}.fish")
            script_rc_command = (
                f"_{command_name}_COMPLETE=fish_source {real_script_name} | source"
            )
        else:
            raise click.UsageError(f"Unsupported shell {shell}")

        script_rc_command = inspect.cleandoc(
            f"""
            # {real_script_name} completion
            if command -v {real_script_name} &>/dev/null; then {script_rc_command}; fi
            """
        )

        if shell in ["bash", "zsh"]:
            script_rc_path = Path(f"{rc_path}_{script_name}_completions")
            rc_command = f"source {script_rc_path}"

        return rc_path, rc_command, script_rc_path, script_rc_command

    def create_rc_backup(self, rc_path: Path):
        """Create a backup of the shell configuration file."""

        backup_path = f"{rc_path}.backup{int(time.time())}"
        self.console_log("Creating backup file...")
        cp[rc_path.expanduser(), backup_path]()
        self.console_log(f"Shell configuration backed up to {backup_path}")

    @click.argument(
        "shell",
        type=click.Choice(["bash", "zsh", "fish", "autodetect"]),
        default="autodetect",
    )
    @Plugin.pass_click_context
    @clickable
    def enable_completions(self, ctx: Context, shell: str):
        """Generate bash completions for the CLI."""

        script_name = self.get_script_name(ctx)

        rc_path, rc_command, script_rc_path, script_rc_command = self.get_shell_info(
            script_name, shell=shell
        )

        self.console_log(f"Creating completions script for `{script_name}`...")

        with open(script_rc_path.expanduser(), "w") as f:
            f.write(script_rc_command)

        self.console_log(
            f"Completions script created for `{script_name}` at {script_rc_path}"
        )

        if rc_path is not None and rc_command is not None:
            self.create_rc_backup(rc_path.expanduser())

            with open(rc_path.expanduser(), "r") as f:
                rc_text = f.read()

            if rc_command in rc_text:
                self.console_log(
                    f"Completions already enabled for `{script_name}` in {rc_path}"
                )
            else:
                with open(rc_path.expanduser(), "a") as f:
                    f.write(f"\n{rc_command}\n")

                self.console_log(f"Completions enabled for {script_name}")

        help_msg = "To enable completions use `{cmd}`"
        cmd = f"source {rc_path}"

        self.console_log(f"{help_msg.format(cmd=cmd)}")

    @click.argument(
        "shell",
        type=click.Choice(["bash", "zsh", "fish", "autodetect"]),
        default="autodetect",
    )
    @Plugin.pass_click_context
    @clickable
    def completions_disable(self, ctx: Context, shell: str):
        """Disable completions for the CLI."""

        rc_path, rc_command, script_rc_path, script_command = self.get_shell_info(
            self.get_script_name(ctx), shell=shell
        )

        if script_rc_path.exists():
            self.create_rc_backup(script_rc_path.expanduser())

        self.console_log("Looking for completions in shell configuration...")

        if rc_path is not None and rc_command is not None:
            self.create_rc_backup(rc_path.expanduser())

            with open(rc_path.expanduser(), "r") as rc_read_file:
                text = ""

                for line in rc_read_file.readlines():
                    if script_command in line:
                        self.console_log(
                            "Found completions command in shell configuration"
                        )
                    else:
                        text += line

                with open(rc_path.expanduser(), "w") as rc_write_file:
                    rc_write_file.write(text)

        self.console_log("Completions disabled in shell configuration")

    def get_backups(self, shell: str) -> List[Path]:
        """Get all shell configuration backups."""

        rc_path, *_ = self.get_shell_info(self.get_script_name(), shell=shell)

        pattern = fr"{rc_path.name}.backup*"

        backups = list(Path("~").expanduser().glob(pattern))
        backups.sort(key=os.path.getmtime, reverse=True)

        return backups

    @click.option(
        "--keep-limit", type=int, default=10, help="Number of backups to keep."
    )
    @click.option(
        "--shell",
        type=click.Choice(["bash", "zsh", "fish", "autodetect"]),
        default="autodetect",
    )
    @clickable
    @with_status("Deleting shell configuration backups...")
    def backups_delete(self, keep_limit: int, shell: str):
        """Delete all shell configuration backups."""

        for backup in self.get_backups(shell)[keep_limit:]:
            self.console_log(f"Deleting {backup}...")
            backup.unlink()

    @click.option("--shell", type=click.Choice(["bash", "zsh", "fish", "autodetect"]), default="autodetect")
    @clickable
    def list_backups(self, shell: str):
        """List all shell configuration backups."""

        table = Table(title="Shell Configuration Backups", show_header=True, header_style="bold magenta")

        table.add_column("Backup", max_width=30)
        table.add_column("Time", max_width=30)

        for backup in self.get_backups(shell):
            path = str(backup).replace(str(Path("~").expanduser()), "~")
            table.add_row(path, time.ctime(backup.stat().st_mtime))

        self.console.print(table)

    def on_load(self):
        self.cli_command("enable", no_args_is_help=False)(self.enable_completions)
        self.cli_command("disable", no_args_is_help=False)(self.completions_disable)

        self.cli_command("delete", self.backups_group, no_args_is_help=False)(
            self.backups_delete
        )
        self.cli_command("list", self.backups_group, no_args_is_help=False)(self.list_backups)
