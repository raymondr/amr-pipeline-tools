import ontology_common
import sys


def main():
    terms = ontology_common.parse_obo('new_combined.obo')
    for l in ontology_common.get_lineage(sys.argv[1], terms):
        print(l)

if __name__ == '__main__':
    main()
