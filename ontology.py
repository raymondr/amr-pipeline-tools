# From a csv file, determine how many genes fall into each general category from CARD ontology
import ontology_common
import sys
import argparse


def get_inclusions():
    parser = argparse.ArgumentParser(description="Filters a PSL file output from blat based on criteria in arguments")
    parser.add_argument('--count', dest='count', default=False, action='store_const', const=True,
                        help='Whether csv file contains counts')
    parser.add_argument('-i', dest='file', required=True,
                        help='The csv file')
    parser.add_argument('-t', dest='tab', required=False, action='store_const', const=True,
                        help='tab separated file')
    args = parser.parse_args()
    with open(args.file) as f:
        lines = f.readlines()
    ids = []
    sep = '\t' if args.tab else ','
    for line in lines:
        line = line.rstrip('\n')
        if args.count:
            id, cnt = line.split(sep, 1)
            cnt = cnt.strip()
            try:
                for i in range(int(cnt)):
                    ids.append(id)
            except ValueError:
                continue
        else:
            name, id = line.rsplit(sep, 1)
            id = id.strip()
            ids.append(id)
    return ids


def categories(terms):
    # read in file of genes to include
    include = get_inclusions()
    count_by_category = {}
    for id in include:
        category = get_category(id, terms)
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
    print(total)


def get_category(id, terms):
        t_id = id
        while t_id:
            if t_id in terms:
                t = terms[t_id]
                t['include'] = True
                if 'is_a' in t:
                    parent_id = t['is_a'][0].split()[0]
                    if parent_id == 'ARO:3000557':
                        parent_id = t['is_a'][1].split()[0]
                    if parent_id == 'ARO:3000000' or parent_id == 'ARO:3000001' or parent_id == 'ARO:3000004' or parent_id == 'ARO:3000568':
                        return t
                    else:
                        t_id = parent_id
                else:
                    return None
            else:
                #print("%s not found in terms" % t_id)
                return None


def main():
    terms = ontology_common.parse_obo('new_combined.obo')
    categories(terms)


if __name__ == '__main__':
    main()
