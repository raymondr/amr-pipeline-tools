# reads a fasta file and generates the set of kmers. These kmers are mapped back to the gene they are based on

import argparse
import collections
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import DNAAlphabet
import evaluate_bait


def kmers(seq,k):
    if len(seq) < k:
        print("Error kmer too short")
        yield seq
    for i in range(len(seq)-k+1):
        yield seq[i:i+k]


def main():
    parser = argparse.ArgumentParser(description="Reads a fasta file and generates the set of kmers.")
    parser.add_argument('-k', dest='k', default=120,
                        help='The length of the kmers')
    parser.add_argument('-i', dest='input_file', required=True,
                        help='The name of the input fasta file')
    parser.add_argument('-r', dest='reverse', default=False, action='store_true',
                        help='Whether to generate reverse complement kmers as well')
    #parser.add_argument('-o', dest='output_dir', required=True,
    #                    help='The directory in which to write output files')
    args = parser.parse_args()

    reads = list(SeqIO.parse(open(args.input_file), format='fasta'))
    kmer_count = collections.defaultdict(list)
    total_kmers = 0
    for idx, read in enumerate(reads):
        for kmer in kmers(read.seq, int(args.k)):
                kmer_count[str(kmer)].append(idx)
                total_kmers += 1
    print(len(kmer_count), total_kmers)

    # collapse kmers
    items = list(kmer_count.items())
    items.sort(key=lambda l: len(l[1]), reverse=True)

    with open("bait.fasta", "w") as f:
        for k in kmer_count.keys():
            f.write(k + '\n')
            if args.reverse:
                f.write(str(Seq(k, DNAAlphabet()).reverse_complement()) + '\n')


if __name__ == '__main__':
    main()