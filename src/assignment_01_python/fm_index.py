from pathlib import Path

import iv2py as iv


def fm_index_search(index_path: Path, reads_path: Path, mismatches: int) -> None:
    index = iv.fmindex.load(path=index_path)
    for read in iv.fasta.reader(file=reads_path):
        for result in index.search(read.seq, k=mismatches):
            print(result)

def fm_construct_index(reference_path: Path, output_path: Path) -> None:
    references = [ reference.seq for reference in iv.fasta.reader(file=reference_path) ]
    index = iv.fmindex(reference=references, samplingRate=16)
    index.save(str(output_path))
