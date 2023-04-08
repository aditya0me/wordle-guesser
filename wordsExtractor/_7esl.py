import requests
import bs4
import html5lib
import json

baseUrl = "https://7esl.com/5-letter-words/"
baseUrlRequest = requests.get( baseUrl , headers={'User-Agent': 'Mozilla/5.0'})
# print(received.content)

baseSoup = bs4.BeautifulSoup( baseUrlRequest.content, "html5lib"  )
# print(baseSoup.prettify())
urlsToCheck = {baseUrl}
for x in baseSoup.select("body main ul li a"):
    # print(x.get("href"))
    link = x.get("href")
    if "https://7esl.com" in link and "5-letter" in link and "#" not in link:
        # print(link)
        urlsToCheck.add(link)

# print(len(urlsToCheck) )
# for x in urlsToCheck:
#     print(x)



def extractFiveLetterWordFromTheUrlAndKnownCssSelctor(siteLink, setToAdd):
    siteLinkResponse = requests.get(siteLink, headers={'User-Agent': 'Mozilla/5.0'} )
    soup = bs4.BeautifulSoup( siteLinkResponse.content, "html5lib"  )

    for itr in soup.select("body main ul li"):
        textVal = itr.text.strip()
        if len(textVal) == 5:
        #     print(textVal)
            setToAdd.add(textVal)

    print(f"length of setToAdd->{siteLink}->{len(setToAdd)}")

globalWordSet = set()
for url  in urlsToCheck:
    extractFiveLetterWordFromTheUrlAndKnownCssSelctor( url, globalWordSet )

globalWordList = list(globalWordSet)
try:
    txtFilePathToWrite = "_7_esl_5_letter_words.txt"
    txtFile = open( txtFilePathToWrite, "w" )
    txtFile.write( json.dumps( globalWordList ) )
finally:
    txtFile.close()