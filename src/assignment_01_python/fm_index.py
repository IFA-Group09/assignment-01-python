from pathlib import Path

import iv2py as iv
from scipy.spatial import distance

from assignment_01_python.benchmark import Benchmark


def fm_index_search(index_path: Path, reads_path: Path, mismatches: int, num_reads: int, quiet: bool) -> None:
    index = iv.fmindex(path=index_path)
    reads_processed = 0

    benchmark = Benchmark(method="fm_search", reference=index_path, reads=reads_path)
    while reads_processed < num_reads:
        for read in iv.fasta.reader(file=reads_path):
            for result in index.search(read.seq, k=mismatches):
                if not quiet:
                    print(result)
            reads_processed += 1
            if reads_processed % benchmark.interval == 0:
                benchmark.write(reads_processed)
            if reads_processed == num_reads:
                break

def split_read(read: str, pieces: int) -> list[str]:
    piece_size = len(read)//pieces
    first_offset = len(read) % pieces

    piece_list = []

    piece_list.append(read[:piece_size+first_offset])
    for i in range(1, pieces):
        piece_list.append(read[(piece_size*i)+first_offset:(piece_size*i)+first_offset+piece_size])
    return piece_list

def verify(reference: str, read: str, start_pos: int, mismatches: int) -> bool:
    return distance.hamming(list(read), list(reference[start_pos:start_pos+len(read)])) <= mismatches/len(read)

def fm_index_pigeon_search(index_path: Path, reads_path: Path, reference_path: Path, mismatches: int, num_reads: int, quiet: bool) -> None:
    index = iv.fmindex(path=index_path)
    references = [ reference.seq for reference in iv.fasta.reader(file=reference_path) ]


    reads_processed = 0
    benchmark = Benchmark(method="fm_search_pigeon", reference=index_path, reads=reads_path)
    while reads_processed < num_reads:
        for read in iv.fasta.reader(file=reads_path):
            read_parts = split_read(read.seq, mismatches+1)

            piece_size = len(read_parts[-1])
            first_offset = len(read_parts[0]) - piece_size

            match_results = set()
            for read_part_n, read_part in enumerate(read_parts):
                for result in index.search(read_part, k=0):
                    #                   read_part_n  ref_id     match_pos
                    match_results.add( (read_part_n, result[0], result[1]))

            for read_part_n, ref_n, match_pos in match_results:
                if (match_pos-((piece_size*read_part_n)+first_offset)) < 0 or (match_pos + read_part_n*piece_size)+first_offset > len(references[ref_n]):
                    continue

                matched_pieces = 1
                for i in range(read_part_n):
                    offset = piece_size * (read_part_n - i)
                    if i == 0:
                        offset += first_offset

                    if (i, ref_n, match_pos - offset) in match_results:
                        matched_pieces += 1

                for i in range(read_part_n+1, len(read_parts)):
                    if (i, ref_n, match_pos+(piece_size*(i-read_part_n))) in match_results:
                        matched_pieces += 1

                if matched_pieces == len(read_parts):
                    if not quiet:
                        print(f"{read.seq},{(match_pos-((piece_size*read_part_n)+first_offset))}")
                elif matched_pieces == len(read_parts)-1:
                    if verify(reference=references[ref_n], read=read.seq, start_pos=(match_pos-((piece_size*read_part_n)+first_offset)), mismatches=mismatches):
                        if not quiet:
                            print(f"{read.seq},{(match_pos-((piece_size*read_part_n)+first_offset))}")

            reads_processed += 1
            if reads_processed % benchmark.interval == 0:
                benchmark.write(reads_processed)
            if reads_processed == num_reads:
                break

def fm_construct_index(reference_path: Path, output_path: Path) -> None:
    references = [ reference.seq for reference in iv.fasta.reader(file=reference_path) ]
    index = iv.fmindex(reference=references, samplingRate=16)
    index.save(str(output_path))
