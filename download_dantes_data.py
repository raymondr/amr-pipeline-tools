from Bio import Entrez
import sys

# dantes papers
p1 = '24847883' # Bacterial Phylogeny Structures Soil Resistomes Across Habitats
p2 = '24236055' # Pediatric Fecal Microbiota Harbor Diverse and Novel Antibiotic Resistance Genes.
Entrez.email = "robr@colostate.edu"     # Always tell NCBI who you are
record = Entrez.read( Entrez.elink(dbfrom="pubmed", db="nuccore", LinkName="pubmed_nuccore", from_uid=sys.argv[1]))
for item in record[0]['LinkSetDb'][0]['Link']:
    id = item['Id']
    url = 'http://www.ncbi.nlm.nih.gov/nuccore/%s?report=fasta' % id
    filename = '%s/%s.fasta' % (sys.argv[2], id)
    data = Entrez.read(Entrez.efetch(db="nucleotide", id=id, rettype="gb", retmode="xml"))
    with open(filename, 'w') as f:
        f.write("> %s" % data[0]['GBSeq_definition'])
        f.write(data[0]['GBSeq_sequence'])
