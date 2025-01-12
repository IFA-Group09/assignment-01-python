from pathlib import Path
import time

import iv2py as iv


def sa_search_naive(sa: list[int], pattern: str, reference: str) -> tuple[int, int] | None:
    min_index = 0
    max_index = len(sa) - 1
    while min_index < max_index:
        c = (min_index + max_index) // 2
        if pattern > reference[sa[c] :]:
            min_index = c + 1
        else:
            max_index = c

    first = min_index
    max_index = len(sa) - 1
    while min_index < max_index:
        c = (min_index + max_index) // 2
        if pattern < reference[sa[c] :]:
            max_index = c
        else:
            min_index = c + 1
    last = max_index
    if first > last or not reference[sa[first] :].startswith(pattern):
        return None
    return first, last


def print_suffixes(sa, reference):
    for v in sa:
        print(reference[v:])


def suffix_array_search(references: Path, reads: Path, num_reads: int = 100, benchmark_path: Path = Path("./python_benchmark.csv")) -> None:
    benchmark_file = open(benchmark_path, "a")
    if benchmark_path.stat().st_size == 0:
        benchmark_file.write("method,reads_file,time,read_n\n")

    start_time = time.time()
    for reference in iv.fasta.reader(file=str(references)):
        reference_text = reference.seq + "$"
        sa = iv.create_suffixarray(reference_text)

        for read_num, read in enumerate(iv.fasta.reader(file=str(reads))):
            if read_num > num_reads:
                break

            if read_num%10 == 0:
                benchmark_file.write(f"sa,{str(reads)},{time.time()-start_time},{read_num}\n")

            res = sa_search_naive(sa=sa, pattern=read.seq, reference=reference_text)
            if res:
                for _ in range(0, res[1] + 1 - res[0]):
                    print(read.seq)
