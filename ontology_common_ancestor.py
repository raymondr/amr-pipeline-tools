# Find the common ancestor in ontology of two ids
import ontology_common
import sys
import json


def get_counts(filename):
    with open(filename) as f:
        lines = f.readlines()
    ids = []
    for line in lines:
        line = line.rstrip('\n')
        id, cnt = line.split(',')
        id = id.replace('ARO', 'ARO:')
        id = id.split('s')[0]
        ids.append((id, int(cnt)))
    return ids


def get_lineage(id, terms):
        t_id = id
        while t_id:
            if t_id in terms:
                t = terms[t_id]
                t['include'] = True
                if 'is_a' in t:
                    parent_id = t['is_a'][0].split()[0]
                    if parent_id == 'ARO:3000557':
                        parent_id = t['is_a'][1].split()[0]
                    yield parent_id
                    t_id = parent_id
                else:
                    t_id = None
            else:
                t_id = None
        if id.startswith('ARO:4'):
            yield 'ARO:4'
            yield "ARO:3000000"
        elif id.startswith('ARO:5'):
            yield 'ARO:5'
            yield "ARO:3000000"
        else:
            yield 'Unknown'


def build_tree(counts, terms):
    root = ["ARO:3000000", 0, set(), '']
    nodes = {"ARO:3000000": root}
    for id, cnt in counts:
        current = get_node(id, nodes)
        current[1] = cnt
        for item in get_lineage(id, terms):
            parent = get_node(item, nodes)
            parent[1] += cnt
            parent[2].add(current[0])
            if parent == root:
                break
            current = parent
    return root, nodes


def get_node(id, nodes):
    if id not in nodes:
        nodes[id] = [id, 0, set(), '']
    return nodes[id]


def fill_children(node, nodes, terms):
    children = {}
    for child in node[2]:
        if type(child) is str:
            c = get_node(child, nodes)
            fill_children(c, nodes, terms)
            children[c[0]] = c
    node[2] = children
    if node[0] in terms:
        node[3] = terms[node[0]]['name'][0]


def main():
    terms = ontology_common.parse_obo('../new_combined.obo')
    with open('mismatch.csv') as f:
        headers = f.readline()
        print("Actual, Identified As, Common Class, Common Class Description")
        while True:
            line = f.readline()
            if not line:
                break
            actual, id = line.strip().split(',')
            id = id.replace('ARO', 'ARO:')
            id = id.split('s')[0]
            actual = actual.replace('ARO', 'ARO:')
            actual = actual.split('s')[0]
            id_parents = [p for p in get_lineage(id, terms)]

            for p in get_lineage(actual, terms):
                if p in id_parents:
                    description = terms[p]['def'][0] if terms.get(p) else "No Description"
                    print('%s,%s,%s,%s' % (id, actual, p, description))
                    break



if __name__ == '__main__':
    main()