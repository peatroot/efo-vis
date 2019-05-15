import sys
import json

output_filename = 'genes.min.json'

def compress(filename):
    '''
    Input should be a JSON file containing a list of objects,
    each containing ensembl id, uniprot id and symbol fields.

    Compression does the following:
    1. Delta encoding by the ensembl id.
    2. The output per disease is an array with delta encoded
       ensembl id and symbol in positions 0 and 1 respectively.
    '''
    with open(filename, 'r') as f_input:
        genes = json.load(f_input)

    # build lookup (ensembl id -> symbol)
    ensembl_to_symbol = {g['id']: g['symbol'] for g in genes}

    # build lookup (ensembl id -> delta encoded ensembl id)
    ensembl_ids = sorted([g['id'] for g in genes])
    ensembl_to_int = lambda ensembl_id: int(ensembl_id.split('ENSG')[1])
    ensembl_to_delta = {
        ensembl_id: (ensembl_to_int(ensembl_id) - ensembl_to_int(ensembl_ids[i - 1])) if i > 0 else ensembl_id
        for i, ensembl_id in enumerate(ensembl_ids)
    }

    # build output ([delta encoded ensembl id, symbol])
    output = [[ensembl_to_delta[ensembl_id], ensembl_to_symbol[ensembl_id]] for ensembl_id in ensembl_ids]

    with open(output_filename, 'w') as f_output:
        json.dump(output, f_output, separators=(',', ':'), sort_keys=True)


if __name__ == '__main__':
    filename = sys.argv[1]
    compress(filename)