# This is to take the result of running blat of a proposed set of baits against the AMR database.
# The goal is to calculate which baits are associated with what family so that we can print
# out AMR family and how many baits will recognize that family. We may decide to enrich some baits
# in order to deal with the some gene families that we know occur more often in our database.

import sys
import readers
import collections

import ontology_common


def read_fsl(filename):
    baits = set()
    with open(filename) as f:
        lines = f.readlines()
    for line in lines[5:]:
        tokens = line.strip('\n').split('\t')
        score = int(tokens[0])
        gene = tokens[9]
        bait = tokens[13]
        baits.add(bait)
    return baits


def main():
    if len(sys.argv) != 3:
        print("Usage: bait_topmatch.py file.fsl baits.fasta")
        sys.exit(-1)
    fsl_file = sys.argv[1]
    matched_baits = read_fsl(fsl_file)
    baits = readers.read_fasta(file=sys.argv[2])
    for b in baits.keys():
        if b not in matched_baits:
            print(b)

if __name__ == '__main__':
    main()
