"""
Sends a command to the application.

For now accepts only incomes and expenses:
- incomes are written in format "+<float> <comment?>"
- expenses are written in format "<float> <category> <comment?>"

Accepted command flags (all are optional):
    -d:
        Set date in format %Y-%m-%d (1989 C standard). By default the current
        date is taken (from host computer).

Also, temporarily, all this program does is to convert incoming commands to
dated commands and write them to a file (in append mode). In future the
full-working application can retrieve it's state from such file.

The file has a special (another one) extension called "cnbx" which
stands for CommandBox.

Note that currently input command checking and exception throwing is very raw,
so be careful what you're typing.
"""
import argparse
from datetime import datetime
import os
from pathlib import Path
import re

from loguru import logger as Log

from src.environ import Environ
from src.errors import EnvironError


def main():
    try:
        output_dir_environ: str | None = os.environ[Environ.OUTPUT_DIR.value]
    except KeyError as error:
        raise EnvironError(
            f"please define environ {Environ.OUTPUT_DIR.value}"
        ) from error
    else:
        output_dir: Path = Path(output_dir_environ)
        command: str = _get_cli_command()
        _execute(command, output_dir)


def _execute(command: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path: Path = Path(
        output_dir,
        "state.cnbx"
    )

    existing_date_match: re.Match | None = re.search(
        r"-d\s\d{4}-\d{2}-\d{2}",
        command
    )

    dated_command: str
    if existing_date_match is not None:
        dated_command = command
    else:
        current_date_str: str = datetime.now().strftime(r"%Y-%m-%d")
        dated_command = command + " -d " + current_date_str

    with open(output_path, "a") as f:
        Log.info(f"write command={dated_command}, path={output_path}")
        f.write(dated_command + "\n")


def _get_cli_command() -> str:
    return _parse_args().command


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sends a command to the application."
    )

    parser.add_argument(
        "command",
        type=str,
        help="a complete command string"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
