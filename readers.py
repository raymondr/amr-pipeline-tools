def read_fasta(file='../master_AMRdb.fa', shorten=False):
    with open(file) as f:
        lines = f.readlines()
    name = None
    map = {}
    name_map = {}
    seq = ''
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('>'):
            if name:
                map[name] = seq
                seq = ''
            name = line[1:].strip()
            if shorten:
                long_name = name
                if ' ' in name:
                    name = name.split()[0]
                if len(name) > 19:
                    name = name[:19]
                name_map[name] = long_name
        else:
            seq += line
    map[name] = seq
    if shorten:
        return map, name_map
    return map


def read_grouping(filename='../grouping.csv', short=False):
    with open(filename) as f:
        lines = f.readlines()
    id_to_name = {}
    for line in lines:
        line = line.rstrip('\n')
        name, id = line.rsplit(',', 1)
        id = id.strip()
        id = ''.join(id.split(':'))
        name = name.strip('"').strip()
        if short and ' ' in name:
            name = name.split()[0]
        if id not in id_to_name:
            id_to_name[id] = [name]
        else:
            id_to_name[id].append(name)
    return id_to_name


def read_scan_results(threshold, filename, key=False, protein=False):
    with open(filename) as f:
        lines = f.readlines()
    scan_id_to_name = {}
    scan_name_to_id = {}
    for line in lines:
        if line[0] == '#':
            continue
        fields = line.split()
        target = fields[0]
        query = fields[2]
        if protein:
            start = ' '.join(fields[17:])
            target = fields[-1].strip('[]') if 'ARO' in fields[-1] else fields[1]
            end = fields[1]
            score = float(fields[5])
        else:
            start = int(fields[5])
            end = int(fields[6])
            score = float(fields[13])
        if score > threshold:
            if key:
                loc,match,name = query.split('?')
                loc_start, loc_end = loc.split(':')
                loc_start = int(loc_start)
                loc_end = int(loc_end)
            else:
                name = query

            if target not in scan_id_to_name:
                scan_id_to_name[target] = [(name, score, start, end)]
            else:
                scan_id_to_name[target].append((name, score, start, end))
            if name not in scan_name_to_id:
                scan_name_to_id[name] = [(target, score, start, end)]
            else:
                scan_name_to_id[name].append((target, score, start, end))
    return scan_id_to_name, scan_name_to_id


def read_maf(filename):
    with open(filename) as f:
        lines = f.readlines()
    contig_to_read = {}
    for line in lines:
        if '\t' not in line:
            continue;
        line = line.rstrip('\n')
        code, remainder = line.split('\t', 1)
        if code == 'CO':
            contig = remainder
            contig_to_read[contig] = []
        elif code == 'RD':
            gene, offset = remainder.rsplit('-', 1)
            if gene not in contig_to_read[contig]:
                contig_to_read[contig].append(gene)
    return contig_to_read


def read_cluster(filename = '../cdhit_combined.clstr'):
    with open(filename) as f:
        lines = f.readlines()
    id_to_name = {}
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('>'):
            c, id = line.split()
            id_to_name[id] = []
        else:
            symbols = line.split()
            name = symbols[2]
            # strip of > and ...
            id_to_name[id].append(name[1:-3])
    return id_to_name


def create_fasta_file_for_each_id(name_to_sequence, id_to_name, dir='seq', name_map=None):
    for k, v in id_to_name.items():
        filename = ''.join(k.split(':')) if ':' in k else k
        with open('%s/%s.fa' % (dir, filename), 'w+') as fasta:
            for name in v:
                if name_map:
                    fasta.write('>%s\n' % name_map[name])
                else:
                    fasta.write('>%s\n' % name)
                fasta.write(name_to_sequence[name] + '\n')


