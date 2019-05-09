import sys
import json

output_filename = 'genes.json'
summary_output_filename = 'protein-coding-genes.json'

def parse(filename):
    genes = {}
    genes_summary = []
    with open(filename, 'r') as f_input:        
        for line in f_input:
            blob = json.loads(line)
            gene_id = blob['id']
            gene_symbol = blob['approved_symbol']
            uniprot_id = blob['uniprot_id']
            genes[gene_symbol] = gene_id
            if blob['biotype'] == 'protein_coding':
                genes_summary.append({
                    'id': gene_id,
                    'symbol': gene_symbol,
                    'uniprotId': uniprot_id
                })

    with open(output_filename, 'w') as f_output:
        json.dump(genes, f_output, indent=4, sort_keys=True)

    with open(summary_output_filename, 'w') as f_output:
        json.dump(genes_summary, f_output, indent=4, sort_keys=True)

if __name__ == '__main__':
    filename = sys.argv[1]
    parse(filename)