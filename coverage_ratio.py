import argparse
import sys

parser = argparse.ArgumentParser(description="Filters a PSL file output from blat based on criteria in arguments")
parser.add_argument('-r', dest='ratio', type=float, default=0.0,
                    help='The minimum coverage ratio required to pass through to output.'
                         ' <ratio> is an decimal number <= 1, and is non-inclusive.')
args = parser.parse_args()
print('QName\tTName\tSimilarity')

for line in sys.stdin:
    if line[0].isdigit():
        tokens = line.split('\t')
        similarity = float(tokens[0])/float(tokens[14])
        if similarity > args.ratio:
            print('%s\t%s\t%f' % (tokens[9], tokens[13], similarity))
