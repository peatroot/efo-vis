import sys
import json

output_filename = 'efo-graph.json'

def parse(filename):
    diseases = {}

    with open(filename, 'r') as f_input:        
        for line in f_input:
            blob = json.loads(line)
            efo_id = blob['code'].split('/')[-1]
            name = blob['label']
            description = blob['definition'] if blob['definition'] != '' else None
            parent_ids = {}
            for path in blob['path']:
                if len(path) > 1:
                    parent_id = path[-2]['uri'].split('/')[-1]
                    parent_ids[parent_id] = True
            diseases[efo_id] = {
                'id': efo_id,
                'name': name,
                'description': description,
                'parentIds': list(parent_ids.keys())
            }

    with open(output_filename, 'w') as f_output:
        diseases_list = list(diseases.values())
        json.dump(diseases_list, f_output, indent=4, sort_keys=True)

if __name__ == '__main__':
    filename = sys.argv[1]
    parse(filename)