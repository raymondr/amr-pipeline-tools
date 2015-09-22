# This is to evaluate the results of running HMM scan against genomic data from functionally verified
# samples. The goal is to evaluate the precision and recall of the HMM.

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

import ontology_common

antibiotic_code = {
    'AX': ('amoxicillin', 'ARO:0000064'),
    'AZ': ('aztreonam', 'ARO:3000550'),
    'CA': ('carbenicillin', 'ARO:0000043'),
    'CF': ('cefdinir', 'ARO:3000650'),
    'CH': ('chloramphenicol', 'ARO:3000385'),
    'CT': ('cefotaxime', 'ARO:3000645'),
    'CX': ('cefoxitin', 'ARO:0000008'),
    'CY': ('cylcoserine', 'ARO:3000760'),
    'CZ': ('ceftazidime', 'ARO:0000060'),
    'GE': ('gentamicin', 'ARO:0000014'),
    'MN': ('minocycline', 'ARO:3000152'),
    'OX': ('oxytetracycline', 'ARO:3000668'),
    'PE': ('penicillin-G', 'ARO:0000054'),
    'PI': ('piperacillin', 'ARO:0000078'),
    'PITZ': ('PiperacillinTazobactam', 'ARO:0000078'),
    'SI': ('sisomicin', 'ARO:0000035'),
    'TE': ('tetracycline', 'ARO:0000051'),
    'TEp10': ('tetracycline', 'ARO:0000051'),
    'TEra': ('tetracycline', 'ARO:0000051'),
    'TG': ('tigecycline', 'ARO:0000030'),
    'TGp15': ('tigecycline', 'ARO:0000030'),
    'TGp14': ('tigecycline', 'ARO:0000030'),
    'TR': ('trimethoprim', 'ARO:3000188'),
    'TRSX': ('trimethoprim', 'ARO:3000188')
}


def read_fsl(filename):
    groups = readers.read_grouping('grouping.csv', short=True, map_name=True, strip_colon=False)
    query_to_target = {}
    with open(filename) as f:
        lines = f.readlines()
    for line in lines[1:]:
        tokens = line.strip('\n').split('\t')
        group = groups[tokens[1]]
        if tokens[0] in query_to_target:
            query_to_target[tokens[0]].append((group, tokens[2]))
        else:
            query_to_target[tokens[0]] = [(group, tokens[2])]
    return query_to_target


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: functional_compare.py [-fsl] [-protein] results.scan seq.fasta")
        sys.exit(-1)
    fsl = True if sys.argv[1] == '-fsl' else False
    protein = True if sys.argv[1] == '-protein' else False
    if fsl:
        fsl_file = sys.argv[2]
        fasta_file = sys.argv[3]
    elif protein:
        scan_file = sys.argv[2]
        fasta_file = sys.argv[3]
    else:
        scan_file = sys.argv[1]
        fasta_file = sys.argv[2]
    genes = readers.read_fasta(fasta_file)
    if fsl:
        target_to_id = read_fsl(fsl_file)
    else:
        id_to_target, target_to_id = readers.read_scan_results(0, scan_file, protein=protein)
    if protein:
        readers.change_RF_to_ARO(target_to_id)
        already_seen_protein = set() # We don't want to double count if we have seen the same gene

    terms = ontology_common.parse_obo('new_combined.obo')
    false_positive = 0
    true_positive = 0
    false_negative = 0
    for gene in genes.keys():
        if protein:
            names = gene.split('>')
            gene = names[1].strip()
            name = names[0].strip()
            if gene in already_seen_protein:
                continue
            else:
                already_seen_protein.add(gene)
        else:
            name = gene
        found = name in target_to_id
        if found:
            antibiotic = gene.split('_')[1]
            functional_antibiotic = antibiotic_code[antibiotic]
            results = target_to_id[name]
            results.sort(key=lambda l: l[1], reverse=True)
            index = 0
            while index < len(results):
                result = results[index]
                index += 1
                id = result[0]
                # remove formatting used by hmm
                if 's' in id:
                    id = id.replace('ARO', 'ARO:')
                    id = id.split('s')[0]
                if ';' in id:
                    # resfams can have a list of ids associated with a gene
                    classes = [terms[p]['name'] for i in id.split(';') for p in ontology_common.get_class(i, terms)]
                    drugs = set()
                    for i in id.split(';'):
                        drugs |= ontology_common.get_resistance(ontology_common.get_lineage(i, terms), terms)
                else:
                    classes = [terms[p]['name'] for p in ontology_common.get_class(id, terms)]
                    drugs = ontology_common.get_resistance(ontology_common.get_lineage(id, terms), terms)
                identified = False
                for drug in drugs:
                    for d in ontology_common.get_lineage(drug, terms):
                        for fd in ontology_common.get_lineage(functional_antibiotic[1], terms):
                            if d == fd and d not in ['ARO:1000001', 'ARO:1000003', 'Unknown']:
                                identified = True

                if identified:
                    true_positive += 1
                    break
        else:
            false_negative += 1
        if found and not identified:
            print(gene, functional_antibiotic, id, classes, drugs)
            false_positive += 1


    print('False negative: %d; False Positive:%d; True Positive:%d' % (false_negative, false_positive, true_positive))
if __name__ == '__main__':
    main()
