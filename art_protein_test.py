# read in mapping file and master.scan
# output all the genes that were not found by their hmm
# output all the genes that were found by multiple hmm (other than their own) ordered by number. Perhaps these genes encode their genes
# output all the hmm that found more than their content ordered by number. Perhaps these hmms are too broad

import matplotlib.pyplot as plt
import numpy as np
import readers
import sys
import test


def read_genemark(filename):
    with open(filename) as f:
        lines = f.readlines()
    genemark_to_source = {}
    for line in lines:
        if line.startswith('>'):
            annot = line.split()
            genemark_to_source[annot[0][1:]] = annot[1][1:]
    return genemark_to_source


def substitute_read_name(scan_name_to_id, contig_to_read, genemark_to_name):
    new_name_to_id = {}
    for k, v in scan_name_to_id.items():
        k = genemark_to_name[k]
        for name in contig_to_read[k]:
            if name in new_name_to_id:
                new_name_to_id[name].append(v)
            else:
                new_name_to_id[name] = [v]

    return new_name_to_id


def search(name, id, scan_name_to_id):
    if ' ' in name:
        short_name, rest = name.split(' ', 1)
    else:
        short_name = name
    if short_name not in scan_name_to_id:
        return None
    merged_list = []
    for ids in scan_name_to_id[short_name]:
        ids.sort(key=lambda l: l[1], reverse=True)
        if ids[0][0] == id or ids[0][0].split('s')[0] == id.split('s')[0]:
            return ids
        else:
            merged_list += ids
    merged_list.sort(key=lambda l: l[1], reverse=True)
    return merged_list


def main():
    if len(sys.argv) != 6:
        print("Usage: art_test.py grouping.csv scanresults.scan art_out.maf scores.csv genemark.f")
        sys.exit(0)

    genemark_to_name = read_genemark(sys.argv[5])

    id_to_name = readers.read_grouping(sys.argv[1])
    thresh = []
    fp = []
    tp = []
    nf = []
    contig_to_read = readers.read_maf(sys.argv[3])
    for threshold in range(0, 80, 100):
        mismatch = []
        scan_id_to_name, scan_name_to_id = readers.read_scan_results(threshold, sys.argv[2],protein=True)
        readers.change_RF_to_ARO(scan_name_to_id)
        scan_name_to_id = substitute_read_name(scan_name_to_id, contig_to_read, genemark_to_name)
        found_score = []
        true_positive = 0
        false_positive = 0
        not_found = 0
        total = 0
        for id in sorted(id_to_name.keys()):
            canonical_id = id.split('s')[0]
            canonical_id = 'ARO:' + canonical_id.split('O')[1]
            for name in id_to_name[id]:
                total += 1
                ids = search(name, id, scan_name_to_id)
                if ids:
                    if ids[0][0] == canonical_id:
                        true_positive += 1
                        found_score.append((ids[0][1], id, name))
                    else:
                        if ';' in ids[0][0] and canonical_id in ids[0][0].split(';'):
                            true_positive += 1
                            found_score.append((ids[0][1], id, name))
                        else:
                            #print("False Positive: %s, %s" % (name, id))
                            mismatch.append((name, canonical_id, ids[0][0], ids[0][2]))
                            for i in range(len(ids)):
                                #print("Attempt %d: %s %f" % (i, ids[i][0], ids[i][1]))
                                if ids[i][0] == canonical_id:
                                    found_score.append((ids[i][1], id, name))
                                    break
                            false_positive += 1
                else:
                    #for k,v in contig_to_read.items():
                    #    if name in v:
                    #        #print("Found read %s in %s" % (name, k))
                    #print("Not Found: %s,%s" % (name, id))
                    not_found += 1

        thresh.append(threshold)
        tp.append(true_positive)
        fp.append(false_positive)
        nf.append(not_found)
        print("misclassified %d notfound %d true positive %d of total %d" % (false_positive,
                                                                             not_found,
                                                                             true_positive,
                                                                             total))

        print(threshold, true_positive, false_positive, not_found, total)
    x = np.array(fp)# false_positive_rate
    y = np.array(tp)# true_positive_rate
    t = np.array(thresh)
    n = np.array(nf)

    found_score.sort()
    with open(sys.argv[4], 'w') as f:
        for score, hmm, name in found_score:
            f.write('%s,%d\n' % (hmm, score - 1))
    with open('mismatch.csv', 'w') as f:
        f.write('Gene,Expected ID,Found ID\n')
        for a, b, c, d in mismatch:
            f.write('%s,%s,%s\n' % (b, c, a))

    test.graph(x, y, t, n)


if __name__ == '__main__':
    main()