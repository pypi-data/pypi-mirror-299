from pathlib import Path
from typing import Literal

import nest_asyncio
from llama_parse import LlamaParse, ResultType
from rich.console import Console
from rich.panel import Panel

from ak_pdf2md.utils.config_parser import Config

_config = Config()

nest_asyncio.apply()


class LlamaParser:
    VERBOSITY: bool = False
    __console = Console()

    def __init__(self) -> None:
        pass

    def __parser(
        self, result_type: Literal[".md", ".txt"], verbose: bool = VERBOSITY, **kwargs
    ):
        match result_type.casefold():
            case ".md":
                _result_type = ResultType.MD
            case ".txt":
                _result_type = ResultType.TXT
            case _:
                raise Exception(f"{result_type=} not in `Literal['.md', '.txt']`")

        _default_args = {
            "api_key": _config.get(keys=("llamaparse", "apiKey")),
            "result_type": _result_type,
            "verbose": verbose,
            "parsing_instruction": "",
            "skip_diagonal_text": False,
            "do_not_unroll_columns": False,
        }

        for k, v in kwargs:
            _default_args[k] = v

        return LlamaParse(**_default_args)

    def __write(self, dest_path: Path, contents: str) -> Path:
        """Write the contents of markdown document to file"""

        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(contents)
        return dest_path

    def __process_pdf(
        self, pdf_path: Path, result_type: Literal[".md", ".txt"], **kwargs
    ) -> str:
        docs = self.__parser(result_type=result_type, **kwargs).load_data(str(pdf_path))
        return "\n".join([doc.text for doc in docs])

    def convert(
        self,
        filepath: Path,
        dest_dir: Path | None = None,
        extension: Literal[".md", ".txt"] = ".md",
        **kwargs,
    ):
        dest_dir = dest_dir or filepath.parent
        destpath: Path = dest_dir / f"{filepath.stem}{extension}"
        with self.__console.status(
            f"Converting {filepath.name} to {destpath.name}...", spinner="dots"
        ):
            _data = self.__process_pdf(
                pdf_path=filepath, result_type=extension, **kwargs
            )

        self.__write(dest_path=destpath, contents=_data)
        self.__console.print(
            Panel(
                f'[green bold]Contents written to "{str(destpath)}"',
                title="Success",
                border_style="green",
            )
        )


parser = LlamaParser()
