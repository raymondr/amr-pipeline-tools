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
    new_name_to_id = {}
    for id, names in id_to_name.items():
        try:
            clstr_id_to_name = readers.read_cluster("%s/%s.clstr" % (sys.argv[2], id))
        except IOError:
            # work around bug in cdhit where it cannot deal with one sequence
            clstr_id_to_name = {0: ['ENA|pgpA/ltpgpA|CAA']}
        for clstr_id, names in clstr_id_to_name.items():
            new_id = 'ARO:%ss%s' % (id[3:], clstr_id)
            for name in names:
                new_name_to_id[name] = new_id

    with open(sys.argv[1]) as f:
        lines = f.readlines()
    with open(sys.argv[3], 'w+') as new_grouping:
        for line in lines:
            line = line.rstrip('\n')
            name, id = line.rsplit(',', 1)
            short_name = name.strip('"').strip()
            short_name = short_name.split()[0] if ' ' in short_name else short_name
            if len(short_name) > 19:
                short_name = short_name[:19]
            new_grouping.write('%s,%s\n' % (name, new_name_to_id[short_name]))

if __name__ == '__main__':
    main()
