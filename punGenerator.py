import csv
import nltk
import getPhonScores
import transliterate
from getRelated import getRelBasic
from getRelated import getRelatedGlove
from syllabify import syllabify

#import python-Levenshtein
#import nltk.corpus.cmudict
#from syllabify import syllabify





#takes a word and returns a list of transcribed syllables
def transcribe(word):
	transcription = []
	cmuDict = nltk.corpus.cmudict.dict()
	try:
		syllabified =  syllabify(cmuDict[word][0])
		for syllable in syllabified:
			dummyStr = ""
			for segment in syllable[0]:
				dummyStr += segment + " "
			for segment in syllable[1]:
				dummyStr += segment + " "
			for segment in syllable[2]:
				dummyStr += segment + " "
			transcription.append(dummyStr.strip())
		return transcription
	except Exception as e:
		return "NOT IN DICTIONARY"


#modified version of implementation at https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshteinDistance(word1, word2):
    if len(word1) < len(word2):
        return levenshteinDistance(word2, word1)

    # len(word1) >= len(word2)
    if len(word2) == 0:
        return len(word1)

    previous_row = range(len(word2) + 1)
    for i, c1 in enumerate(word1):
        current_row = [i + 1]
        for j, c2 in enumerate(word2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than word2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


'''
Tries to insert the whole word into a phrase. 
Matches as much of the word to given phrase as possible, for example:
"tiffany" + "kneecap" => "tiffa-kneecap", but
"avenue" + "avalanche" => "avalanche-nue"
'''
def wholeWordInsert(word, phrase):
	punsList = []
	punBase = []
	dummyPun = []
	i = 0
	while(i < len(phrase)):
		if phrase[i] == word[0]:
			dummyPun = punBase[:]
			j = 0
			while (j < len(word)):
				if i < len(phrase):
					if phrase[i] == word[j]:
						dummyPun.append(phrase[i])
						punBase.append(phrase[i])
						i +=1
						j +=1
					else:

						dummyPun += word[j:]
						dummyPun += phrase[i:]
						j = len(word) + 1
				else:
					dummyPun += word[j:]
					j = len(word) + 1
			punsList.append((dummyPun, word))
		if (i < len(phrase)):
			punBase.append(phrase[i])
		i += 1
	return punsList

'''
Inserts the first syllable of word somewhere into phrase 
if the levenshtein distance is <= 2 and >0
"womb" + "room on fire" => "womb on fire"
"bark" + "parking lot" => "barking lot"
etc.
'''
def firstSyllableInsert(word, phrase):
	insertions = []
	if len(word) == 1:
		for i in range(len(phrase)):
			if levenshteinDistance(word[0], phrase[i]) <= 2 and levenshteinDistance(word[0], phrase[i]) > 0:
				dummyPhrase = phrase[:]
				dummyPhrase[i] = word[0]
				insertions.append(dummyPhrase)

		return insertions
	else:
		return []

def possiblePuns(word, phrase, orthography):
	puns = []
	for pun in firstSyllableInsert(word, phrase):
		puns.append((pun, orthography))
	for pun in wholeWordInsert(word, phrase):
		puns.append((pun, orthography))
	return puns


'''
The big one.
Phrase and topic are strings
'''

def generatePuns(phrase, topic):
	relatedWords = getRelatedGlove("closestWords10k.csv",topic)
	relatedWordsArpa = []
	phraseArpa = []

	for word in relatedWords:
		transcription = transcribe(word)
		if transcription != "NOT IN DICTIONARY":
			relatedWordsArpa.append((transcription, word))

#testing change
	for word in phrase.split():
		phraseArpa += transcribe(word)
		phraseArpa.extend("#")

	punsList = []
	for wordPair in relatedWordsArpa:
		word = wordPair [0]
		dummyPunsList = possiblePuns(word, phraseArpa, wordPair[1])
		for pun in dummyPunsList:
			if pun != []:
				punsList.append((pun, wordPair[1]))

	punsListStrings = []
	punOrigins = {}
	for punPair in punsList:
		pun = punPair[0]
		print(pun)
		punString = ""
		for syllable in pun[0]:
			punString+= syllable + " "
		punString = punString.strip()
		punsListStrings.append(punString)
		punOrigins[punString] = punPair[1]


	punsList = getPhonScores.sortPuns(getPhonScores.getPhonScores(punsListStrings))

	finalList = []
	for pun in punsList:
		finalList += (transliterate.transliterate([pun], phrase), punOrigins[pun])

	
	return finalList

print(str(generatePuns("black leather jacket", "finance")))

