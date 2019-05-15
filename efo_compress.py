import sys
import json

output_filename = 'efo-graph.min.json'

def compress(filename):
    '''
    Input should be a JSON file containing a list of objects,
    each containing id, name and parentIds fields.

    Compression does the following:
    1. A wordList is built from the words used across all
       disease names (ordered by frequency descending). The
       words in each name are then replaced with the index
       of each word in the wordList.
    2. The output per disease is an array with id, name and
       parentIds in positions 0, 1 and 2 respectively.
    '''
    with open(filename, 'r') as f_input:
        diseases = json.load(f_input)

    unique_word_frequencies = {}
    for disease in diseases:
        words = disease['name'].split()
        for w in words:
            if not w in unique_word_frequencies.keys():
                unique_word_frequencies[w] = 0
            unique_word_frequencies[w] += 1
    
    word_list = sorted(unique_word_frequencies.keys(), key=unique_word_frequencies.get, reverse=True)
    word_to_id = {w: i for i, w in enumerate(word_list)}

    compressed_diseases = [[
        d['id'],
        [word_to_id[w] for w in d['name'].split()],
        d['parentIds']
     ] for d in diseases]

    compressed = {
        'wordList': word_list,
        'diseases': compressed_diseases
    }

    with open(output_filename, 'w') as f_output:
        json.dump(compressed, f_output, separators=(',', ':'), sort_keys=True)


if __name__ == '__main__':
    filename = sys.argv[1]
    compress(filename)