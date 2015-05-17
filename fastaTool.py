from Bio import SeqIO
import sys


def usage():
    print("fastaTools find file start length")


def main():
    if len(sys.argv) == 5 and sys.argv[1] == 'find':
        handle = open(sys.argv[2])
        start = int(sys.argv[3])
        length = int(sys.argv[4])
        records = list(SeqIO.parse(handle, 'fasta'))
        print(records[0][start:start+length].seq)
    else:
        usage()


if __name__ == '__main__':
    main()

