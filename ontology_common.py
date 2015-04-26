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
