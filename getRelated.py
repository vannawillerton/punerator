'''
Pun Generator Component:
Getting list of words related to category input
'''
from __future__ import division
from nltk.corpus import wordnet as wn
from collections import defaultdict
import csv

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
** Find way to add words if there aren't enough in hypo/hypernyms?? - like get hypers and hypos of related words.

** This v is perhaps not ideal but it works now
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
	if len(relatedWords) > 10:
		scores = []
		scoredWords = {}
		out = []
		for key in relatedWords:
			score = wordSS[0].path_similarity(relatedWords[key])
			scores.append(score)
			scoredWords[key] = score 
		scores.sort()
		
		for value in scores:
			for key in scoredWords:
				if (len(out) < 15) and (scoredWords[key] == value) and (key not in out):
					out.append(key)

		for ss in wordSS:
			for w in ss.lemma_names():
				if (len(out) < 25) and (w.lower() not in out) and ('_' not in w):
					out.append(w.lower())
	
		return out
	

	#4 add in lemma names (these are good ones)
	for ss in wordSS:
		for w in ss.lemma_names():
			if (w.lower() not in relatedWords.keys()) and ('_' not in w):
				relatedWords[w.lower()] = 0

	return relatedWords.keys()

def getRelatedGlove(filename, word):
	with open(filename) as csvfile:
		readList = list(csv.reader(csvfile, delimiter=','))
		for row in readList:
			if row[0] == word:
				return row[1:]

#print getRelated('fish')



