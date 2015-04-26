with open('../cdhit_combined.clstr') as f:
    lines = f.readlines()
counts = [0] * 300
last = 0
for line in lines:
    if line.startswith('>'):
        #print(last)
        counts[last] += 1
    else:
        last = int(line.split()[0])

for i in range(len(counts)):
    if counts[i] > 0:
        print(i, counts[i])