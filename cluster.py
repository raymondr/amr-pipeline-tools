import json

def read_fasta():
    with open('../master_AMRdb.fa') as f:
        lines = f.readlines()
    name = None
    map = {}
    seq = ''
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('>'):
            if name:
                map[name] = seq
                seq = ''
            name = line[1:]
        else:
            seq += line
    map[name] = seq
    return map


id_to_name = {}
def read_ontology():
    with open('../aro.obo') as f:
        lines = f.readlines()
    NAME_TOKEN = 'name: '
    ID_TOKEN = 'id: '
    SYNONYM_TOKEN = 'synonym: "'
    map = {}
    for line in lines:
        if line.startswith(ID_TOKEN):
            id = line[len(ID_TOKEN):-1]
        elif line.startswith(NAME_TOKEN):
            map[line[len(NAME_TOKEN):-1].lower()] = id
            id_to_name[id] = line[len(NAME_TOKEN):-1]
        elif line.startswith(SYNONYM_TOKEN):
            map[line[len(SYNONYM_TOKEN):-11].lower()] = id
            id_to_name[id] = line[len(SYNONYM_TOKEN):-11]
    return map


def lookup_term(term):
    id = ontology.get(term.lower(), None)
    return id


def add_entry(name, id):
    if id in entries:
        entries[id].append(name)
    else:
        entries[id] = [name]

ontology = read_ontology()
m = read_fasta()
names = m.keys()
names.sort()
entries = {}

ARO_PREFIX = 'ARO:3'
for name in names:
    #print name
    if name.startswith('('):
        # handle (AGly)3Aac6-Iad:AB119105:1-435:435
        cla, remainder = name.split(')', 1)
        cla = cla[1:]
        components = remainder.split(':')
        method = components[0]
        '''
        if '-' in method:
            components = method.split('-')
            method = components[0]
        '''
        id = lookup_term(method)
        if not id and '-' in method:
            # handle (AGly)Ant6-Ia:AF330699:22-930:909 mapping to ontology ANT(6)-Ia
            for i in range(len(method)):
                if method[i].isdigit():
                    first_digit = i
                    break;
            end = method.find('-')
            new_method = "%s(%s)%s" % (method[:first_digit],
                                       method[first_digit:end],
                                       method[end:])
            id = lookup_term(new_method)
        add_entry(name, id)
    elif ' ' in name:
        if ARO_PREFIX in name:
            # handle CP001581.1.gene938 folP. folP encodes dihydropteroate synthase. ARO:1000001 process or component of antibiotic biology or chemistry. ARO:3000226 sulfonamide resistant dihydropteroate synthase folP. [Clostridium botulinum A2 str. Kyoto]
            start = name.find(ARO_PREFIX)
            end = name.find(' ', start)
            id = name[start:end]
            add_entry(name, id)
        else:
            print('Unknown annotation: ' + name)
    elif '_' in name:
        components = name.split('_')
        prefix = components[0]
        # handle QnrB71_1_KC580660
        id = lookup_term(prefix)
        if not id and '(' in prefix:
            # handle vga(C)_2_NC_013034
            cla, remainder = name.split('(', 1)
            components = remainder.split(')', 1)
            method = components[0]
            id = lookup_term(cla+method)
        add_entry(name, id)

    else:
        print('Unknown annotation: ' + name)

#print len(names), len(entries), len(entries[None])

ids = entries.keys()
ids.sort()
table = [(k, len(entries[k]), entries[k]) for k in ids]
#print json.dumps(table)


for id in ids:
    #name = id_to_name.get(id, None)
    for t in entries[id]:
        print('"%s",%s' % (t, id))