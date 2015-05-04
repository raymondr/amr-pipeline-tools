# read in mapping file and master.scan
# output all the genes that were not found by their hmm
# output all the genes that were found by multiple hmm (other than their own) ordered by number. Perhaps these genes encode their genes
# output all the hmm that found more than their content ordered by number. Perhaps these hmms are too broad

import matplotlib.pyplot as plt
import numpy as np
import readers
import sys


def graph(x, y, t, n):
    # This is the ROC curve
    '''
    plt.plot(x,y)
    plt.title("Multi value ROC Curve")
    plt.ylabel("True Positive (%)")
    plt.xlabel("False Positive (%)")
    plt.show()
    '''

    width = 20
    b1 = plt.bar(t, y, width, color='g')
    b2 = plt.bar(t, x, width, bottom=y, color='r')
    b3 = plt.bar(t, n, width, bottom=y+x, color='b')
    plt.title("How classification varies with threshold")
    plt.ylabel("Number of genes")
    plt.xlabel("Threshold")
    plt.legend((b1[0], b2[0], b3[0]), ('True Positive', 'False Positive', 'Not Classified'))
    plt.show()
    # This is the AUC
    auc = np.trapz(y,x)


def main():
    if len(sys.argv) != 3:
        print("Usage: test.py grouping.csv scanresults.scan")
        sys.exit(0)

    id_to_name = readers.read_grouping(sys.argv[1], short=True)
    thresh = []
    fp = []
    tp = []
    nf = []
    for threshold in range(0, 10, 100):
        scan_id_to_name, scan_name_to_id = readers.read_scan_results(threshold, sys.argv[2])
        found_score = []
        true_positive = 0
        false_positive = 0
        not_found = 0
        total = 0
        for id in id_to_name.keys():
            for name in id_to_name[id]:
                total += 1
                if name not in scan_name_to_id:
                    print("Not found %s,%s" % (name, id))
                    not_found += 1
                    continue
                ids = scan_name_to_id[name]
                ids.sort(key=lambda l: l[1], reverse=True)
                if ids[0][0] == id:
                    true_positive += 1
                    found_score.append((ids[0][1], id, name))
                else:
                    print("False Positive: %s, %s" % (name, id))
                    for i in range(len(ids)):
                        print("Attempt %d: %s %f" % (i, ids[i][0], ids[i][1]))
                        if ids[i][0] == id:
                            found_score.append((ids[i][1], id, name))
                            break
                    false_positive += 1


        thresh.append(threshold)
        tp.append(true_positive)
        fp.append(false_positive)
        nf.append(not_found)

    x = np.array(fp)# false_positive_rate
    y = np.array(tp)# true_positive_rate
    t = np.array(thresh)
    n = np.array(nf)

    found_score.sort()
    print(found_score)
    print(x, y, t, n)
    graph(x, y, t, n)

if __name__ == '__main__':
    main()