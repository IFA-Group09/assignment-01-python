from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from assignment_01_python.naive_search import naive_search
from assignment_01_python.suffix_array_search import suffix_array_search


class SearchMethod(str, Enum):
    naive = "naive"
    suffix_array = "suffix_array"


def main(
    reference: Annotated[Path, typer.Option(help="Path to a reference genome in FASTA format (may be compressed)")],
    reads: Annotated[Path, typer.Option(help="Path to reads in FASTA format (may be compressed)")],
    search_method: Annotated[SearchMethod, typer.Option(help="Search method to use")] = SearchMethod.naive,
    num_reads: Annotated[Optional[int], typer.Option(help="Number number of reads to use")] = 100,
):
    if search_method is SearchMethod.naive:
        naive_search(references=reference, reads=reads, num_reads=num_reads)
    else:
        suffix_array_search(references=reference, reads=reads, num_reads=num_reads)


def run() -> None:
    typer.run(main)
