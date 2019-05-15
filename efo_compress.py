import sys
import json

output_filename = 'efo-graph.min.json'

def compress(filename):
    '''
    Input should be a JSON file containing a list of objects,
    each containing id, name and parentIds fields.

    Compression does the following:
    1. A words list is built from the words used across all
       disease names (ordered by frequency descending). The
       words in each name are then replaced with the index
       of each word in the words list.
    2. A diseases list is built from the diseases and efo
       ids are replaced by the index of the disease in the
       diseases list.
    3. The output per disease is an array with id, name and
       parentIds in positions 0, 1 and 2 respectively.
    '''
    with open(filename, 'r') as f_input:
        diseases = json.load(f_input)

    # build word lookup (word -> int)
    unique_word_frequencies = {}
    for disease in diseases:
        words = disease['name'].split()
        for w in words:
            if not w in unique_word_frequencies.keys():
                unique_word_frequencies[w] = 0
            unique_word_frequencies[w] += 1
    
    # build word list
    word_list = sorted(unique_word_frequencies.keys(), key=unique_word_frequencies.get, reverse=True)

    # compress names using word list
    word_to_id = {w: i for i, w in enumerate(word_list)}
    compressed_names = [{
        'id': d['id'],
        'compressedName': [word_to_id[w] for w in d['name'].split()],
        'parentIds': d['parentIds']
    } for d in diseases]

    # build efo_id lookup (efo_id -> int)
    efo_frequencies = {disease['id']: 0 for disease in diseases}
    for disease in diseases:
        for parent_id in disease['parentIds']:
            efo_frequencies[parent_id] += 1
    efo_list = sorted(efo_frequencies.keys(), key=efo_frequencies.get, reverse=True)
    efo_to_id = {efo: i for i, efo in enumerate(efo_list)}

    # build diseases list (and parents)
    ids_and_names = [[] for i in range(len(efo_list))]
    parents = [[] for i in range(len(efo_list))]
    for disease in compressed_names:
        int_id = efo_to_id[disease['id']]
        ids_and_names[int_id] = [disease['id'], disease['compressedName']]
        parents[int_id] = [efo_to_id[efo] for efo in disease['parentIds']]

    # build top level object
    compressed = {
        'words': word_list,
        'diseases': ids_and_names,
        'parents': parents
    }

    with open(output_filename, 'w') as f_output:
        json.dump(compressed, f_output, separators=(',', ':'), sort_keys=True)


if __name__ == '__main__':
    filename = sys.argv[1]
    compress(filename)