import readers
import sys


# read input files
name_to_sequence, name_map = readers.read_fasta(sys.argv[1], shorten=True)
id_to_name = readers.read_cluster(sys.argv[2])

# create fasta files for each id
readers.create_fasta_file_for_each_id(name_to_sequence, id_to_name, sys.argv[3], name_map)

