
# First collect memory usage

READS_FILE=../ImplementingSearch/data/illumina_reads_100.fasta.gz
REFERENCE_FILE=../ImplementingSearch/data/hg38_partial.fasta.gz
FMINDEX_FILE=test.index

MEM_OUTPUT_FILE=python_memory_benchmark.csv
echo "method,reference_file,reads_file,read_num,mem_usage" > $MEM_OUTPUT_FILE
## Naive search
read_nums=(10)
for read_num in "${read_nums[@]}"
do
	mem_usage=`\time -f "%M"  implementing-search-python naive search --reads $READS_FILE --reference $REFERENCE_FILE --num-reads $read_num 2>&1 | tail -n 1`
	echo "naive,${REFERENCE_FILE},${READS_FILE},${read_num},${mem_usage}" >> $MEM_OUTPUT_FILE
done



## SA search
read_nums=(1000 10000)
for read_num in "${read_nums[@]}"
do
	mem_usage=`\time -f "%M" implementing-search-python suffix_array search --reads $READS_FILE --reference $REFERENCE_FILE --num-reads $read_num  2>&1 | tail -n 1`
	echo "sa,${REFERENCE_FILE},${READS_FILE},${read_num},${mem_usage}" >> $MEM_OUTPUT_FILE
done

## FM search
read_nums=(1000 10000 100000 1000000)
for read_num in "${read_nums[@]}"
do
	mem_usage=`\time -f "%M" implementing-search-python fm_index search --reads $READS_FILE --index $FMINDEX_FILE --num-reads $read_num 2>&1 | tail -n 1`
	echo "fm,${FMINDEX_FILE},${READS_FILE},${read_num},${mem_usage}" >> $MEM_OUTPUT_FILE
done

# remove any old benchmark file
rm python_benchmark.csv

# Now collect processing per read num
implementing-search-python naive search --reads $READS_FILE --reference $REFERENCE_FILE --num-reads 1000
implementing-search-python suffix_array search --reads $READS_FILE --reference $REFERENCE_FILE --num-reads 10011 
implementing-search-python fm_index search --reads $READS_FILE --index $FMINDEX_FILE --num-reads 1000011
