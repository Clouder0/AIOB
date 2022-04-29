"""The CLI entry for AIOB package."""

from __future__ import annotations

import typer

from aiob.cli import main


if __name__ == "__main__":
    typer.run(main.main)
