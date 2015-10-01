# This is to take the result of running blat of a proposed set of baits against the AMR database.
# The goal is to calculate which baits are associated with what family so that we can print
# out AMR family and how many baits will recognize that family. We may decide to enrich some baits
# in order to deal with the some gene families that we know occur more often in our database.

import sys
import readers
import collections

import ontology_common


def read_fsl(filename):
    groups = readers.read_grouping('grouping.csv', short=True, map_name=True, strip_colon=False)
    bait_to_match = {}
    with open(filename) as f:
        lines = f.readlines()
    skipped_matches = 0
    for line in lines[5:]:
        tokens = line.strip('\n').split('\t')
        score = int(tokens[0])
        gene = tokens[9]
        bait = tokens[13]
        if bait in bait_to_match:
            if score > bait_to_match[bait][0]:
                bait_to_match[bait] = (score, gene)
        else:
            bait_to_match[bait] = (score, gene)
    total = collections.defaultdict(int)
    for s, g in bait_to_match.values():
        if g in groups:
            total[groups[g]] += 1
        else:
            total['unknown'] += 1
    return total

def main():
    if len(sys.argv) != 2:
        print("Usage: bait_topmatch.py file.fsl")
        sys.exit(-1)
    fsl_file = sys.argv[1]
    total = read_fsl(fsl_file)
    terms = ontology_common.parse_obo('new_combined.obo')
    baits_for_class = collections.defaultdict(int)
    for gene in total.keys():
        for cl in ontology_common.get_class(gene, terms):
            baits_for_class[cl] += total[gene]

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
