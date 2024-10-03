import sys
import argparse

import time
from rich.console import Console, RenderableType

from rich.padding import Padding
from rich.style import Style
from rich.text import Text

from rich.progress import (
    Progress,
    RenderableColumn,
)


console = Console()


# define styles for heading and list items
kelvin_logo = Style(color="green", bold=True)
experiment_style = Style(color="yellow", bold=True)
file_style = Style(color="cyan", bold=True)
cmd_style = Style(color="bright_magenta", bold=True)


def pad(item: RenderableType, ntabs: int = 1) -> RenderableType:
    return Padding(item, (0, 0, 0, ntabs * 4))


# create heading with style
heading = Text("Kelvin: ", style=kelvin_logo)


def main():
    args = parse_args()
    args.func(args)


def run_alias():
    run_parser = argparse.ArgumentParser()
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER)

    run(run_parser.parse_args())


def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    show_parser = commands.add_parser("show")
    show_parser.set_defaults(func=show)
    show_parser.add_argument("experiment", help="Name of experiment to show.")

    list_parser = commands.add_parser("list")
    list_parser.set_defaults(func=list_experiments)

    create_parser = commands.add_parser("create")
    create_parser.set_defaults(func=create)
    create_parser.add_argument("experiment", help="Name of experiment to create.")

    lock_parser = commands.add_parser("lock")
    lock_parser.set_defaults(func=lock)

    load_parser = commands.add_parser("load")
    load_parser.set_defaults(func=load)
    load_parser.add_argument("experiment", help="Name of experiment to load.")

    link_parser = commands.add_parser("link")
    link_parser.set_defaults(func=link)
    link_parser.add_argument("experiment", help="Name of experiment to link.")

    run_parser = commands.add_parser("run")
    run_parser.set_defaults(func=run)
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER)

    restore_parser = commands.add_parser("restore")
    restore_parser.set_defaults(func=restore)

    sync_parser = commands.add_parser("sync")
    sync_parser.set_defaults(func=sync)

    generate_parser = commands.add_parser("generate")
    generate_parser.set_defaults(func=generate)
    generate_parser.add_argument("template", help="Path to template.")

    return parser.parse_args()


def init(_: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "initialised.")
    console.print(msg)


def show(args: argparse.Namespace) -> None:
    msg = Text.assemble(
        heading, "showing ", (f"{args.experiment}", experiment_style), "."
    )
    console.print(msg)
    console.print(pad(Text("Here is some metadata.")))


def list_experiments(_: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "listing experiments:")
    console.print(msg)

    for i in range(1, 3 + 1):
        console.print(
            pad(Text.assemble(f"{i:0d}. ", ("experiment.", experiment_style)))
        )


def create(args: argparse.Namespace) -> None:
    msg = Text.assemble(
        heading, "created ", (f"{args.experiment}", experiment_style), "."
    )
    console.print(msg)


def lock(_: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "locked experiment.")
    console.print(msg)


def load(args: argparse.Namespace) -> None:
    msg = Text.assemble(
        heading, "loading ", (f"{args.experiment}", experiment_style), "."
    )
    console.print(msg)


def link(_: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "linking ", (f"{sys.argv}", experiment_style), ".")
    console.print(msg)


def run(args: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "running ", (f"{' '.join(args.cmd)}", cmd_style), ".")
    console.print(msg)


def restore(_: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "restored working directory.")
    console.print(msg)


def sync(_: argparse.Namespace) -> None:
    msg = Text.assemble(heading, "syncing with remote.")
    console.print(msg)

    with Progress(
        RenderableColumn(
            Text.assemble(heading, ("syncing: ", Style(color="red", bold=True)))
        ),
        *Progress.get_default_columns(),
    ) as progress:
        task1 = progress.add_task("", total=100)

        while not progress.finished:
            progress.update(task1, advance=1.0)
            time.sleep(0.02)


def generate(args: argparse.Namespace) -> None:
    msg = Text.assemble(
        heading,
        "generating directory structure from ",
        (f"{args.template}", file_style),
        ".",
    )
    console.print(msg)
