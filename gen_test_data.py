import random
import readers

# definitions
ACTG_PROB_DISTRO = [.25, .25, .25, .25]
MAX_GEN_SIZE = 500


def cumulative(l):
    total = 0
    for n in l:
        total += n
        yield total


actg = ['A', 'C', 'T', 'G']
actg_prob_cumulative = [p for p in cumulative(ACTG_PROB_DISTRO)]
def random_base():
    value = random.random()
    for i in range(len(actg_prob_cumulative)):
        if value < actg_prob_cumulative[i]:
            return actg[i]


def gen_random_sequence(length):
    return ''.join([random_base() for i in range(length)])


def gen_test(seq, target, name):
    prefix_len = random.randint(0, MAX_GEN_SIZE)
    suffix_len = random.randint(0, MAX_GEN_SIZE)

    output = ''.join([gen_random_sequence(prefix_len),
                      seq,
                      gen_random_sequence(suffix_len)])
    return "> %d:%d?%s?%s\n%s" %(prefix_len, len(seq) + prefix_len, target, name, output)


def unit_test():
    pattern = 'AAAAAA'
    value = gen_test(pattern, 'adr001', 'test')
    lines = value.split('\n')
    offset, target, name = lines[0][1:].split('?', 2)
    start, end = offset.split(':')
    start = int(start)
    end = int(end)
    if lines[1][start:end] == pattern:
        print("Success")
    else:
        print(lines[1][start:end])

#unit_test()
id_to_name = readers.read_grouping()
name_to_seq = readers.read_fasta()
for id, names in id_to_name.items():
    with open('../test/%s.fa' % id, 'w+') as fasta:
        for name in names:
            seq = name_to_seq[name]
            value = gen_test(seq, id, name)
            fasta.write(value + '\n')

