'''
Pun Generator Component:
Phonotactics scores for a list of generated puns

Takes as input a list of ARPAbet words
Returns a dictionary with words as keys and scores as values.

Recall that lower scores = better words, because its a penalty system

Also included a sorter so we return puns in best to worst order in terms of phonotactics.
'''

from blick import BlickLoader

def getPhonScores(puns):

	b = BlickLoader()
	scoredPuns = {}
	
	for pun in puns:
		scoredPuns[pun] = b.assessWord(pun)

	return scoredPuns


def sortPuns(scoredPuns):

	scores = scoredPuns.values()
	scores.sort()
	sortedPuns = []

	for value in scores:
		for key in scoredPuns:
			if scoredPuns[key] == value and key not in sortedPuns:
				sortedPuns.append(key)

	return sortedPuns
	

print getPhonScores(["B N IH1 K","T EH1 S T", "R EH1 S T"])
x = getPhonScores(["B L IH1 K","T EH1 S T", "R EH1 S T"])
print sortPuns(x)
