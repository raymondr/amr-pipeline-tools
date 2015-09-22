# evaluate conscensus sequences and see if they would match sequences within tolerances provided by Agilent.
# No more than 5 mismatches in a row and no more than 40 mismatches.

MISMATCH_THRESHOLD_PERCENT = 40.0/120.0
CONS_MISMATCH_THRESHOLD = 6


import readers


def match(str1, str2):
    mismatch = 0
    cons_mismatch = 0
    mismatch_threshold = MISMATCH_THRESHOLD_PERCENT * len(str1)
    lth = min(len(str1), len(str2))
    for i in range(lth):
        if str1[i] != str2[i]:
            mismatch += 1
            cons_mismatch += 1
            if mismatch > mismatch_threshold:
                return False
            if cons_mismatch > CONS_MISMATCH_THRESHOLD:
                #print(str1[i-82:])
                #print(str2[i-82:])
                return False
        else:
            cons_mismatch = 0

    return True


def main():
    # for each sequence, see if there is a match with any consensus sequence
    amr = readers.read_fasta(file='../combined.fasta')
    #amr = readers.read_fasta(file='../test.combined.fasta')
    consensus = readers.read_fasta(file='../bait.fasta')
    #consensus = readers.read_fasta(file='../test.clstr.fasta')
    not_found = 0
    for name, gene in amr.items():
        found = False
        for cluster in consensus.values():
            if match(gene, cluster):
                found = True
                break
        if not found:
            not_found += 1
            print('Not found: %s' % name)

    print(not_found)


if __name__ == '__main__':
    main()