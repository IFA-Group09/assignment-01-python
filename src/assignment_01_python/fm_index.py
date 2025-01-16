from pathlib import Path

import iv2py as iv

from assignment_01_python.benchmark import Benchmark


def fm_index_search(index_path: Path, reads_path: Path, mismatches: int, num_reads: int) -> None:
    index = iv.fmindex(path=index_path)
    reads_processed = 0

    benchmark = Benchmark(method="fm_search", reference=index_path, reads=reads_path)
    while reads_processed < num_reads:
        for read in iv.fasta.reader(file=reads_path):
            for result in index.search(read.seq, k=mismatches):
                print(result)
            reads_processed += 1
            if reads_processed % benchmark.interval == 0:
                benchmark.write(reads_processed)
            if reads_processed == num_reads:
                break

def fm_construct_index(reference_path: Path, output_path: Path) -> None:
    references = [ reference.seq for reference in iv.fasta.reader(file=reference_path) ]
    index = iv.fmindex(reference=references, samplingRate=16)
    index.save(str(output_path))
