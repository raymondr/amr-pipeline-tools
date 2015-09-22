# This is to evaluate the results of running HMM scan against genomic data from functionally verified
# samples. The goal is to evaluate the precision and recall of the HMM.
import sys
import readers


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: functional_test.py [-protein] results.scan seq.fasta")
        sys.exit(-1)
    protein = True if sys.argv[1] == '-protein' else False
    if protein:
        scan_file = sys.argv[2]
        fasta_file = sys.argv[3]
        protein_map = {} # place to store mapping of protein name to dna name for genes
    else:
        scan_file = sys.argv[1]
        fasta_file = sys.argv[2]

    genes = readers.read_fasta(fasta_file)
    positive_count = 0
    negative_count = 0

    for gene in genes.keys():
        if 'True' in gene:
            positive_count += 1
        elif 'False' in gene:
            negative_count += 1
        if protein:
            names = gene.split('>')
            protein_map[names[0].strip()] = names[1].strip()

    id_to_target, target_to_id = readers.read_scan_results(0, scan_file, protein=protein)
    false_positive = 0
    true_positive = 0
    already_seen_protein = set() # We don't want to double count if we have seen the same gene
    for key in target_to_id.keys():
        if protein:
            key = protein_map[key]
            if key in already_seen_protein:
                continue
            else:
                already_seen_protein.add(key)
        if key.startswith('False'):
            false_positive += 1
        elif key.startswith('True'):
            true_positive += 1

    print("True Positive: %d/%d(%f); False Positive: %d/%d(%f)" % (true_positive,
                                                            positive_count,
                                                            float(true_positive)/positive_count,
                                                            false_positive,
                                                            negative_count,
                                                            float(false_positive)/negative_count
    ))

if __name__ == '__main__':
    main()
