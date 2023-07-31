import re
from string import punctuation
from pythainlp.tokenize import word_tokenize
from spellchecker import SpellChecker
from pythainlp.spell import NorvigSpellChecker
from manage_word import load_dictionaries

tnc_dict, trie_dict = load_dictionaries()

# Separate Thai and English
def seperate_th_en(tokens):
	en_words = []
	th_words = []

	for token in tokens:
		if re.findall(r'[a-zA-Z]+', token):
			en_words.append(token)
		else:
			th_words.append(token)
	return en_words, th_words

# Clean text
def clean_content(text):
	punc = punctuation.replace(".", "")
	text = re.sub(f'[{re.escape(punc)}]', '', text)
	text = re.sub('@[a-zA-Z]+', '', text)
	text = re.sub('https?://\S+|www.\S+', '', text)
	text = re.sub('<.*?>', '', text)
	text = re.sub('[a-zA-Z\.]*/+[a-zA-Z\./0-9_\?]+', '', text)
	text = re.sub(r'\d+', '', text)
	text = re.sub(r'\s', '', text)
	text = re.sub(r'ฯ', '', text)
	text = re.sub('“','', text)
	text = re.sub('”', '', text)    
	text = re.sub('‘','', text)
	text = re.sub('’', '', text)
	return text

# English spell checker
def en_checker(words):
	en_result = []

	en_spell = SpellChecker()
	for word in words:
		correct_word = en_spell.correction(word)

		if correct_word is not None:
			if word not in correct_word:
				en_result.append({'word': word, 'suggest': en_spell.candidates(word)})
	return en_result

# Thai spell checker
def th_checker(words):
	th_result = []

	th_spell = NorvigSpellChecker(custom_dict=tnc_dict)
	for word in words:
		suggest_word = th_spell.spell(word)

		if word not in suggest_word:
			th_result.append({'word': word, 'suggest': suggest_word})
	return th_result

def spell_checker(input_text):
	# Word Tokenize
	tokens = word_tokenize(input_text, engine='newmm', custom_dict=trie_dict)
	
	## Text Preprocessing
	# Separate Thai and English
	en_words, th_words = seperate_th_en(tokens)
						
	# Clean text
	en_words = [ clean_content(x) for x in en_words ]
	th_words = [ clean_content(x) for x in th_words ]
	th_words = [ ele for ele in th_words if ele != '' ]   # Remove empty List from List

	## Spell Checker
	en_result = en_checker(en_words)    # English spell checker
	th_result = th_checker(th_words)    # Thai spell checker

	result = en_result + th_result

	return {"result": result, "tokens": tokens}