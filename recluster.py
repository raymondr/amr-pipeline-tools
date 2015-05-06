# the purpose of this is to break down dissimilar hmms into smaller hmms with subsets of similarity
# the input is a grouping CSV file and a directory of cdhit clusters. This program then creates
# smaller groupings corresponding to the clusters. This is written out as a new grouping CSV
import sys
import readers


def main():
    if len(sys.argv) != 4:
        print("Usage: recluster.py grouping.csv cdhit output.csv")
        sys.exit(0)

    id_to_name = readers.read_grouping(sys.argv[1], short=True)
    with open(sys.argv[3], 'w+') as new_grouping:
        for id, names in id_to_name:
            clstr_id_to_name = readers.read_cluster("%s/%s.clstr" % (sys.argv[2], id))
            for clstr_id, names in clstr_id_to_name:
                new_id = '%ss%s' % (id, clstr_id)
                for name in names:
                    new_grouping.write('%s,%s' % (name, new_id))

if __name__ == '__main__':
    main()
