import os

print os.getcwd ()

os.chdir ("Directory Path") #Example for directory path might be like "C:\Users\Username\Desktop\IntentDirectory



#glob is used for accessing documents within a directory
import glob

#These libraries are for cleaning text data
#re is the Python library for Regular Expressions
import re

#nltk is the python library for Natural Language Processing (used here for cleaning non-English text from the data)
from nltk.corpus import brown
from nltk.corpus import words
from nltk.corpus import cess_esp as spanish
from nltk.corpus import reuters
from nltk.corpus import nps_chat

#These dictionaries are used to reduce time required to search for English words by implementing a hash search in "isEnglishWord"
englishBrownDict = dict.fromkeys (brown.words (), True)
englishWordsDict = dict.fromkeys (words.words (), True)
englishReutersDict = dict.fromkeys (reuters.words (), True)
englishChatDict = dict.fromkeys (nps_chat.words (), True)

spanishWordsDict = dict.fromkeys (spanish.words (), True)

malayText = open (os.path.join (os.getcwd (), "malayUpdated.txt"))
malayWordsDict = []

for line in malayText:
    
    malayWordsDict.append (line)
    
#print "Count of malay words: ", len (malayWords), "\n"
#malayWordsDict = dict.fromkeys (malayWords, True)



commonTweetWords = ["ur", "u", "youre", "gonna", "wanna", "wannabe", "shoulda", "should've", "coulda", "could've", "woulda", "would've", "thats", "that's", "whats", "what's", "hadnt", "hadn't", "couldnt", "couldn't", "wouldnt", "wouldn't", "shouldnt", "shouldn't", "didnt", "didn't", "mustnt", "mustn't", "cant", "can't", "shant", "shan't", "wont", "won't", "dont", "don't", "retweet", "rt", "smh", "omg", "lol", "ha", "haha", "hahaha", "ok", "okay", "lmao", "lmbo", "rofl", "roflol", "im", "i'm", "imma", "ive", "i've", "he's", "she's", "we've", "weve", "they've", "theyve", "theyre", "they're", "we're", "dammit", "af", "fuck", "fucks", "shit", "bro", "bruh", "homie", "loves", "hates", "hater", "haters", "luv", "noone", "rip", "r.i.p.", "chester", "bennington", "malyasia", "malaysia's", "hotline", "hl", "its", "it's"]

suicideDepressionWords = ["depressed", "depression", "hopeless", "alone", "worthless", "empty", "suicide", "suicidal", "pain", "anxiety"]

#Establish the nltk tools
#Will use nltk.corpus.words.words ()



originalSaveDirectory = os.path.join (os.getcwd (), "responseSaveDirectory")

newSaveDirectory = os.path.join (os.getcwd (), "responseSaveDirectoryNew")


usernameResponseDictionary = {}


def isEnglishBrown (word):
    
    try:
        
        x = englishBrownDict [word]
        
    except Exception as e:
        
        x = False
        
    return x



def isEnglishWord (word):
    
    try:
        
        x = englishWordsDict [word.lower ()]
        
    except Exception as e:
        
        x = False
        
    return x
    


def isEnglishReuters (word):
    
    try:
        
        x = englishReutersDict [word]
        
    except Exception as e:
        
        x = False
        
    return x
    
    
    
def isEnglishChat (word):
    
    try:
        
        x = englishChatDict [word]
        
    except Exception as e:
        
        x = False
        
    return x
        
        

def isSpanishWord (word):
    
    try:
        
        x = spanishWordsDict [word]
        
    except Exception as e:
        
        x = False
        
    return x
        


def isMalayWord (word):
    
    x = False
    
    if word.lower () in malayWordsDict:
        
        x = True
        
    return x



def extractText (child, line, textType):
    
    #print "Entered extractText function \n\n"
    
    if child != "" and child != None:
        
        currentUsername = child.split ("2017") [0]
        currentUsername = currentUsername [0: len(currentUsername) - 1]
        
        textData = ""
        
        if textType == "Message Text":
            
            textData = line [line.find ("Message Text:"): line.find ("Message User:")]
            
            textData = re.sub ('Message Text:', '', textData)
            
        else:
            
            textData = line [line.find ("Response Text:"): line.find ("Response User:")]
            
            textData = re.sub ('Response Text:', '', textData)
            
            
        #CLEAN the textData before linking it to the Username
        
        #print "Attempting to clean up the textData with regex\n\n"
        
        try:
        
            #Attempt a Regular Expression to catch ANY URL
            regexURL = "(https://|http://)" #(\w*[0-9]*(-)*)*\.\w*/(\w*[0-9]*(-)*(_)*)*/*
            #Attempt a Regular Expression to catch ANY @Username mention
            regexUsername = "@((-)*(_)*\w+[0-9]*(-)*(_)*)"
            #Attempt a Regular Expression to catch ANY #Hashtag
            regexHashtag = "#((-)*(_)*\w+[0-9]*(-)*(_)*)"
            
            #regexString = regexURL + regexUsername + regexHashtag
            
            regexListURL = re.findall (regexURL, textData)
            regexListUsername = re.findall (regexUsername, textData)
            regexListHashtag = re.findall (regexHashtag, textData)
            
            #print "Just ran the re.findall function for the regexURL, regexUsername, and regexHashtag in the current textData\n\n"
            
            #print "textData: ", textData, "\n\n"
    
            #print "regexListURL: ", regexListURL, "\n"
            #print "regexListUsername: ", regexListUsername, "\n"
            #print "regexListHashtag: ", regexListHashtag, "\n"
            
            for url in regexListURL:
                
                if url == "http://" or url == "https://":
                    
                    #print "Current URL: ", url, "\n"
                    #
                    #print "URL in textData: ", textData [textData.find (url): textData [textData.find (url)].find (" ")]
                    
                    urlStartIndex = textData.find (url)
                    
                    urlEndIndex = textData [textData.find (url)].find (" ")
                    
                    urlString = textData [urlStartIndex: urlEndIndex]
                    
                    textData = textData.replace (urlString, "") #re.sub (urlString, "", textData)
                    
            for item in regexListUsername:
                
                for username in item:
                
                    if len (username) > 4:
                        
                        #print "Current Username: ", username, "\n"
                        
                        textData = textData.replace ("@" + username, "") #re.sub ("@" + username, "", textData)
                        
                        textData = textData.replace (":", "")
                        textData = textData.replace (".", "")
                        textData = textData.replace (",", "")
                        textData = textData.replace ("&amp", "")
                        textData = textData.replace ("&lt", "")
                        textData = textData.replace ("&gt", "")
                        textData = textData.replace ("&nbsp", "")
                        
                    
            for item in regexListHashtag:
                
                for hashtag in item:
                
                    if len (hashtag) > 1:
                        
                        #print "Current Hashtag: ", hashtag, "\n"
                        
                        textData = textData.replace ("#" + hashtag, "") #re.sub ("#" + hashtag, "", textData)
                
            #    print "cleaningList Element: ", element, "\n\n"
            
            
            #print "textData AFTER cleaning: ", textData, "\n\n\n"
            
            nonEnglishWordCount = 0
            
            textDataSplit = textData.split (" ")
            
            for word in textDataSplit:
                
                #if child == "@124f4c5e4ace4e6_20170805-165950":
                #    
                #    print "Current word for comparison: ", word, "\n\n"
                
                #word = word.strip ()
                
                if not word.lower () in commonTweetWords and not word.isdigit () and isEnglishWord (word) == False and isEnglishBrown (word) == False and isEnglishChat (word) == False: #and not nltk.corpus.wordnet.synset (word.lower ()) #not word.lower () in nltk.corpus.words.words () and # and not word in nltk.corpus.brown.words ()
                    # and isEnglishReuters (word) == False
                    
                    #textData = textData.replace (word, "")
                    
                    #nonEnglishWordCount += 1
                    
                    if isSpanishWord (word) == True:
                        
                        #print "Found Spanish word: ", word, "\n\n"
                        
                        textData = ""
                        
                        break
                        
                    if isMalayWord (word) == True:
                        
                        print "Found Malay Word: ", word, "\n\n"
                        
                        textData = ""
                        
                        break
                        
                        
                    if not word.lower () in suicideDepressionWords:
                        
                        #print "Found Non English Word: ", word, "\n\n"
                        nonEnglishWordCount += 1
                        
                        if len (textDataSplit) > 0 and ((1.0 * nonEnglishWordCount) / (1.0 * len (textDataSplit))) > .20:
                        
                            textData = ""
                    #if nonEnglishWordCount >= 2 and len (textData) > 3 :
                    #    
                    #    textData = ""
                    #    
                    #    break
                    #    
                    #elif nonEnglishWordCount > 1 and len (textData) <= 3:
                    #    
                    #    textData = ""
                    #    
                    #    break
                    #    
                    ##elif word.lower () not in commonTweetWords:
                    ##    
                    ##    textData = textData.replace (word, "")
                    #    
                    #else:
                    #    
                    #    #textData = textData.replace (word, "")
                    #    if nonEnglishWordCount >= 1:
                    #        
                    #        nonEnglishWordCount -= 1
                        #textData = textData.replace (word, "")
                        
                    #print "textData AFTER looking for NON English words: ", textData, "\n\n"
            
        
        except Exception as e:
            
            raise
            
        
        if currentUsername in usernameResponseDictionary:
            
            usernameResponseDictionary [currentUsername] ["completeResponseFile"].append (textData + "\n\n")
        
            if child in usernameResponseDictionary [currentUsername]:
                
                usernameResponseDictionary [currentUsername] [child].append (textData + "\n\n")
                
            else:
                
                usernameResponseDictionary [currentUsername] [child] = []
                
                usernameResponseDictionary [currentUsername] [child].append (textData + "\n\n")
            
        else:
            
            usernameResponseDictionary [currentUsername] = {}
            
            usernameResponseDictionary [currentUsername] [child] = []
            
            usernameResponseDictionary [currentUsername] [child].append (textData + "\n\n")
            
            
            
            usernameResponseDictionary [currentUsername] ["completeResponseFile"] = []
            
            usernameResponseDictionary [currentUsername] ["completeResponseFile"].append (textData + "\n\n")






def createUpdateSaveDirectories (childResponseDirectory):
    
    updateUserSaveDirectory = os.path.join (newSaveDirectory, childResponseDirectory)
    
    if not os.path.exists (updateUserSaveDirectory):
        
        os.makedirs (os.path.join (newSaveDirectory, childResponseDirectory))
    
    else:
        
        pass
        
        
        





def outputData (username):

    for username in usernameResponseDictionary:
        
        completeDirectory = os.path.join (newSaveDirectory, username)
        
        for child in usernameResponseDictionary [username]:
        
            outfile = child + ".txt"
            
            #print "Just created the OUTFILE name: ", outfile, "\n\n"
            
            completeFile = os.path.join (completeDirectory, outfile)
            
            output = open (completeFile, 'w')
            
            
            for index in usernameResponseDictionary [username] [child]:
                
                output.write (index + "\n\n")
                
            output.close ()
            
    
    usernameResponseDictionary.clear ()
    
    #print "Just output data files for: ", username, "\n\n"





for child in os.listdir (originalSaveDirectory):
    
    childResponseDirectory = os.path.join (originalSaveDirectory, child)
    
    #print "Child Response Directory: ", childResponseDirectory
    
    if os.path.isdir (childResponseDirectory):
        
        #print "Current Child Response Directory contains: ", os.listdir (childResponseDirectory), "\n\n\n"
        
        #if os.path.dirname (childResponseDirectory) == "C:\Users\Username\Desktop\IntentDirectory
            
            #print "Hit @0GGiraffeneck, which has listdir: ", os.listdir (childResponseDirectory)
        
        if os.listdir (childResponseDirectory) == []:
            
            continue
            
        else:
            
            #print "Current childResponseDirectory WITH Files: ", os.path.basename (childResponseDirectory)
            #try:
            #print type (childResponseDirectory)
            createUpdateSaveDirectories (os.path.basename (childResponseDirectory))
            
            
            for child in os.listdir (childResponseDirectory):
                
                currentResponseFileName = os.path.join (childResponseDirectory, child)
                
                #print "Checking to see if current response file name IS A FILE\n\n"
                
                if os.path.isfile (currentResponseFileName):
                    
                    #print "currentResponeFileName", currentResponseFileName
                    
                    if os.path.exists (currentResponseFileName):
                        
                        currentResponseFile = open (currentResponseFileName)
                        #
                        #currentResponseData = currentResponseFile.read ()
                        #
                        for line in currentResponseFile:
                            
                            if re.search ("Response Text:", line):
                                
                                #print "Found RESPONSE TEXT in current line: ", line, "\n\n"
                                #print "hello"
                                extractText (child, line, "Response Text")
                                
                            #elif re.search ("Message Text:", line):
                            #    
                            #    extractText (child, line, "Message Text")
                            
                    else:
                        
                        continue
                
                else:
                    
                    continue
                    
            currentUsername = os.path.basename (childResponseDirectory)
            outputData (currentUsername)
                    
                    #currentUsername = child.split ("2017") [0]
                    #currentUsername = currentUsername [0: len(currentUsername) - 1]
                    #
                    #if currentUsername in usernameResponseDictionary:
                    ##    
                    #    usernameResponseDictionary [currentUsername].append (currentResponseData)
                    ##    
                    #else:
                    ##    
                    #    usernameResponseDictionary [currentUsername] = []
                    ##    
                    #    usernameResponseDictionary [currentUsername].append (currentResponseData)
                        
            #except Exception as e:
                
                #raise









    
    
