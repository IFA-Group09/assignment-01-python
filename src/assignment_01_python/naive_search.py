from pathlib import Path

import iv2py as iv

from assignment_01_python.benchmark import Benchmark


def naive_search(references: Path, reads: Path, num_reads: int = 100, benchmark_path: Path = Path("./python_benchmark.csv")) -> None:
    benchmark = Benchmark(method="naive", reads=reads)
    for reference in iv.fasta.reader(file=references):
        for read_num, read in enumerate(iv.fasta.reader(file=reads)):
            if read_num > num_reads:
                break

            if read_num % benchmark.interval == 0:
                benchmark.write(read_num)

            start = reference.seq.find(read.seq)
            while start != -1:
                print(read.seq)
                start += len(read.seq)
                start = reference.seq.find(read.seq, start)
