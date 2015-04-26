import fileinput

def read_grouping(filename='../grouping.csv'):
    with open(filename) as f:
        lines = f.readlines()
    name_to_id = {}
    for line in lines:
        line = line.rstrip('\n')
        name, id = line.rsplit(',', 1)
        id = id.strip()
        name = name.strip('"').strip()
        name = ''.join(name.split())
        if name not in name_to_id:
            name_to_id[name] = id
        else:
            print("Could not find name")
    return name_to_id


def read_grouping_list(filename='../grouping.csv'):
    with open(filename) as f:
        lines = f.readlines()
    name_to_id = []
    for line in lines:
        line = line.rstrip('\n')
        name, id = line.rsplit(',', 1)
        id = id.strip()
        name = name.strip('"').strip('>').strip()
        name = ''.join(name.split())
        name_to_id.append((name, id))
    return name_to_id

name_to_id = read_grouping_list('../combined_grouping.csv')
for line in fileinput.input():
    line = line.rstrip('\n')
    found = False
    for i in name_to_id:
        if i[0].startswith(line):
            print('%s,%s' % (line, i[1]))
            found = True
            break
    if not found:
        print('%s not found' % line)