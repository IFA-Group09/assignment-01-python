from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from assignment_01_python.fm_index import fm_construct_index, fm_index_pigeon_search, fm_index_search
from assignment_01_python.naive_search import naive_search
from assignment_01_python.suffix_array_search import suffix_array_search

app = typer.Typer()

naive_app = typer.Typer()
app.add_typer(naive_app, name="naive")

sa_app = typer.Typer()
app.add_typer(sa_app, name="suffix_array")

fm_index_app = typer.Typer()
app.add_typer(fm_index_app, name="fm_index")


@naive_app.command("search")
def naive_search_cmd(
reference: Annotated[Path, typer.Option(help="Path to a reference genome in FASTA format (may be compressed)")],
reads: Annotated[Path, typer.Option(help="Path to reads in FASTA format (may be compressed)")],
num_reads: Annotated[Optional[int], typer.Option(help="Number number of reads to use")] = 100,
):
    naive_search(references=reference, reads=reads, num_reads=num_reads)

@sa_app.command("search")
def sa_search_cmd(
reference: Annotated[Path, typer.Option(help="Path to a reference genome in FASTA format (may be compressed)")],
reads: Annotated[Path, typer.Option(help="Path to reads in FASTA format (may be compressed)")],
num_reads: Annotated[Optional[int], typer.Option(help="Number number of reads to use")] = 100,
):
    suffix_array_search(references=reference, reads=reads, num_reads=num_reads)

@fm_index_app.command("construct")
def fm_index_construct_cmd(
        reference: Annotated[Path, typer.Option(help="Path to a reference genome in FASTA format (may be compressed)")],
        output: Annotated[Path, typer.Option(help="Path to save constructed FM index")],
):
    fm_construct_index(reference_path=reference, output_path=output)

@fm_index_app.command("search")
def fm_index_search_cmd(
        index: Annotated[Path, typer.Option(help="Path to a FM index")],
        reads: Annotated[Path, typer.Option(help="Path to reads in FASTA format (may be compressed)")],
        num_reads: Annotated[int, typer.Option(help="Number number of reads to use")] = 100,
        reference: Annotated[Optional[Path], typer.Option(help="Path to a reference genome in FASTA format (may be compressed)")] = None,
        mismatches: Annotated[int, typer.Option(help="Number of mismatches to allow")] = 0,
        use_pigeon: Annotated[bool, typer.Option(help="Use pigeonhole principle for inexact search")] = False,
):
    if use_pigeon:
        if not reference:
            print("Must specify reference if using `use_pigeon`")
            return
        fm_index_pigeon_search(index_path=index, reads_path=reads, mismatches=mismatches, num_reads=num_reads, reference_path=reference)
    else:
        fm_index_search(index_path=index, reads_path=reads, mismatches=mismatches, num_reads=num_reads)

def run() -> None:
    app()
