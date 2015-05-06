# read in mapping file and master.scan
# output all the genes that were not found by their hmm
# output all the genes that were found by multiple hmm (other than their own) ordered by number. Perhaps these genes encode their genes
# output all the hmm that found more than their content ordered by number. Perhaps these hmms are too broad

import matplotlib.pyplot as plt
import numpy as np
import readers
import sys
import test



def substitute_read_name(scan_name_to_id, contig_to_read):
    new_name_to_id = {}
    for k, v in scan_name_to_id.items():
        for name in contig_to_read[k]:
            if name.startswith('NC_010611.6233911'):
                pass
            new_name_to_id[name] = v
    return new_name_to_id


def search(name, id, scan_name_to_id):
    if ' ' in name:
        short_name, rest = name.split(' ', 1)
    else:
        short_name = name
    if short_name not in scan_name_to_id:
        return None
    ids = scan_name_to_id[short_name]
    ids.sort(key=lambda l: l[1], reverse=True)
    return ids

def main():
    if len(sys.argv) != 4:
        print("Usage: art_test.py grouping.csv scanresults.scan art_out.maf")
        sys.exit(0)

    id_to_name = readers.read_grouping(sys.argv[1])
    thresh = []
    fp = []
    tp = []
    nf = []
    contig_to_read = readers.read_maf(sys.argv[3])
    for threshold in range(0, 10, 20):
        scan_id_to_name, scan_name_to_id = readers.read_scan_results(threshold, sys.argv[2])
        scan_name_to_id = substitute_read_name(scan_name_to_id, contig_to_read)
        true_positive = 0
        false_positive = 0
        not_found = 0
        total = 0
        for id in sorted(id_to_name.keys()):
            for name in id_to_name[id]:
                total += 1
                ids = search(name, id, scan_name_to_id)
                if ids:
                    if ids[0][0] == id:
                        true_positive += 1
                    else:
                        print("False Positive: %s, %s" % (name, id))
                        for i in range(len(ids)):
                            print("Attempt %d: %s %f" % (i, ids[i][0], ids[i][1]))
                            if ids[i][0] == id:
                                break
                        false_positive += 1
                else:
                    for k,v in contig_to_read.items():
                        if name in v:
                            print("Found read %s in %s" % (name, k))
                    print("Not Found: %s,%s" % (name, id))
                    not_found += 1

        thresh.append(threshold)
        tp.append(true_positive)
        fp.append(false_positive)
        nf.append(not_found)
        print(threshold, true_positive, false_positive, not_found, total)
    x = np.array(fp)# false_positive_rate
    y = np.array(tp)# true_positive_rate
    t = np.array(thresh)
    n = np.array(nf)

    test.graph(x, y, t, n)


if __name__ == '__main__':
    main()