from pathlib import Path
import time

import iv2py as iv


def naive_search(references: Path, reads: Path, num_reads: int = 100, benchmark_path: Path = Path("./python_benchmark.csv")) -> None:
    benchmark_file = open(benchmark_path, "a")
    if benchmark_path.stat().st_size == 0:
        benchmark_file.write("method,reads_file,time,read_n\n")

    start_time = time.time()
    for reference in iv.fasta.reader(file=references):
        for read_num, read in enumerate(iv.fasta.reader(file=reads)):
            if read_num > num_reads:
                break

            if read_num%10 == 0:
                benchmark_file.write(f"naive,{str(reads)},{time.time()-start_time},{read_num}\n")

            start = reference.seq.find(read.seq)
            while start != -1:
                print(read.seq)
                start += len(read.seq)
                start = reference.seq.find(read.seq, start)
