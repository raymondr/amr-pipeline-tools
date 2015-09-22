# some code taken from http://blog.nextgenetics.net/?e=6

def getTerm(stream):
    block = []
    for line in stream:
        if line.strip() == "[Term]" or line.strip() == "[Typedef]":
            break
        else:
            if line.strip() != "":
                block.append(line.strip())

    return block


def parseTagValue(term):
    data = {}
    for line in term:
        tag = line.split(': ', 1)[0]
        value = line.split(': ', 1)[1]
        if tag not in data:
            data[tag] = []

        data[tag].append(value)

    return data


def parse_obo(filename):
    oboFile = open(filename, 'r')

    # declare a blank dictionary
    #keys are the goids
    terms = {}

    #skip the file header lines
    getTerm(oboFile)


    #infinite loop to go through the obo file.
    #Breaks when the term returned is empty, indicating end of file
    while 1:
        #get the term using the two parsing functions
        term = parseTagValue(getTerm(oboFile))
        if len(term) != 0:
            termID = term['id'][0]
            terms[termID] = term
        else:
            break
    return terms

def find_children():
    for k, v in terms.items():
        if 'is_a' in v:
            for value in v['is_a']:
                id = value.split()
                parent = terms[id[0]]
                if 'childrenId' not in parent:
                    parent['childrenId'] = []
                parent['childrenId'].append(k)


visited = {}
def populate_children(parent, depth=0):
    if depth > 5:
        print("skipping", parent['name'])
        return
    if 'childrenId' in parent:
        parent['children'] = []
        for id in parent['childrenId']:
            if id not in visited:
                child = terms[id]
                if 'include' in child:
                    parent['children'].append(child)
                    populate_children(child, depth+1)
                    visited[id] = True
            else:
                print("already visited: ", id)


def get_lineage(id, terms):
        t_id_stack = [id]
        yield id
        while t_id_stack:
            t_id = t_id_stack.pop(0)
            if t_id in terms:
                t = terms[t_id]
                t['include'] = True
                if 'is_a' in t:
                    for is_a_node in t['is_a']:
                        parent_id = is_a_node.split()[0]
                        yield parent_id
                        t_id_stack.append(parent_id)

        if id.startswith('ARO:4'):
            yield 'ARO:4'
            yield "ARO:3000000"
        elif id.startswith('ARO:5'):
            yield 'ARO:5'
            yield "ARO:3000000"
        else:
            yield 'Unknown'


def get_class(id, terms):
        t_id_stack = [id]
        while t_id_stack:
            t_id = t_id_stack.pop(0)
            if t_id in terms:
                t = terms[t_id]
                if 'is_a' in t:
                    for is_a_node in t['is_a']:
                        parent_id = is_a_node.split()[0]
                        if parent_id == "ARO:3000000":
                            yield t_id
                        else:
                            t_id_stack.append(parent_id)


def get_resistance(lineage, terms):
    drugs = set()
    for id in lineage:
        if id in terms and 'relationship' in terms[id]:
            for relation in terms[id]['relationship']:
                args = relation.split()
                if args[0] in ['confers_resistance_to_drug', 'confers_resistance_to']:
                    drugs.add(args[1])
    return drugs