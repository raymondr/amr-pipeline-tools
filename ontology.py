# From the grouping file, determine how many genes fall into each general category from CARD ontology
import ontology_common


def get_inclusions():
    #with open('../combined_grouping.csv') as f:
    with open('/tmp/cluster') as f:
        lines = f.readlines()
    ids = []
    for line in lines:
        line = line.rstrip('\n')
        name, id = line.rsplit(',', 1)
        id = id.strip()
        ids.append(id)
    return ids


def categories():
    # read in file of genes to include
    include = get_inclusions()
    count_by_category = {}
    for id in include:
        category = get_category(id)
        if category:
            name = category['name'][0]
        elif id.startswith('ARO:4'):
            name = 'ARO:4'
        elif id.startswith('ARO:5'):
            name = 'ARO:5'
        else:
            name = 'Unknown'
        if name in count_by_category:
            count_by_category[name] += 1
        else:
            count_by_category[name] = 1
        #print(id, name)
    category_list = [(k, v) for k, v in count_by_category.items()]
    category_list.sort(key=lambda l: l[1], reverse=True)
    print('Class, Count, Percent')
    total = 0
    for m in category_list:
        total += m[1]
    for m in category_list:
        print('%s, %s, %d' % (m[0], m[1], float(m[1]) * 100.0 / total))


def get_category(id):
        t_id = id
        while t_id:
            if t_id in terms:
                t = terms[t_id]
                t['include'] = True
                if 'is_a' in t:
                    parent_id = t['is_a'][0].split()[0]
                    if parent_id == 'ARO:3000557':
                        parent_id = t['is_a'][1].split()[0]
                    if parent_id == 'ARO:3000000':
                        return t
                    else:
                        t_id = parent_id
                else:
                    return None
            else:
                #print("%s not found in terms" % t_id)
                return None

terms = ontology_common.parse_obo('../new_combined.obo')
categories()
