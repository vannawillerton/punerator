'''
Pun Generator Component:
Getting list of words related to category input
'''

from __future__ import division
from nltk.corpus import wordnet as wn
from collections import defaultdict

def getRelBasic(word):
	#1 Build the list of potential related sysents/words from wn
	wordSS = wn.synsets(word)
	relatedWords = []
	relatedSynsets = []

	for ss in wordSS:
		for w in ss.lemma_names():
			if (w.lower() not in relatedWords) and ('_' not in w):
				relatedWords.append(w.lower())
		for ss in ss.hyponyms():
			w = ss.name().partition('.')[0]
			if (w.lower() not in relatedWords) and ('_' not in w):
				relatedWords.append(w.lower())
		for ss in ss.hypernyms():
			w = ss.name().partition('.')[0]
			if (w.lower() not in relatedWords) and ('_' not in w):
				relatedWords.append(w.lower())

	return relatedWords	

#print getRelBasic('good')


'''
** Find way to add words if there aren't enough in hypo/hypernyms - like get hypers and hypos of related words.
'''

def getRelated(word):
	#1 Build the list of potential related sysents/words from wn
	wordSS = wn.synsets(word)
	relatedWords = {}

	for SS in wordSS:
		for ss in SS.hyponyms():
			w = ss.name().partition('.')[0]
			if (w.lower() not in relatedWords.keys()) and ('_' not in w):
				relatedWords[w.lower()] = ss
		for ss in SS.hypernyms():
			w = ss.name().partition('.')[0]
			if (w.lower() not in relatedWords.keys()) and ('_' not in w):
				relatedWords[w.lower()] = ss

	#3 cut list down if too long. Keep most similar words (using path sim)
## FIX THIS SO SCORE DICT CORRESPONDS WITH TOPSCORING
	if len(relatedWords.keys()) > 10:
		score = {}
		topScoring = {}
		for ss in relatedWords.values():
			w = ss.name().partition('.')[0]
			scoretmp = wordSS[0].path_similarity(ss)
			score[scoretmp] = ss 
		## MAYBE SPLIT HERE. LIKE GET ALL SCORES AND THEN CONTINUE ON
		#while len(topScoring) < 15:
			#topScoring[ss] = something
 			if (len(topScoring) < 10):
				topScoring[ss] = w.lower()
			else:
				minScore = min(score.keys())
				if scoretmp > minScore:
					topScoring[score[minScore]] = w.lower()
					topScoring[score[scoretmp]] = topScoring[score[minScore]]
					del topScoring[score[minScore]]
		
		for ss in wordSS:
			for w in ss.lemma_names():
				if (w.lower() not in topScoring.values()) and ('_' not in w):
					topScoring[ss] = w.lower()

		return topScoring.values()
		

	#4 add in lemma names (these are good ones)
	for ss in wordSS:
		for w in ss.lemma_names():
			if (w.lower() not in relatedWords.keys()) and ('_' not in w):
				relatedWords[w.lower()] = 0

	return relatedWords.keys()

print getRelated('good')




