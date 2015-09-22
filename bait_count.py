# This is to take the result of running counting what genes match a set of baits against the AMR database.
# The goal is to calculate which baits are associated with what family so that we can print
# out AMR family and how many baits will recognize that family. We may decide to enrich some baits
# in order to deal with the some gene families that we know occur more often in our database.

'''
For the protein case, we start with the hmmscan result file which
maps protein gene name -> RF number
metadata maps RF number -> ARO: number for resistance gene
Use ontology to map ARO: number for resistance gene to list of genes based on is_a relationship
Use ontology to find where any of these gene has "confers resistance to" relationship to ARO: antibiotic

read protein fasta file to map protein gene name to dna gene name
parse acronym for antibiotic_code to get ARO: for antibiotic
Use ontology to walk is_a relationship for all other drugs
compare these drugs with the list of antibiotics confer resistance to
'''
import sys
import readers
import collections
import argparse

import ontology_common


def read_count(filename):
    name_to_count = collections.defaultdict(int)
    with open(filename) as f:
        lines = f.readlines()
    for line in lines[1:]:
        tokens = line.strip('\n').split('\t')
        name = tokens[0]
        count = tokens[1]
        try:
            c = int(count)
        except ValueError:
            continue
        name_to_count[name] += c
    return name_to_count


def main():
    if len(sys.argv) != 2:
        print("Usage: bait_count.py master_amr_parsed.tsv")
        sys.exit(-1)
    count_file = sys.argv[1]
    name_to_count = read_count(count_file)
    groups = readers.read_grouping('grouping.csv', short=True, map_name=True, strip_colon=False)
    terms = ontology_common.parse_obo('new_combined.obo')
    baits_for_class = collections.defaultdict(int)
    for gene, count in name_to_count.items():
        group = groups[gene]
        for cl in ontology_common.get_class(group, terms):
            baits_for_class[cl] += count
    print()
    total_baits = 0
    for k, v in baits_for_class.items():
        if 'resistance gene' in terms[k]['name'][0]:
            print(terms[k]['name'][0], v)
            total_baits += v
    print("Total counts for gene class ", total_baits)
    print()
    total_baits = 0
    for k, v in baits_for_class.items():
        if 'resistance gene' not in terms[k]['name'][0]:
            print(terms[k]['name'][0], v)
            total_baits += v
    print("Total counts for mechanism ", total_baits)

if __name__ == '__main__':
    main()
