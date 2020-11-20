
def read_textfile(path):
    with open(path, 'r') as f:
        return [l.strip() for l in f.readlines()]

def write_textfile(path, seq, mode='w'):
    with open(path, mode) as f:
        f.write(seq + '\n')

def read_FASTA(path):
    with open(path, 'r') as f:
        Fasta = [l.strip() for l in f.readlines()]

    F_Dictionary = {}
    Label = ""

    for line in Fasta:
        if '>' in line:
            Label = line
            F_Dictionary[Label] = ""
        else:
            F_Dictionary[Label] += line

    return F_Dictionary
