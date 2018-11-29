'''
Pun Generator Component:
Getting list of words related to category input
'''

from __future__ import division
from nltk.corpus import wordnet as wn

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

print getRelated('fish')


'''
** Find way to add words if there aren't enough in hypo/hypernyms - like get hyper/hypo' hypers and hypos of related words.
** Cut down words if more than 20, using some similarity scoring
'''
'''
	#Maybe cut off at 20 most similar words if list is > 20
	if len(relatedSynsets) > 20:
		topScoreList = []
		for ss in relatedSynsets:
			score = wordSyn.path_similarity(ss)
			if len(topScoreList) < 20:
				topScoreList.append(ss)
			else:
				minScore = min(topScoreList)
				minIndex = topScoreList.index(min)
				if score > minScore:
					topScoreList[minIndex] = ss
	else:
		topScoreList = relatedWords

'''








