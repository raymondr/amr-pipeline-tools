with open('uclust.70') as f:
    lines = f.readlines()
counts = [0] * 300
last = 0
for line in lines:
    if line.startswith('C'):
        items = line.split()
        counts[int(items[2])] += 1

for i in range(len(counts)):
    if counts[i] > 0:
        print(i, counts[i])