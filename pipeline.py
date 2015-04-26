import readers
import sys

def create_fasta_file_for_each_id(name_to_sequence, id_to_name):
    for k, v in id_to_name.items():
        filename = ''.join(k.split(':'))
        with open('seq/%s.fa' % filename, 'w+') as fasta:
            for name in v:
                fasta.write('>%s\n' % name)
                fasta.write(name_to_sequence[name] + '\n')

# read input files
name_to_sequence = readers.read_fasta(sys.argv[1])
id_to_name = readers.read_grouping(sys.argv[2])

# create fasta files for each id
create_fasta_file_for_each_id(name_to_sequence, id_to_name)

# run clustering program on each fasta file to gauge how similar the sequences are
#cluster_fasta_files(id_to_name)

