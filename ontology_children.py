# This file prints out all of the CARD entries that are children of the root entry

import ontology_common


def find_children(parent):
    for k, v in terms.items():
        if 'is_a' in v:
            for value in v['is_a']:
                id = value.split()
                if id[0] == parent:
                    print("'%s': %s," % (k, v['name']))

terms = ontology_common.parse_obo('../aro.obo')
find_children('ARO:3000000')
