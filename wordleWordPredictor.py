import json
import random
inpWordleWordsFromFile = [] 

greyAlphabetSet = set()
greenPlaceDict = {}   # This will hold data like, { 1:"g",    } -> position:"alphabet" - postion here is 0 based
yellowAlphabetDict = {}   # This will hold data like,{ 'k':{0}, 'a':{1,4} } 
goodAlphabetCountFoundTillNow = {} #This will hold data like {"f":2} -> "alphabet":count

GREEN_ALTERNATE_STRING = "n"
YELLOW_ALTERNATE_STRING = "y"
GREY_ALTERNATE_STRING = "g"

def initializeWordleWords(txtFilePath):
    try:
        txtFile = open( txtFilePath, "r" )
        txtFileContents = txtFile.read()
        # print(txtFileContents)
        # print(len(txtFileContents))

    finally:
        txtFile.close()

    #print(len(txtFileContents))
    global inpWordleWordsFromFile 
    inpWordleWordsFromFile = json.loads( txtFileContents  )


# updateProbaleWordList
def updateHintInformation(lastWordPredicted, hintsRecieved):
    hintsArr = hintsRecieved.split(",")
    print(hintsArr  )
    hintsArrParsed = []
    for x in hintsArr:
        position = int(x.split('-')[0])
        alphabet = x.split('-')[1]  #lastWordPredicted[position]
        colour = x.split('-')[2]
        hintsArrParsed.append( {"position":position, "colour":colour, "alphabet":alphabet}  )
    
    goodAlphabetCountInCurrentHint = {}
    for x in hintsArrParsed:
        #We will only process for green or yellow characters here
        #for grey we will update only if it is not present in info set for yellow or green
        #the reason is suppose the word is Smart, we predicted Smash, the 's' present in 3rd index in Smash will be shown as grey
        #And as per our logic we are keeping those alphabets in the info set for grey alphabets if it does not appear in the word at all
        if x["colour"] == GREEN_ALTERNATE_STRING: #green
            greenPlaceDict[x["position"]] =  x["alphabet"]
        elif x["colour"] == YELLOW_ALTERNATE_STRING: #yw - yellow
            if x["alphabet"] not in yellowAlphabetDict:
                yellowAlphabetDict[ x["alphabet"] ] = { x["position"] }  #this is a set 
            else:
                #check if this yellow for the alphabet was in the same place 
                yellowAlphabetDict[ x["alphabet"] ].add( x["position"]   )
        
        #updating the count
        if x["colour"] == GREEN_ALTERNATE_STRING or x["colour"] == YELLOW_ALTERNATE_STRING:
            if x["alphabet"] in goodAlphabetCountInCurrentHint:
                goodAlphabetCountInCurrentHint[ x["alphabet"] ] += 1
            else:
                goodAlphabetCountInCurrentHint[ x["alphabet"] ] = 1

    for x in hintsArrParsed:
        if x["colour"] == GREY_ALTERNATE_STRING and x["alphabet"] not in greenPlaceDict.values() and  x["alphabet"] not in yellowAlphabetDict.keys() : #grey
            greyAlphabetSet.add( x["alphabet"] )


    #Updating the count info
    for alpha in goodAlphabetCountInCurrentHint:
        if alpha in goodAlphabetCountFoundTillNow:
            goodAlphabetCountFoundTillNow[alpha] = max( goodAlphabetCountFoundTillNow[alpha], goodAlphabetCountInCurrentHint[alpha]  )
        else:
            goodAlphabetCountFoundTillNow[alpha] = goodAlphabetCountInCurrentHint[alpha]

    


def passForGreyAlphabetSet(word:str):
    global greyAlphabetSet
    return len( set(word).intersection(greyAlphabetSet)  ) == 0 #intersection between grey alphabet set and characters of word should be null

def passForGreenPlaceDict(word:str):
    global greenPlaceDict
    for key,val in greenPlaceDict.items():
        if word[key] != val:
            return False
    return True

def passForYellowAlphabetDict(word:str):
    global yellowAlphabetDict
    for alphabet in yellowAlphabetDict.keys():
        for place in yellowAlphabetDict[alphabet]:
            if word[place] == alphabet:
                return False
    
    return True

def passForGoodAlphabetCountFoundTillNow(word:str):
    global currentWordAlphabetCountSet
    currentWordAlphabetCountSet = {}
    for alphabet in word:
        if alphabet in currentWordAlphabetCountSet:
            currentWordAlphabetCountSet[ alphabet ] += 1
        else:
            currentWordAlphabetCountSet[ alphabet ] = 1

    #In current word the count for alphabet should be same or greater than that count in goodAlphabetCountFoundTillNow
    #Because then only it can be a possible answer if we look into count only
    for alphabet, countInGoodAlphabetSet in goodAlphabetCountFoundTillNow.items():
        if currentWordAlphabetCountSet.get( alphabet, 0) < countInGoodAlphabetSet:
            return False
        
    return True
        


def filterWordsFromTheListUsingHint( wordsList):
    filteredWordList = []
    global greyAlphabetSet
    global greenPlaceDict
    global yellowAlphabetDict
    global goodAlphabetCountFoundTillNow
    for word in wordsList:
        if (passForGreyAlphabetSet(  word  ) and passForGreenPlaceDict(word) 
            and passForYellowAlphabetDict(word) and passForGoodAlphabetCountFoundTillNow(word)
        ):
            filteredWordList.append( word )

    return filteredWordList

def chooseARandomWordFromTheList( wordList  ): 
    print( f"choosing a random word from list of {len(wordList)} words"  )
    if len( wordList ) == 0:
        raise Exception("There is no more words left in the probable list. Can't guess anymore")
    randomIdx = random.randint(0, len(wordList) -1)
    return wordList[randomIdx]

def main():
    global greyAlphabetSet
    global greenPlaceDict
    global yellowAlphabetDict
    global goodAlphabetCountFoundTillNow
    global inpWordleWordsFromFile

    initializeWordleWords(".\combined_5_letter_word.txt")
    
    totalNoOfHints = 6
    remainingProbableWordleWords = inpWordleWordsFromFile
    for i in range( 0, totalNoOfHints):
        randomWordFromList = chooseARandomWordFromTheList( remainingProbableWordleWords )
        print( f"hint no-{i+1}-", randomWordFromList  )
        print( f"waiting for hint from the user, given by wordle, please write in correct format" )
        hintFromWordle:str = input()
        updateHintInformation(randomWordFromList, hintFromWordle)
        remainingProbableWordleWords = filterWordsFromTheListUsingHint( remainingProbableWordleWords  )
    
    print(  remainingProbableWordleWords  )
if __name__ == "__main__":
    main()

#***************************************************Test-1 Unit test for updateHintInformation****************************************/
# # Suppose the word is -> adrde
# # First prediction made 
# # 	word:sdteg
# #       hint:0-gy,1-gn,2-gy,3-yw,4-gy
# # Second prediction made 
# # 	word:bderd
# #       hint:0-gy,1-gn,2-yw,3-yw,4-yw


# updateHintInformation( "sdteg", "0-gy,1-gn,2-gy,3-yw,4-gy" )
# print( greyAlphabetSet)
# print(  greenPlaceDict )
# print(  yellowAlphabetDict )
# print(  goodAlphabetCountFoundTillNow )
# print("---------------------------Separator-------------------------------")
# updateHintInformation("bderd", "0-gy,1-gn,2-yw,3-yw,4-yw")
# print( greyAlphabetSet)
# print(  greenPlaceDict )
# print(  yellowAlphabetDict )
# print(  goodAlphabetCountFoundTillNow )
# print("---------------------------Separator-------------------------------")

# wordsList = ["bderd", "adecd", "cdrde","adrde"]
# returnedWordList = filterWordsFromTheListUsingHint( wordsList )
# print(  returnedWordList)
#***************************************************Above was Unit test for updateHintInformation****************************************/


# ******************************** Test 2 *********************************************
# updateHintInformation( "email", "0-e-n,1-m-n,2-a-n,3-i-n,4-l-n" )
# print("herr")
# print( greyAlphabetSet)
# print(  greenPlaceDict )
# print(  yellowAlphabetDict )
# print(  goodAlphabetCountFoundTillNow )


# initializeWordleWords( "./wordsExtractor/youtube_guy_5_letter_words.txt" )
# remainingWordList = filterWordsFromTheListUsingHint( inpWordleWordsFromFile  )

# print(remainingWordList)
# ******************************** Test 2 above *********************************************