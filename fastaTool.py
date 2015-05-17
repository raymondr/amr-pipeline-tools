from Bio import SeqIO
import sys


def usage():
    print("fastaTools find file start length")
    print("fastaTools len file")


def main():
    if len(sys.argv) == 5 and sys.argv[1] == 'find':
        handle = open(sys.argv[2])
        records = list(SeqIO.parse(handle, 'fasta'))
        start = int(sys.argv[3])
        length = int(sys.argv[4])
        print(records[0][start:start+length].seq)
    elif len(sys.argv) == 3 and sys.argv[1] == 'len':
        handle = open(sys.argv[2])
        records = list(SeqIO.parse(handle, 'fasta'))
        for record in records:
            print(len(record.seq))
    else:
        usage()


if __name__ == '__main__':
    main()

