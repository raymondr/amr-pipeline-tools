import readers
import sys


def main():
    threshold = 150
    scan_id_to_name, scan_name_to_id = readers.read_scan_results(threshold, sys.argv[1])
    genes = [(len(v), k) for k,v in scan_id_to_name.items()]
    genes.sort(reverse=True)
    for c,g in genes:
        print('%s,%d' % (g, c))


if __name__ == '__main__':
    main()