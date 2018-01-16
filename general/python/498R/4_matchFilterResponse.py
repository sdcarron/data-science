#Check the current working directory
import os

print os.getcwd ()

#Set the current working directory as desired
os.chdir ("Directory Path") #Example for directory path might be like "C:\Users\Username\Desktop\IntentDirectory

#Verify that current working directory is updated as desired
print os.getcwd ()



#Used for accessing items within a directory
import glob

#Used for matching a Username from the Initial Tweet File (Username indicated by Line starting with '@')
import re

#Used for copying Response files that will be kept
import shutil

#Used for pausing between CREATING Response SAVE Directories and trying to Copy Files INTO Save Directories
import time




#Set the directories needed for mathing each Initial Suicide Tweet with Responses


#Establish the access path for Initial Tweet Files
initialTweetIndex = 21
initialTweetPath = os.path.join (os.getcwd (), "trueSuicideDirectory")
initialTweetDirectory = os.path.join (initialTweetPath, str (initialTweetIndex))

print "Initial Tweet Directory: ", initialTweetDirectory

#Establish the access path for Response Tweet Files
responseTweetIndex = 1
responseTweetPath = os.path.join (os.getcwd (), "responseTweet_Files")
responseTweetDirectory = os.path.join (responseTweetPath, str (responseTweetIndex))

print "Response Tweet Directory: ", responseTweetDirectory

#Establish the path for SAVED Response Tweet Directories (And Associated Files)
savePath = os.path.join (os.getcwd (), "responseSaveDirectory")

#Used for TESTING that INITIAL Tweet File Usernames can be matched with RESPONSE Tweet File Usernames
testTweetDirectory = os.path.join (os.getcwd (), "testSuicideDirectory")


#Verify that the directories for matching Initial Tweet with Responses have been set as desired
print "Initial Tweet Directory: ", initialTweetDirectory, "\n\n\n", "Response Tweet Direcotry: ", responseTweetDirectory




#Begin the process of accessing Initial Tweet Data
currentInitialTweetFileSet = os.path.join (initialTweetDirectory, "*.txt")
currentTestTweetFileSet = os.path.join (testTweetDirectory, "*.txt")



currentInitialUsername = ""



def extractInitialUsername (line):
    
    if re.match ('@', line):
                
        #        print "Found username: ", line.split (">") [0]
        #    
        currentInitialUsername = line.split (">") [0]
        
        return currentInitialUsername
    
    else:
        
        return ""
                


#Look for the Target User (intended recipient of the RESPONSE data) for the Current Response Tweet File
def matchInitialUsername (currentInitialTweetFile, currentResponseTweetFile):
    
    print "Current Response Tweet File FULL NAME: ", currentResponseTweetFile, "\n\n"
    
    #Parse through the File Name for the Current Response Tweet File in order to extract the Target
    currentResponseFileName = os.path.basename (currentResponseTweetFile)
    
    print "\n\n\nCurrent Response File: ", currentResponseFileName, "\n\n\n"
    
    currentResponseFileNameSplit = currentResponseFileName.split ("2017")
    
    print "\n\n\nCurrent Response File Name Split: ", currentResponseFileNameSplit
    
    currentResponseTarget = currentResponseFileNameSplit [0]
    
    print "\n\n\nCurrent Response Target: ", currentResponseTarget
    
    #Remove the LAST character in the Current Response Target Username
    currentResponseTarget = currentResponseTarget [0:len (currentResponseTarget) - 1]
    
    print "\n\n\nCurrent Response Target: ", currentResponseTarget
    
    #Compare the Target User from the Current Response Tweet File to the
    
    with open (currentInitialTweetFile) as initialFile_in:
        
        print "Opened Current Initial Tweet File\n\n"
        
        for line in initialFile_in:
            #
            currentInitialUsername = extractInitialUsername (line)
            
            if currentInitialUsername != "":
                
        #        print "Found username: ", line.split (">") [0]
        #    
        #       currentInitialPoster = line.split (">") [0]
        #        print "Current Initial Poster: ", currentInitialPoster
        #        
                if currentInitialUsername == currentResponseTarget:
        #            
                    print "Current Initial Poster: ", currentInitialUsername, "\t\t\tCurrent Response Target: ", currentResponseTarget
                    
                    saveDirectory = os.path.join (savePath, currentResponseTarget)
                    print "Save Directory: ", saveDirectory, "\n\n"
                    
                    if not os.path.exists (saveDirectory):
                        
                        print "Save Directory does NOT YET exist\n\n"
                        
                        saveDirectory = os.makedirs (os.path.join (savePath, currentResponseTarget))
                        
                        print "Save Directory: ", saveDirectory, "\n\n"
                        
                    #Save the Current RESPONSE File in the SAVE Directory NAMED AFTER the CURRENT Response Target/Current Initial Poster
                    time.sleep (5)
                    shutil.copy2 (currentResponseTweetFile, saveDirectory)
                    
                                       
                                                          
 
def createSaveDirectories (currentInitialFile):
    
   with open (currentInitialFile) as initialFile_In:
       
      for line in initialFile_In:
                    
             
        currentInitialUsername = extractInitialUsername (line)
         
        if currentInitialUsername != "":
            
         
            saveDirectory = os.path.join (savePath, currentInitialUsername)
            
            print "Save Directory: ", saveDirectory, "\n\n"
            
            if not os.path.exists (saveDirectory):
                
                print "Save Directory does NOT YET exist\n\n"
                
                saveDirectory = os.makedirs (os.path.join (savePath, currentInitialUsername))
                
                print "Save Directory: ", saveDirectory, "\n\n"
        
        else:
            
            continue
            
            
for initialFile in glob.glob (currentInitialTweetFileSet):
    
    #Create Save Directories FIRST
    createSaveDirectories (initialFile)
    
    #currentFileName = os.path.basename (file)
    
    #print "os.listdir(responseTweetDirectory): ", os.listdir (responseTweetDirectory)
    
    for child in os.listdir (responseTweetDirectory):
        
        responseFileDirectory = os.path.join (responseTweetDirectory, child)
        
    #    print "Current Respone Tweet Directory CHILD directory test: ", directoryTest
        
        if os.path.isdir (responseFileDirectory):
            
    #        print "Current Response Tweet CHILD IS a directory\n\n"
            
    #        print "Processing RESPONSE Files located in: ", os.path.dirname (directoryTest), "\n\n\n"
    #        
    #        print "Current Response Tweet Directory CHILD: ", child
    #        
    #        print "Current CHILD TYPE: ", type (child)
    #        
            for child in os.listdir (responseFileDirectory):
                
                responseFile = os.path.join (responseFileDirectory, child)
    #            print "Current response file: ", responseFile, "\n\n\n"
                
    #            print "Current initial file: ", initialFile
                if responseFile != None and os.path.exists (responseFile) and initialFile != None and os.path.exists (initialFile):
                    
                    try:
                        matchInitialUsername (initialFile, responseFile)#, responseFileDirectory)
                        
                    except Exception as e:
                        
                        continue
    #            
        else:
            
            responseFile = os.path.join (responseTweetDirectory, child)
            
            matchInitialUsername (initialFile, responseFile)
    
    
