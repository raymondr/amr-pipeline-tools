# reads a fasta file and generates the set of kmers. These kmers are mapped back to the gene they are based on

import argparse
import collections
from Bio import SeqIO
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
    #parser.add_argument('-o', dest='output_dir', required=True,
    #                    help='The directory in which to write output files')
    args = parser.parse_args()

    reads = list(SeqIO.parse(open(args.input_file), format='fasta'))
    kmer_count = collections.defaultdict(list)
    total_kmers = 0
    for idx, read in enumerate(reads):
        for kmer in kmers(read.seq, args.k):
                kmer_count[str(kmer)].append(idx)
                total_kmers += 1
    print(len(kmer_count), total_kmers)

    # collapse kmers
    items = list(kmer_count.items())
    items.sort(key=lambda l: len(l[1]), reverse=True)
    for i1 in range(len(items)-1):
        for i2 in range(i1+1, len(items)):
            """
            item1 = items[i1]
            item2 = items[i2]
            if item1 and item2 and evaluate_bait.match(item1[0], item2[0]):
                kmer_count[item1[0]].append(item2[1])
                del kmer_count[item2[0]]
                items[i2] = None
            """
            pass
        print(i1)

    with open("bait.fasta", "w") as f:
        for k in kmer_count.keys():
            f.write(k + '\n')


if __name__ == '__main__':
    main()