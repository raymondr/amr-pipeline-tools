from Bio import Entrez
import sys

# dantes papers
p1 = '24847883' # Bacterial Phylogeny Structures Soil Resistomes Across Habitats
p2 = '24236055' # Pediatric Fecal Microbiota Harbor Diverse and Novel Antibiotic Resistance Genes.
p3 = '22936781' # The shared antibiotic resistome of soil bacteria and human pathogens
Entrez.email = "robr@colostate.edu"     # Always tell NCBI who you are
record = Entrez.read( Entrez.elink(dbfrom="pubmed", db="nuccore", LinkName="pubmed_nuccore", from_uid=sys.argv[1]))
filename = '%s' % (sys.argv[2])
with open(filename, 'w') as f:
    for item in record[0]['LinkSetDb'][0]['Link']:
        id = item['Id']
        url = 'http://www.ncbi.nlm.nih.gov/nuccore/%s?report=fasta' % id
        data = Entrez.read(Entrez.efetch(db="nucleotide", id=id, rettype="gb", retmode="xml"))
        resistance = False
        product = id
        for elem in data[0]['GBSeq_feature-table']:
            if 'GBFeature_quals' in elem:
                for e in elem['GBFeature_quals']:
                    if e['GBQualifier_name'] == 'note' and \
                            ('antibiotic resistance gene' in e['GBQualifier_value'] or
                             'confers' in e['GBQualifier_value']):
                        resistance = True
                    if e['GBQualifier_name'] == 'product':
                        product = e['GBQualifier_value']
                        product = '_'.join(product.split())
        f.write("> %s_%s_%s\n" % (str(resistance), product, id))
        # data[0]['GBSeq_definition'])
        f.write("%s\n" % data[0]['GBSeq_sequence'])
