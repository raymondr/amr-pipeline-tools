# This is to take the result of running blat of a proposed set of baits against the AMR database.
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

import ontology_common


def read_fsl(filename):
    groups = readers.read_grouping('grouping.csv', short=True, map_name=True, strip_colon=False)
    query_to_target = {}
    with open(filename) as f:
        lines = f.readlines()
    skipped_matches = 0
    for line in lines[5:]:
        tokens = line.strip('\n').split('\t')
        if int(tokens[0]) < 120 * .4:
            skipped_matches += 1
            continue
        if tokens[9] in groups:
            group = groups[tokens[9]]
        else:
            group = "Unknown"
        if tokens[9] in query_to_target:
            query_to_target[tokens[9]].append((group, tokens[13]))
        else:
            query_to_target[tokens[9]] = [(group, tokens[13])]
    print("matches lower that 40%", skipped_matches)
    return query_to_target


def main():
    if len(sys.argv) != 3:
        print("Usage: bait_frequency.py file.fsl genes.fa")
        sys.exit(-1)
    fsl_file = sys.argv[1]
    target_to_id = read_fsl(fsl_file)
    fasta_file = sys.argv[2]
    genes, name_map = readers.read_fasta(fasta_file, shorten=True, max_length_shorten=False)
    terms = ontology_common.parse_obo('new_combined.obo')
    baits_for_class = collections.defaultdict(set)
    for gene in genes.keys():
        name = gene
        found = name in target_to_id
        if found:
            results = target_to_id[name]
            for result in results:
                for cl in ontology_common.get_class(result[0], terms):
                    baits_for_class[cl].add(result[1])
            #print(name, len(results))
        else:
            print(name, '0')
    print()
    total_baits = 0
    for k, v in baits_for_class.items():
        print(terms[k]['name'], len(v))
        total_baits += len(v)
    print("Total baits for all genes", total_baits)

if __name__ == '__main__':
    main()
