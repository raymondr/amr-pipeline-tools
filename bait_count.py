# This is to take the result of counting what genes match a set of baits against the AMR database.
# The goal is to calculate which baits are associated with what family so that we can print
# out AMR family and how many baits will recognize that family. We may decide to enrich some baits
# in order to deal with the some gene families that we know occur more often in our database.
# We finally print out the summary for both gene class and resistance mechanism.

'''
Internally, this reads the passed in tab separated file that lists genes and the number of baits
that match that gene. This file may contain header lines scattered throught the file since it appeasr to be
multiple files concatenated together. Also a gene will appear multiple times so we want to keep a running sum.
This is stored in a dictionary.
We then use the grouping file to map the gene name to ARO id.
Given this ARO id we then use the ontology code to map the ARO id using the multiple inheritance is_a relationship.
'''
import sys
import readers
import collections

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
