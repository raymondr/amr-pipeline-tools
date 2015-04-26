# This program takes a CSV with 3 columns ARO Number, name, ARO Grouping number
# and generates an ontology in ORO format.
# It reads from stdin and writes to stdout

import fileinput


id_to_name = {
'ARO:3000472': ['tetracycline resistance gene'],
'ARO:3000751': ['peptide antibiotic resistance gene'],
'ARO:3000012': ['gene conferring antibiotic resistance via molecular bypass'],
'ARO:3000610': ['gene detected by antibiotic resistance screening microarray'],
'ARO:3001311': ['elfamycin resistance gene'],
'ARO:3001217': ['trimethoprim resistance gene'],
'ARO:0000031': ['antibiotic resistant gene variant or mutant'],
'ARO:3000159': ['efflux pump conferring antibiotic resistance'],
'ARO:3001207': ['gene involved in antibiotic sequestration'],
'ARO:3000052': ['phenicol resistance gene'],
'ARO:3000383': ['rifampin resistance gene'],
'ARO:3000557': ['antibiotic inactivation enzyme'],
'ARO:3000451': ['gene modulating antibiotic efflux'],
'ARO:3000362': ['mosaic antibiotic resistance gene'],
'ARO:3000241': ['lincosamide resistance gene'],
'ARO:0000010': ['antibiotic resistance gene cluster, cassette, or operon'],
'ARO:3003058': ['tunicamycin resistance gene'],
'ARO:3000529': ['mupirocin resistance gene'],
'ARO:3000381': ['antibiotic target replacement protein'],
'ARO:3000267': ['linezolid resistance gene'],
'ARO:3003024': ['fusidic acid resistance gene'],
'ARO:3000477': ['aminocoumarin resistance gene'],
'ARO:3000185': ['antibiotic target protection protein'],
'ARO:3002984': ['polymyxin resistance gene'],
'ARO:3000492': ['gene involved in self resistance to antibiotic'],
'ARO:3000468': ['ethambutol resistance gene'],
'ARO:3000494': ['glycopeptide resistance gene'],
'ARO:3000100': ['gene modulating beta-lactam resistance'],
'ARO:3000270': ['gene modulating permeability to antibiotic'],
'ARO:3000271': ['fosfomycin resistance gene'],
'ARO:3000315': ['macrolide resistance gene'],
'ARO:3000519': ['antibiotic target modifying enzyme'],
'ARO:3000868': ['streptothricin resistance gene'],
'ARO:3000104': ['aminoglycoside resistance gene'],
'ARO:3003073': ['lipopeptide antibiotic resistance gene'],
'ARO:3000102': ['fluoroquinolone resistance gene'],
'ARO:3000240': ['streptogramin resistance gene'],
'ARO:3000129': ['beta-lactam resistance gene'],
'ARO:3000398': ['chloramphenicol resistance gene'],
'ARO:3000408': ['sulfonamide resistance gene'],
'ARO:4000070': ['metronidazoles resistance gene']
}

def main():
    for line in fileinput.input():
        line = line.rstrip('\n')
        id,name,parent = line.split(',')
        print('[Term]')
        print('id: %s' % id)
        print('name: %s' % name)
        print('namespace: antibiotic_resistance')
        print('def: "CSU internal term" []')
        print('is_a: %s ! %s\n' %(parent, id_to_name[parent][0]))


if __name__ == '__main__':
    main()