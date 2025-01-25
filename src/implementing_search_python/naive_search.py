from pathlib import Path

import iv2py as iv

from implementing_search_python.benchmark import Benchmark


def naive_search(references: Path, reads: Path, num_reads: int, quiet: bool) -> None:
    benchmark = Benchmark(method="naive", reference=references, reads=reads)
    for read_num, read in enumerate(iv.fasta.reader(file=reads)):
        if read_num > num_reads:
            break
        for reference in iv.fasta.reader(file=references):
            start = reference.seq.find(read.seq)
            while start != -1:
                if not quiet:
                    print(read.seq)
                start += len(read.seq)
                start = reference.seq.find(read.seq, start)

        if read_num % benchmark.interval == 0:
            benchmark.write(read_num)
