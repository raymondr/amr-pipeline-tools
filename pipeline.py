import readers
import sys

# read input files
name_to_sequence = readers.read_fasta(sys.argv[1])
id_to_name = readers.read_grouping(sys.argv[2])

# create fasta files for each id
readers.create_fasta_file_for_each_id(name_to_sequence, id_to_name, sys.argv[3])

