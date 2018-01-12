#Import os in order to work with directory information and filenames
import os

#Check the current working directory
os.getcwd ()

#Set the current working directory to be C:\Users\Steve\Desktop\dataScience\CS 498R, which is the directory for this data science project
os.chdir ("Directory Path") #Example for directory path might be like "C:\Users\Username\Desktop\IntentDirectory

#Import glob in order to cycle through each of the files in the CURRENT Filter Set
import glob

#Import re in order to utilize Regular Expressions for automatically filtering out Initial Tweet data ALREADY KNOWN to be unsatisfactory
import re




#Import time for having the script sleep for a brief moment while Direcotries are being created IF they do not yet exist
import time





#Set the True Directory to be the directory that will store All TRUE Suicided related tweets
saveDirectory = os.path.join (os.getcwd (), 'trueSuicideDirectory/31')

#If the Directory that holds data for TRUE Suicide Tweets DOES NOT yet exist, try to create it
if not os.path.exists (saveDirectory):

    try:    
        saveDirectory = os.makedirs (os.path.join (os.getcwd (), 'trueSuicideDirectory/31'))#'C:\Users\Steve\Desktop\dataScience\CS 498R\trueSuicide\*.txt')
        
        print 'Created the SAVE Directory for holding TRUE Suicide related tweets\n\n'
        
        #time.sleep (5)
        
    #If an error occurs when trying to CREATE the Directory that holds TRUE Suicide Tweets, print the error
    except OSError as e:    
        #saveDirectory = os.path.join (os.getcwd (), 'filteredInitialTweet_files')
        print 'Error encountered with establishing True Directory:\t', e.errno, '\n\n'
        
        raise
        

#This is the Dictionarythat will hold the CURRENT CHUNK of TRUE Suicide related tweets for SAVING in the CURRENT Save File
saveTweetList = []


#This will be the Unique ID for the Save File that will contain the CURRENT Chunk of TRUE Suicide related tweets
currentSaveFileID = '5.txt'


#This value will track the number of Tweets that have been identified as TRUE Suicide related and, thus, SAVED in the CURRENT Chunk
saveTweetCount = 0
        
        
        






#Set the True DICTIONARY Directory for storing a file that lists ALL TRUE Suicide related tweets encountered so far
trueDirectory = os.path.join (os.getcwd (), 'trueSuicideDictionary')

if not os.path.exists (trueDirectory):
    
    try:
        trueDirectory = os.makedirs (os.path.join (os.getcwd (), 'trueSuicideDictionary'))
        
        print 'Created the TRUE Suicide DICTIONARY Directory\n\n'
        
        #time.sleep (5)
        
    except OSError as e:
        
        print 'Error encountered with establishing TRUE Suicide DICTIONARY Directory:\t', e.errno, '\n\n'
        
        raise
        
#This is the Dictionary that will hold TRUE Suicide related tweets for comparing
#At the end of filtering a Chunk of Initial Tweet Files, the TRUE Suicide related tweets will be written to a file for futher processing and analysis
#NOTE: I decided to use a LIST to store my TRUE Suicide Dictionary because I can use the 'in' method to search if 'NEW' Tweet Messages already exist in the Dictionary
#trueDictionary = {}
trueDictionaryList = []

trueTweetCount = 1

#If the TRUE Suicide Dictionary Directory is NOT NONE, then, if it's NOT EMPTY, pull out the TRUE Suicide tweets from the dictionary file
if not trueDirectory == None:

    #In order to generate a list of the contents in 'trueDirectory', the pathname must be converted to a STRING (by using os.path.dirname)
    #If the TRUE Suicide Dictionary Directory is NOT EMPTY, then access the file containing the TRUE Suicide related tweets and pull out each TRUE Tweet
    if not os.listdir (os.path.dirname (trueDirectory)) == []:
        
        print 'PUlling out PREVIOUS True Suicide tweet references and establishing CURRENT falseDictionary\n\n'
        
        #After verifying that the TRUE Suicide Dictionary Directory is NOT EMPTY, check if the Dictionary FILE exists
        infile = os.path.join (trueDirectory, 'trueDictionary.txt')
        
        
        #NOTE: I had to perform this 'if os.path.exists' for the file because, although the DIRECTORY exists now, the file may not yet have been created,
        #and if the file has not yet been created, I encountered an IOError (permission denied)
        if os.path.exists (infile):
            
            #if os.path.isfile (file):
            
            #After verifying that the TRUE Sucide Dictionary FILE exists, pull out each TRUE Suicide related tweet and establish the CURRENT True Suicide Dictionary
            trueDictionaryFileIn = open (infile, 'r')
            
            with trueDictionaryFileIn:
                
                for line in trueDictionaryFileIn:
                    
                    if line is '':
                        print 'Encountered EMPTY STRING while establishing current TRUE Suicide Dicitonary\n\n'
                        
                    else:
                        print 'Encountered a TRUE Suicide Dictionary Entry\n\n'
                        
                        print 'TRUE Suicide Dictionary Entry BEFORE replaceing NEWLINE Char:\t', line, '\n\n'
                        
                        #trueDictionary [trueTweetCount] = line
                        
                        
                        #NOTE: Initially, I tried getting rid of NEWLINE Characters using the 'replace' function, but ultimately I just had to
                        #remove them from the LINE by CUTTINT OUT the LAST Character in LINE
                        #line.replace ('\n', '')
                        #trueDictionaryList.append (line)
                        trueDictionaryList.append (line [0: -1])
                        
                        print 'TRUE Suicide Dictionary Entry AFTER replacing NEWLINE Char:\t', line, '\n\n'
                        
                        trueTweetCount += 1
                    
                trueDictionaryFileIn.close ()
                
                
                
            print 'Printing out PREVIOUS True Suicide tweet DICTIONARY after READING IN\n\n'
            
            #for key in trueDictionary:
            for trueTweet in trueDictionaryList:
                
                #print 'CURRENT Prev Key:\t', str (key), '\t\tCURRENT Prev VALUE:\t', trueDictionary [key]
                print 'CURRENT True Tweet:\t', trueTweet
                        
    else:
        print 'Creating the trueDictionary.txt file inside of trueSuicideDictionary Directory\n\n'
        
        trueDictionaryFile = 'trueDictionary.txt'
        
        trueDictionaryFileComplete = os.path.join (trueDirectory, trueDictionaryFile)
        
        trueDictionaryTemp = open (trueDictionaryFileComplete, 'r+')
        trueDictionaryTemp.write ('testing testing 123 true')
        trueDictionaryTemp.close ()

else:
    
    print 'NEWLY created trueSuicideDictionary Directory is NoneType'
    
    pass
        
    
    
    





#Set the False DICTIONARY Directory for storing a file that lists ALL FALSE Suicide related tweets encountered so far
falseDirectory = os.path.join (os.getcwd (), 'falseSuicideDictionary')
#If the Direcotry that holds data for FALSE Suicide Tweets DOES NOT yet exist, try to create it
if not os.path.exists (falseDirectory):
    try:
        falseDirectory = os.makedirs (os.path.join (os.getcwd (), 'falseSuicideDictionary/initial.txt'))#'C:\Users\Steve\Desktop\dataScience\CS 498R\falseSuicide\dictionary.txt')
        
        print 'Created the FALSE Suicide DICTIONARY Directory\n\n'
        
        #time.sleep (5)
        
    #If an error occurs when trying to CREATE the Directory that holds data for FALSE Suicide Tweets, print the error
    except OSError as e:
        
        print 'Error encountered with establishing False Suicide DICTIONARY Directory:\t', e.errno, '\n\n'
        
        raise
        
#This is the Dictionary that will hold ALL FALSE Suicide related tweets encountered
#FIRST: Read in tweets from what has been stored in the FALSE Suicide Directory
#SECOND: Add NEW tweets encountered that are FALSE Suicide related tweets
#LAST: Write out UPDATED Dictionary with ALL UP-TO-DATE FALSE Suicide related tweets encountered
#NOTE: I decided to use a LIST to store my FALSE Suicide Dictionary because I can use the 'in' method to search if 'NEW' Tweet Messages already exist in the Dictionary
#falseDictionary = {}
falseDictionaryList = []

#Read each of the PREVIOUSLY encountered FALSE Suicide related tweets INTO the False Dictionary
falseTweetCount = 1


if not falseDirectory == None:
    
    #In order to generate a list of the contents of 'falseDirectory', the pathname must be converted to a STRING (by using os.path.dirname)
    #If the False Directory is NOT EMPTY, then access the file containing the False Suicide related tweets and pull out each FALSE tweet
    if not os.listdir (os.path.dirname (falseDirectory)) == []:
        
        print 'PUlling out PREVIOUS False Suicide tweet references and establishing CURRENT falseDictionary\n\n'
        
        #After verifying that the FALSE Suicide Dictionary Directory is NOT EMPTY, check if the Dictionary FILE exists
        infile = os.path.join (falseDirectory, 'falseDictionary.txt')
        
        
        #NOTE: I had to perform this 'if os.path.exists' for the file because, although the DIRECTORY exists now, the file may not yet have been created,
        #and if the file has not yet been created, I encountered an IOError (permission denied)
        if os.path.exists (infile):
            
            print 'In the FALSE Dictionary Directory... trying to access PREVIOUS False Tweet Data\n\n'
            
            #if os.path.isfile (file):
            
            #After verifying that the FALSE Suicide Dictionary FILE exists, pull out each FALSE Suicide related tweet and establish the CURRENT False Suicide Dictionary
            falseDictionaryFileIn = open (infile,'r')
            
            print 'Verified that file IS a file\n\n'
            
            with falseDictionaryFileIn:
                
                print 'OPENED the CURRENT Previous FALSE Dictionary File\n\n'
                
                for line in falseDictionaryFileIn:
                    
                    print 'Adding new data to the current FALSE Filtering Dictionary\n\n'
                    
                    #falseDictionary [falseTweetCount] = line
                    
                    #NOTE: Initially, I tried getting rid of NEWLINE Characters using the 'replace' function, but ultimately I just had to
                    #remove them from the LINE by CUTTINT OUT the LAST Character in LINE  
                    falseDictionaryList.append (line [0: -1])
                    
                    falseTweetCount += 1
                    
                falseDictionaryFileIn.close ()
                
            print 'Printing out PREVIOUS False Dictionary after READGING IN\n\n'
            
            #for key in falseDictionary:
            for falseTweet in falseDictionaryList:
                
                #print 'CURRENT Prev Key:\t', str (key), '\t\tCURRENT Prev VALUE:\t', falseDictionary [key]
                print 'CURRENT FALSE Tweet:\t', falseTweet
    else:
       print 'Creating the falseDictionary.txt file inside of falseSuicideDictionary Directory\n\n'
       
       falseDictionaryFileComplete = os.path.join (falseDirectory, 'falseDictionary.txt')
       
       falseDictionaryTemp = open (falseDictionaryFileComplete, 'w+')
       #falseDictionaryTemp.write ('testing testing 123 false')
       falseDictionaryTemp.close ()
        
         

else:
    print 'NEWLY created falseSuicideDictionary Directory is NoneType'
    
    pass





#Set the Base Directory to be the directory that contains the ALL sets of tweet files to be filtered
baseDirectory = os.path.join (os.getcwd (), 'initialTweet_files')



#Set the CURRENT Filter Set to be the BASE DIRECTORY that is then JOINED to the directory that contains the CURRENT set of tweet files to be filtered

#This is currently associated with FOLDER 1 from Folder 31 inside InitialTweet_files
startFilterIndex = 5 #This is the Index of the folder that contains the FIRST set of tweet files to be filtered
endFilterIndex = 5 #This is the Index of the folder that contains the LAST set of tweet files to be filtered
currentFilterIndex = startFilterIndex #Set the current Filter Index to be the START Index in the CURRENT set of Directories for filtering





#Start cycling through Initial Tweet Container Folders from the indicated START INDEX through END INDEX
while currentFilterIndex < endFilterIndex + 1:
    
    #Update the Folder that contains the CURRENT Filter Set
    currentFilterSet = os.path.join (baseDirectory, str(currentFilterIndex) + '\*.txt')
    
    print 'Current Filter Set: ', str (currentFilterSet), '\n\n'
    
    #Access the Initial Tweet data contained in each file in the CURRENT DIRECTORY
    for file in glob.glob (currentFilterSet):
        
        #Indicate CURRENT Initial Tweet file
        currentFileName = os.path.basename (file)
        
        print '\n\n\nCurrent Work being done in file:\t', currentFileName, '\n\n\n'
        
        

        #Open the CURRENT Initial Tweet file in the CURRENT Directory, to access the Tweet data
        with open (file) as infile:
            

            #Look at each LINE in the CURRENT Initial Tweet file
            for line in infile:
                
                
                #If the CURRENT LINE begins with '@' then it is the START of a NEW Initial Tweet
                if re.match ('^@', line):
                    
                    
                    #The CURRENT Initial Tweet DATA begins AFTER '|' (everything before '|' is the Username and Timestamp
                    currentTweetData = line [line.find ('|') + 1: ]
                    
                else:
                    
                    continue
                    
                    
                #The ACTUAL Tweet MESSAGE is labeled with 'Message Text' and followed by 'Message User'
                #The Tweet Message begins AFTER '\t\t\tMessage Text:',
                #so to establish the CORRECT Index for the Start of the CURRENT Tweet Message,
                #FIND the FIRST occurrence of '\t\t\tMessage Text:' and then ADD the LENGTH of '\t\t\tMessage Text:' to that value to establish the STARTING Index of the CURRENT Tweet Message
                currentTweetText = currentTweetData [currentTweetData.find ('\t\t\tMessage Text:') : currentTweetData.find ('\t\t\tMessage User:')]
                #+ len ('\t\t\tMessage Text:')
                
                print '\n\t\tCurrent Filter Tweet Text:\t', currentTweetText
                
                
                #Set up a 
                
                
                #Initially, Regular Expressions were going to be utilized for the filtering process, but because there are an infinite number of possible text combinations,
                #I figured a more efficient approach was builiding DICTIONARIES to hold text already identified as "True Suicide" or "False Suicide"
                #currentTextSearchGUN =  re.search ('\s*(\w*\d*\S*)*\s*(@\w*\d*\S*)*\s*(:\w*\d*\S*)*gun\s*(\w*\d*\S*)*', currentTweetText) # re.search ('RT\s(@\w*\d*\S*)*:', currentTweetText) #
                #re.search ('(\w*\d*)*\s*feel\s*(\w*\d*)*\s*empty', currentTweetText.decode ('ascii', 'ignore'))#, currentTweetText).groups ()#re.match ('[A-Za-z0-9]*\bempty\s(without|house|home|bed|bowl|plate|container|stomach)', currentTweetText):
                
                #if currentTextSearchGUN.group () is not None:
                #    
                #    print '\n\nFound GUN in Current Tweet Text:\t', '\n\n\n'
                #    
                #else:
                #    
                #    print '\n\nDid NOT find GUN in Current Tweet Text:\t', '\n\n\n'
                #    
                #    pass
                    
                #else:
                #    
                #    print '\n\n\tNo REGEX Recognition in Current Tweet Text'
                
                #If the CURRENT Tweet Text is ALREADY in the TRUE Suicide Dictionary, then move to the next Tweet
                
                
                
                
                
                #Try to filter the CURRENT Tweet by omparing the CURRENT Tweet Text against Messages stored in the TRUE Suicide Dictionary AND the FALSE Suicide Dictionary
                if currentTweetText in trueDictionaryList:
                    
                    #print 'Found the CURRENT Tweet Text (', currentTweetText, ') in the TRUE Dictionary LIST\n\n\n'
                    
                    #If the CURRENT Tweet Text is ALREADY in the TRUE Suicide Dictionary, add the CURRENT TWEET to the list of Tweets for saving
                    saveTweetList.append (line)
                    
                    saveTweetCount += 1
                    
                    continue
                        
                #If the CURRENT Tweet Text is ALREADY in the FALSE Suicide Dictionary, then move to the next Tweet
                elif currentTweetText in falseDictionaryList:
                    
                    #print 'Found the CURRENT Tweet Text (', currentTweetText, ') in the FALSE Dictionary LIST\n\n\n'
                    
                    continue
                        
                
                
                #Otherwise, if the CURRENT Tweet Text IS NOT YET in either the TRUE or FALSE Suicide Dictionary,
                #continue processing to determine if the CURRENT Tweet is TRUE Suicide related or FALSE Suicide related and add it to the appropriate dictionary
                else:
                    userTextAssessment = raw_input ('\nIs the above Tweet Text related to suicide? Enter y or n')
                    
                    print 'User Text Assessment (Is the tweet related to suicide?): ', userTextAssessment
                    
                    
                    #This was used for testing whether the DICTIONARY Files were being PROPERLY RECREATED following each filter cycle OR if the FILES were simply being ADDED TO
                    if userTextAssessment.lower () == 'p':
                        
                        continue
                    
                    #If the CURRENT Tweet Text is identified as TRUE Suicide, add it to the TRUE Suicide Dictionary
                    elif userTextAssessment.lower () == 'y':
                        
                        #trueDictionary [trueTweetCount] = currentTweetText
                        trueDictionaryList.append (currentTweetText)
                        
                        #If the User identified the CURRENT TWEET as TRUE Suicide related, then ADD the CURRENT TWEET to the list of Tweets for saving
                        saveTweetList.append (line)
                        
                        saveTweetCount += 1
                        
                        trueTweetCount += 1
                        
                    #If The CURRENT Tweet Text is identified as FALSE Suicide, add it to the FALSE Suicide Dictionary
                    elif userTextAssessment.lower () == 'n':
                        
                        #falseDictionary [falseTweetCount] = currentTweetText
                        falseDictionaryList.append (currentTweetText)
                        
                        falseTweetCount += 1
                        
                    else:
                        
                        continue
    
    
    
    currentFilterIndex += 1
    
    
    
    
print 'Printing out the key-value pairs for FALSE Suicide related tweets\n\n'

try:
    #falseDictionaryFile = 'falseDictionary.txt'
    #Remove the PREVIOUS FALSE Suicide Dictionary so that the UPDATED FALSE Suicide Dictionary can be saved (preventing DUPLICATE False Suicide Tweets)
    falseDictionaryFileComplete = os.path.join (falseDirectory, 'falseDictionary.txt')
    
    if os.path.exists (falseDictionaryFileComplete): 
        
        os.remove (falseDictionaryFileComplete)
    
    #Reconstruct the False Suicide Dictionary FILE to save the False Suicide Dictionary        
    falseDictionaryFileComplete = os.path.join (falseDirectory, 'falseDictionary.txt')
    
    #Open the RECONSTRUCTED False Suicide Dictionary FILE for saving the False Suicide Dictionary
    falseDictionaryTemp = open (falseDictionaryFileComplete, 'w+')
    
    #Save each False Suicide Tweet in the RECONSTRUCTED False Suicide Dictionary FILE
    for tweetMessage in falseDictionaryList:
        
        print '\tCurrent FALSE Tweet Message: ', tweetMessage#str (key),'\t\tCurrent Value: ', falseDictionary [key]
        
        falseDictionaryTemp.write (tweetMessage + '\n')#falseDictionary [key] + '\n')
 
    #After all of the False Suicide Tweets has been saved into the RECONSTRUCTED False Suicide Dictionary FILE, close the file   
    falseDictionaryTemp.close ()
    
except Exception as e:
    
    raise
    


print '\n\n\n\nPrinting out the key-value pairs for TRUE Suicide related tweets'

try:
    #trueDictionaryFile = 'trueDictionary.txt'
    #Remove the PREVIOUS TRUE Suicide Dictionary so that the UPDATED TRUE Suicide Dictionary can be saved (preventing DUPLICATE True Suicide Tweets)
    trueDictionaryFileComplete = os.path.join (trueDirectory, 'trueDictionary.txt')
    
    if os.path.exists (trueDictionaryFileComplete):
    
        os.remove (trueDictionaryFileComplete)
    
    #Reconstruct the TRUE Suicide Dictionary FILE to save the UPDATED True Suicide Dictionary
    trueDictionaryFileComplete = os.path.join (trueDirectory, 'trueDictionary.txt')
    
    #Open the RECONSTRUCTED True Suicide Dictionary FILE for saving the True Suicide Dictionary
    trueDictionaryTemp = open (trueDictionaryFileComplete, 'w+')

    #Save each True Suicide Tweet in the RECONSTRUCTED True Suicide Dictionary FILE
    for tweetMessage in trueDictionaryList:
        
        print '\tCurrent TRUE Tweet Message: ', tweetMessage#str (key), '\t\tCurrent Value: ', trueDictionary [key]
        
        trueDictionaryTemp.write (tweetMessage + '\n')#trueDictionary [key] + '\n')
    
    #After all of the True Suicide Tweets have been saved to the RECONSTRUCTED True Suicide Dictionary FILE, close the file
    trueDictionaryTemp.close ()
    
except Exception as e:
    
    raise
    
    
    
    
    
    

try:
    
    #Construct the CURRENT Save File that will contain the current chunk of True Suicide Tweets
    #Note that 'saveDirectory' and 'currentSaveFileID' are defined at the beginning of this script
    saveFileComplete = os.path.join (saveDirectory, currentSaveFileID)
    
    saveFileTemp = open (saveFileComplete, 'w+')
    
    for tweet in saveTweetList:
        
        saveFileTemp.write (tweet + '\n\n')
        
    saveFileTemp.close ()
    
except Exception as e:
    
    raise
    
    
    
    
    
    
print '\n\n\n\n\nTotal Number of TRUE Suicide Tweets saved FROM the CURRENT Chunk: \t\t', saveTweetCount
