import csv
#import nltk.corpus.cmudict
#from syllabify import syllabify





#takes a word and returns a list of transcribed syllables
def transcribe(word):
	print('PLACEHOLDER')

def possiblePuns(word, phrase):
	punsList = []
	for syllable in phrase:
		if syllable == word[0]:
			dummyPun = []
			i = 0
			wordInserted = False
			for syllCount in range(len(phrase)):
				inBounds = True
				if (phrase[syllCount] == word[i]) and not wordInserted:
					while phrase[syllCount] == word[i] and inBounds:
						dummyPun.append(phrase[syllCount])
						print(dummyPun)
						if (i == len(word) - 1) or (syllCount == len(phrase) - 1):
							inBounds = False
						else:
							i += 1
							syllCount += 1
					for j in range (i, len(word)):
						dummyPun.append(word[i])
						print(dummyPun)
					wordInserted = True
				else:
					dummyPun.append(phrase[syllCount])
					print(dummyPun)
			punsList.append(dummyPun)
	return punsList


#modified version of implementation at https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshteinDistance(word1, word2):
    if len(word1) < len(word2):
        return levenshtein(word2, word1)

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



#Opens the CMU Dictionary and just maps all the orthographies to their transcriptions
#This doesn't handle words for which the dictionary has multiple pronunciations
#cmudict = nltk.corpus.cmudict.dict()
print(possiblePuns(['gruh', 'fi', 'ti'], ['por', 'naw', 'gruh', 'fi']))
