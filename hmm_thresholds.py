import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()
hmm_to_score = {}
for line in lines:
    hmm, score = line.split(',')
    if hmm not in hmm_to_score:
        hmm_to_score[hmm] = score
for hmm, score in hmm_to_score.items():
    filename = '%s/%s.hmm' % (sys.argv[2], hmm)
    with open(filename) as f:
        lines = f.readlines()
    thresh = min(int(score), 700)
    cutoff = 'GA %d %d;\n' % (thresh, thresh)
    newlines = lines[:14] + [cutoff] + lines[14:]
    filename2 = '%s/%s.hmm' % (sys.argv[3], hmm)
    with open(filename2, mode='w') as r:
        r.writelines(newlines)
