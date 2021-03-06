import sys
import json

output_filename = 'efo-graph.json'
output_minified_filename = 'efo-graph-minified.json'

def parse(filename):
    diseases = {}

    root_node = {
        'id': 'EFO_ROOT',
        'name': 'root',
        # 'description': None,
        'parentIds': []
    }
    diseases[root_node['id']] = root_node

    with open(filename, 'r') as f_input:        
        for line in f_input:
            blob = json.loads(line)
            efo_id = blob['code'].split('/')[-1]
            name = blob['label']
            # description = blob['definition'] if blob['definition'] != '' else None
            parent_ids = {}
            for path in blob['path']:
                top_ancestor = path[0]['uri'].split('/')[-1] == efo_id
                conditional_root_parent_id = [root_node['id']] if top_ancestor else []

                if len(path) > 1:
                    parent_id = path[-2]['uri'].split('/')[-1]
                    parent_ids[parent_id] = True
            diseases[efo_id] = {
                'id': efo_id,
                'name': name,
                # 'description': description,
                'parentIds': list(parent_ids.keys()) + conditional_root_parent_id
            }

    with open(output_filename, 'w') as f_output:
        diseases_list = list(diseases.values())
        json.dump(diseases_list, f_output, separators=(',', ':'), sort_keys=True)

    # minify (requires some processing, but slight improvement)
    efo_id_to_int_id = { efo_id: i for i, efo_id in enumerate(diseases.keys()) }
    mapping = [[] for i in range(len(diseases.keys()))]
    parents = [[] for i in range(len(diseases.keys()))]

    for disease in diseases.values():
        int_id = efo_id_to_int_id[disease['id']]
        mapping[int_id] = ([disease['id'], disease['name']])
        parents[int_id] = ([efo_id_to_int_id[efo_id] for efo_id in disease['parentIds']])

    with open(output_minified_filename, 'w') as f_output:
        json.dump({
            'mapping': mapping,
            'parents': parents
        }, f_output, separators=(',', ':'), sort_keys=True)

if __name__ == '__main__':
    filename = sys.argv[1]
    parse(filename)