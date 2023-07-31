from pythainlp.corpus import tnc
from pythainlp.util import dict_trie

# Define file paths for dictionary files
TNC_DICT_FILE = 'dictionary/tnc_dict.txt'
TRIE_DICT_FILE = 'dictionary/trie_dict.txt'

def load_dictionaries():
    # Load TNC Dict file
    try:
        with open(TNC_DICT_FILE, 'r', encoding='utf-8') as f:
            tnc_dict = [line.split('\t') for line in f]
            tnc_dict = [(word, int(freq)) for word, freq in tnc_dict]
    except FileNotFoundError:
        tnc_dict = set(tnc.word_freqs())    # If the TNC Dict file is not found, using the default TNC word frequencies

    # Load Trie Dict file
    try:
        with open(TRIE_DICT_FILE, 'r', encoding='utf-8') as f:
            trie_dict = {line.strip(): 1 for line in f.readlines()}
            trie_dict = dict_trie(dict_source=trie_dict)
    except FileNotFoundError:
        trie_dict = {word: 1 for word in tnc_dict if word}      # If the Trie Dict file is not found, generate a Trie dictionary from the TNC Dict words

    return tnc_dict, trie_dict

def save_dictionaries(tnc_dict, trie_dict):
    # Save TNC Dict file
    with open(TNC_DICT_FILE, 'w', encoding='utf-8') as f:
        for word, freq in tnc_dict:
            f.write(f"{word}\t{freq}\n")

    # Save Trie Dict file
    with open(TRIE_DICT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(trie_dict))

def add_new_word(new_word):
    global tnc_dict
    global trie_dict
    
    if new_word and isinstance(new_word, str):
        tnc_dict = set(tnc_dict)
        tnc_dict.add((new_word, 10))

        trie_dict = [x[0] for x in tnc_dict if x[0]]
        trie_dict = dict_trie(dict_source=trie_dict)

        save_dictionaries(tnc_dict, trie_dict)      # Save the updated dictionaries to files

        return True
    else:
        return False

# Load the dictionaries
tnc_dict, trie_dict = load_dictionaries()