from pathlib import Path
from typing import Literal

import typer
from rich.console import Console

from ak_pdf2md.parser import parser

app = typer.Typer()
console = Console()
test = typer.Typer()


def get_filepath(filepath: str | Path | None) -> Path:
    while True:
        if filepath is None:
            filepath = input("Enter the PDF filepath: ")

        filepath = _strip_filepath(filepath)

        if filepath.suffix.casefold() != ".pdf":
            console.print(f'[red]{filepath.suffix=} does not match ".pdf"')
            filepath = None
            continue

        if filepath.is_file():
            return filepath
        else:
            console.print(f"[red]Specified file {filepath} does not exist.")
            filepath = None
            continue


def _strip_filepath(filepath: str | Path) -> Path:
    """Strip extra quotes from filepaths"""
    filepath = str(filepath)
    remove_chars = ("'", '"')
    for char in remove_chars:
        filepath = filepath.strip(char).strip()
    return Path(filepath)


@app.command()
def convert_pdf(
    filepath: str = "",
    dest_dir: str = "",
    markdown_output: bool = True,
):
    """convert pdf file to markdown"""
    if filepath == "":
        filepath = None  # type: ignore
    if dest_dir == "":
        dest_dir = None  # type: ignore
    _filepath: Path = get_filepath(filepath)

    if dest_dir is not None:
        dest_dir = _strip_filepath(dest_dir)  # type: ignore

    ext = ".md" if markdown_output else ".txt"
    parser.convert(filepath=_filepath, dest_dir=dest_dir, extension=ext)


@test.command()
def test_config():
    from ak_pdf2md import test_configs

    test_configs()
