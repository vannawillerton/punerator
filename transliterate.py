'''
Function to translate back to 'English' orthographic spelling

Uses dictionary to define rudimentary mapping between arpabet symbols and english orthographic spelling. Unfortunately English orthography is not transparent or consistent so this will be bad.
'''
import nltk

symbolMap = {'P': 'p', 'B': 'b', 'F': 'f', 'V': 'v', 'M': 'm', 'W': 'w', 'TH': 'th', 'DH': 'th', 'T': 't', 'D': 'd', 'S': 's', 'Z': 'z', 'N': 'n', 'L': 'l', 'CH': 'ch', 'JH': 'j', 'SH': 'sh', 'ZH': 'z', 'K': 'k', 'G': 'g', 'R': 'r', 'NG': 'ng', 'Y': 'y', 'HH': 'h', 'IY1': 'ee', 'IH1': 'i', 'EY1': 'ai', 'EH1': 'e', 'AE1': 'a', 'AA1': 'o', 'A01': 'ough', 'AH1': 'u', 'OW1': 'oa', 'UH1': 'oo', 'UW1': 'oo', 'AY1': 'i', 'AW1': 'ou', 'OY1': 'oy', 'ER1': 'er', 'IY2': 'e', 'IH2': 'i', 'EY2': 'ei', 'EH2': 'e', 'AE2': 'a', 'AA2': 'o', 'AO2': 'aw', 'AH2': 'u', 'OW2': 'o', 'UH2': 'oo', 'UW2': 'ou', 'AY2': 'i', 'AW2': 'ou', 'OY2': 'oi', 'ER2': 'er', 'IY0': 'y', 'IH0': 'i', 'AH0': 'a', 'OW0': 'o', 'UW0': 'u', 'ER0': 'er'}

def transliterate(punsList, phrase):
	orthographic = []
	splitPunsList = []
	phrase = phrase.split(' ')
	cmuDict = nltk.corpus.cmudict.dict()
	
	for pun in punsList:
		pun = pun.split('#')
		del pun[len(pun)-1]
		splitPunsList.append(pun)

	j = 0
	while j < len(splitPunsList):
		i = 0
		orthographic.append([])
		for word in splitPunsList[j]:
			splitWord = word.strip().split(' ')
			if splitWord in cmuDict[phrase[i]]:
				orthographic[j].append(phrase[i])
		#NEW
			else:
				orthWord = []
				for l in splitWord:
					orthWord.append(symbolMap[l])
				orthWord = ''.join(orthWord)
				orthographic[j].append(orthWord)
		#END NEW
			i+=1
		j+=1	

	i = 0
	while i < len(orthographic):	
		orthographic[i] = ' '.join(orthographic[i])
		i+=1

	return orthographic

