def read_fasta(file='../master_AMRdb.fa'):
    with open(file) as f:
        lines = f.readlines()
    name = None
    map = {}
    seq = ''
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('>'):
            if name:
                map[name] = seq
                seq = ''
            name = line[1:].strip()
        else:
            seq += line
    map[name] = seq
    return map


def read_grouping(filename='../grouping.csv'):
    with open(filename) as f:
        lines = f.readlines()
    id_to_name = {}
    for line in lines:
        line = line.rstrip('\n')
        name, id = line.rsplit(',', 1)
        id = id.strip()
        id = ''.join(id.split(':'))
        name = name.strip('"').strip()
        if id not in id_to_name:
            id_to_name[id] = [name]
        else:
            id_to_name[id].append(name)
    return id_to_name


def read_scan_results(threshold, filename, key=False):
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
