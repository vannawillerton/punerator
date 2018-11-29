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

#print getRelBasic('fish')


'''
** Find way to add words if there aren't enough in hypo/hypernyms - like get hyper/hypo' hypers and hypos of related words.
** Cut down words if more than 20, using some similarity scoring
'''

def getRelated(word):
	#1 Build the list of potential related sysents/words from wn
	wordSS = wn.synsets(word)
	relatedWords = {}

	for SS in wordSS:
		for ss in SS.hyponyms():
			w = ss.name().partition('.')[0]
			if (w.lower() not in relatedWords) and ('_' not in w):
				relatedWords[w.lower()] = ss
		for ss in SS.hypernyms():
			w = ss.name().partition('.')[0]
			if (w.lower() not in relatedWords) and ('_' not in w):
				relatedWords[w.lower()] = ss

	#2 Cut list down if too long. Keep most similar words (using path sim)
	if len(relatedWords.keys()) > 15:
		score = {}
		topScoring = {}
		for ss in relatedWords.values():
			w = ss.name().partition('.')[0]
			scoretmp = wordSS[0].path_similarity(ss)
			score[scoretmp] = ss 
			if len(topScoring) < 15:
				topScoring[ss] = w.lower()
			else:
				minScore = min(score.keys())
				if scoretmp > minScore:
					topScoring[score[minScore]] = w.lower()
		
		for ss in wordSS:
			for w in ss.lemma_names():
				if (w.lower() not in relatedWords) and ('_' not in w):
					topScoring[ss] = w.lower()

		return topScoring.values()
		

	#3 Pad up list if too short
	#TO DO still

	#4 add in lemma names (good ones)
	for ss in wordSS:
		for w in ss.lemma_names():
			if (w.lower() not in relatedWords) and ('_' not in w):
				relatedWords[w.lower()] = 0

	return relatedWords.keys()

print getRelated('fish')




