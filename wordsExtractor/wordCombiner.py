import json
def initializeWordleWords(txtFilePath):
    try:
        txtFile = open( txtFilePath, "r" )
        txtFileContents = txtFile.read()
        # print(txtFileContents)
        # print(len(txtFileContents))

    finally:
        txtFile.close()

    #print(len(txtFileContents))
    inpWordleWordsFromFile = json.loads( txtFileContents  )
    return inpWordleWordsFromFile

_7eslWordList = initializeWordleWords("C:/Users/SYR00242/Learning/wordle/wordsEctractor/_7_esl_5_letter_words_archieve_1.txt")
youtubeGuyWordList = initializeWordleWords("C:/Users/SYR00242/Learning/wordle/wordsEctractor/youtube_guy_5_letter_words.txt")


combinedWordSet = set()

for word in _7eslWordList:
    combinedWordSet.add(  word.lower() )

for word in youtubeGuyWordList:
    combinedWordSet.add(  word.lower() )


print( len(_7eslWordList),  len(youtubeGuyWordList), len(combinedWordSet)  )


combinedWordList = list(combinedWordSet)
try:
    txtFilePathToWrite = "combined_5_letter_word.txt"
    txtFile = open( txtFilePathToWrite, "w" )
    txtFile.write( json.dumps( combinedWordList ) )
finally:
    txtFile.close()


