# read in mapping file and master.scan
# output all the genes that were not found by their hmm
# output all the genes that were found by multiple hmm (other than their own) ordered by number. Perhaps these genes encode their genes
# output all the hmm that found more than their content ordered by number. Perhaps these hmms are too broad

import matplotlib.pyplot as plt
import numpy as np
import readers

def substitute_read_name(scan_name_to_id, contig_to_read):
    new_name_to_id = {}
    for k, v in scan_name_to_id.items():
        name = contig_to_read[k][0]
        if name.startswith('NC_002516.2.880450'):
            print(name)
        new_name_to_id[name] = v
    return new_name_to_id

id_to_name = readers.read_grouping('../combined_grouping.csv')
thresh = []
fp = []
tp = []
nf = []
contig_to_read = readers.read_maf('../test_art_out.maf')
for threshold in range(0, 1, 100):
    #print("Threshold: %d" % threshold)
    scan_id_to_name, scan_name_to_id = readers.read_scan_results(threshold, '../art_genes.scan')
    scan_name_to_id = substitute_read_name(scan_name_to_id, contig_to_read)
    #print("Genes not found by HMM")
    true_positive = 0
    false_positive = 0
    not_found = 0
    total = 0
    for id in id_to_name.keys():
        for name in id_to_name[id]:
            total += 1
            if ' ' in name:
                short_name, rest = name.split(' ', 1)
            else:
                short_name = name
            if short_name not in scan_name_to_id:
                print("%s,%s" % (name, id))
                not_found += 1
                continue
            ids = scan_name_to_id[short_name]
            ids.sort(key=lambda l: l[1], reverse=True)
            if ids[0][0] == id:
                true_positive += 1
            else:
                #print("%s,%s,%s" % (name, id, ids[0][0]))
                false_positive += 1
    #print("False positive: %d" %  ((false_positive * 100.0) / total))
    thresh.append(threshold)
    #tp.append((true_positive * 100.0) / total)
    #fp.append((false_positive * 100.0) / total)
    tp.append(true_positive)
    fp.append(false_positive)
    nf.append(not_found)
    print(threshold, true_positive, false_positive, not_found, total)
