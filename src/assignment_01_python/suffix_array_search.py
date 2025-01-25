import bisect
from pathlib import Path

import iv2py as iv

from assignment_01_python.benchmark import Benchmark


def sa_search_bisect(sa: list[int], pattern: str, reference: str) -> tuple[int, int] | None:
    l = bisect.bisect_left(sa, pattern, lo=0, hi=len(sa)-1, key=lambda c: reference[c:c+len(pattern)])
    r = bisect.bisect_right(sa, pattern, lo=l, hi=len(sa), key=lambda c: reference[c:c+len(pattern)])

    if not reference[sa[l] :].startswith(pattern):
        return None

    return l,r-1

def sa_search_naive(sa: list[int], pattern: str, reference: str) -> tuple[int, int] | None:
    min_index = 0
    max_index = len(sa)
    while min_index < max_index:
        c = (min_index + max_index) // 2

        if reference[sa[c] : sa[c]+len(pattern)] < pattern:
            min_index = c + 1
        else:
            max_index = c

    first = min_index
    max_index = len(sa)
    while min_index < max_index:
        c = (min_index + max_index) // 2

        if reference[sa[c]:sa[c]+len(pattern)] > pattern:
            max_index = c
        else:
            min_index = c + 1
    last = max_index-1
    if first > last or not reference[sa[first] :].startswith(pattern):
        return None
    return first, last


def print_suffixes(sa, reference):
    for v in sa:
        print(reference[v:])


def suffix_array_search(references: Path, reads: Path, num_reads: int, quiet: bool) -> None:
    reference_text = ""
    for reference in iv.fasta.reader(file=str(references)):
        reference_text += reference.seq
    reference_text += "$"
    construct_benchmark = Benchmark(method="sa_construct", reference=references, reads=Path(""))
    sa = iv.create_suffixarray(reference_text)
    construct_benchmark.write(0)
    benchmark = Benchmark(method="sa", reference=references, reads=reads)
    for read_num, read in enumerate(iv.fasta.reader(file=str(reads))):
        if read_num > num_reads:
            break

        res = sa_search_bisect(sa=sa, pattern=read.seq, reference=reference_text)
        if res:
            for _ in range(res[1] + 1 - res[0]):
                if not quiet:
                    print(read.seq)

        if read_num%benchmark.interval == 0:
            benchmark.write(read_num)

