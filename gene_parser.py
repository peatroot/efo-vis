import sys
import json

output_filename = 'genes.json'

def parse(filename):
    genes = {}
    with open(filename, 'r') as f_input:        
        for line in f_input:
            blob = json.loads(line)
            gene_id = blob['id']
            gene_symbol = blob['approved_symbol']
            genes[gene_symbol] = gene_id
            # genes.append({
            #     'id': gene_id,
            #     'symbol': gene_symbol
            # })

    with open(output_filename, 'w') as f_output:
        json.dump(genes, f_output, indent=4, sort_keys=True)

if __name__ == '__main__':
    filename = sys.argv[1]
    parse(filename)