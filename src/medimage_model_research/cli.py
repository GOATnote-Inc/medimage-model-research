"""Command-line entry point: medimage-model-research <command>."""

from __future__ import annotations

import click

import medimage_model_research


@click.group()
@click.version_option(medimage_model_research.__version__, prog_name="medimage-model-research")
def main() -> None:
    """medimage-model-research — NC-constrained research-track model."""


@main.command()
def smoke() -> None:
    """Verify package imports."""
    click.echo(f"medimage-model-research {medimage_model_research.__version__} OK")


if __name__ == "__main__":
    main()
