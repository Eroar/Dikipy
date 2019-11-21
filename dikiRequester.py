import sys

import requests
from bs4 import BeautifulSoup

def getDikiUrl(lang):
    if lang == "de":
        return "https://www.diki.pl/slownik-niemieckiego"
    elif lang == "en":
        return "https://www.diki.pl/slownik-angielskiego"
    else:
        raise ValueError(f'The language{lang} is not supported. Use \"en\" or \"de\" as arguments.')

def getWordFromSoup(soup: BeautifulSoup):
    try:
        try:
            word = soup.find("ol", {"class": "foreignToNativeMeanings"}).find("span", {"class":"hw"}).find("a", {"class" : "plainLink"})
            word = word.text
        except:
            word = soup.find("ol", {"class": "nativeToForeignEntrySlices"}).find("span", {"class":"hw"}).find("a", {"class" : "plainLink"})
            word = word.text
    except:
        try:
            word = soup.find("ol", {"class": "foreignToNativeMeanings"}).find("span", {"class":"hw"}).find("a", {"class" : "plainLink"})
            word = word.text
        except:
            word = "No word found"
    return word

def getSoupSimple(response):
    return BeautifulSoup(response.text, "html.parser")


def getResponse(url: str, word: str):
    return requests.get(url + "?q=" + word)

def getSoupFromUrl(url, word):
    response = getResponse(url, word)
    return getSoupSimple(response)

def translate(word, lang):
    soup = getSoupFromUrl(getDikiUrl(lang), word)
    return getWordFromSoup(soup)

if __name__ == "__main__":
    args = sys.argv[1:]
    lang = ""
    infiniteMode = False
    sentenceMode = False
    separate = False

    #for debuging    
    test = False
    wordsToTest = ["word", "tree", "jabłko", "eeee", "cześć"]

    if "-lang" not in args:
        print("no language specified")
        quit()
    
    for arg, i in zip(args, range(len(args))):
        if arg == "-lang":
            lang = args[i+1]
        elif arg == "-i":
            infiniteMode = True
        elif arg == "-test":
            test = True
        elif arg == "-s":
            sentenceMode = True
        elif arg == "-ss":
            sentenceMode = True
            separate = True

    if test:
        print("TESTING")
        for word in wordsToTest:
            print(word, ":", translate(word, lang))
        print("DONE TESTING\n")

    if infiniteMode:
        while True:
            if sentenceMode:
                words = input("Sentence to translate: ").split(" ")
                translation = ""
                for word, i in zip(words, range(len(words))):
                    translation += translate(word, lang) + " "
                    if separate and i+1!=len(words):
                        translation += "| "
                print(translation)

            else:
                word = input("Word to translate: ")
                print(translate(word, lang))