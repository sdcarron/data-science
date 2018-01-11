#Use os library to work with files and filepaths
import os

#Check current directory
os.getcwd ()

#Set working directory to desired path
os.chdir ("Directory Path") #Example for directory path might be like "C:\Users\Username\Desktop\IntentDirectory

#Set the input directory (this directory holds the files generated by SP.py using the Twitter Stream API)
#These files represent the INITIAL tweets obtained when searching for suicide related terms/phrases
baseDirectory = os.path.join (os.getcwd (), "initialTweet_files/")

#Set the output directory (this directory holds the files generated by responseTweet.py using the Twitter Search API)
#These files represent the RESPONSE tweets obtained when searching for tweets to the Users who posted the INITIAL suicide related tweets
saveDirectory = os.path.join (os.getcwd (), "responseTweet_files")




#Use glob for reading in files from the input directory (initialTweet_files)
import glob

#Use re for identifying if a line begins with User name ('@.....')
import re

#I didn't end up using these in the final process. They can be used, for tracking total number of initial posts and
#total number of responses OR number of responses PER initial post
initialTweetCount = 0
responseTweetCount = 0

#This data structure holds each User name that posted an INITIAL tweet (from initialTweet_files) that is associated with suicide
initialNames = {}


#Set Index "i" to match the FIRST initial tweets container folder
i = 3 #This is folder 3 inside folder 35 from initialTweet_files Folder

#Loop through each of the initial tweets container folders sequentially
while i < 4:

    #Set the currentSubmitDirectory to be the next folder containing the next set of Initial Tweet files
    currentSubmitDirectory = os.path.join (baseDirectory, str (i) + "/*.txt")
    
    #Verify that the script is cycling through the Initial tweet CONTAINER folders properly
    #print os.path.basename (currentSubmitDirectory)

    #Read in each file from the input directory (initialTweet_files)
    for file in glob.glob (currentSubmitDirectory):
        
        #Obtain the current file's name and then print the name to verify that each intended file is being accessed
        currentFileName = os.path.basename (file)
        
        #Verify that the correct file is being used
        #print currentFileName
        
        #Read in each file's data and identify the User name that POSTED each INITIAL tweet
        with open (file) as file_in:
            
            #Obtain the text from the current input file and then print the text to verify that the text and file match
            #currentText = file_in.read ()
            #print currentText
            
            for line in file_in:
                
                #If the current line begins with an @, then the current line begins with a User name
                if re.match ('^@', line):
    
                    initialTweetCount += 1
    
                    #Print the current line to compare it to the appropriate initialTweet_files file
                    #print line
                    
                    #Extract the Username AND Date of the Tweet at the beginning of CURRENT Line from the CURRENT File in CURRENT Folder in "initialTweet_files"
                    currentUser_currentDate = line [0:line.find ('|')]
                    
                    #Extract the data associated with the CURRENT Initial Tweet
                    currentTweetData = line [line.find ('|') + 1:]
                    
                    #Split the Username and Date that are associated with the current tweet
                    currentUser_currentDate_split = currentUser_currentDate.split ('>')#.split ('\\')
                    
                    #The current Username is a combination of the Twitter User account name AND the time at which the Tweet was pulled from Twitter and pushed into
                    #the data file inside "initialTweet_files"
                    
                    #print "Current User/Date combination Split: ", currentUser_currentDate_split, '\n\n'
                    
                    #print "Current Tweet Data: ", currentTweetData, "\n\n\n\n"
                    
                    currentUser = currentUser_currentDate_split [0]#.split ('>') [0]
                    
                    if len (currentUser_currentDate_split) == 2:
                    
                        currentDate = currentUser_currentDate_split [1].split ('-') [0]
                        
                        currentYear = currentDate [0:4]
                        currentMonth = currentDate [4:6]
                        currentDay = currentDate [6:]
                        
                        currentDate_List = [currentYear, currentMonth, currentDay]
                    
                    
                    
                    #Add the UNIQUE User name (which is attached to the time at which the User name was obtained in SP.py) as a Key and the Date of the tweet as the VALUE
                    #We need both the User name (WITHOUT the time at which it was obtained in SP.py) and the Tweet Date in order to correctly run Search API
                    if currentUser in initialNames:
                        
                        #initialNames [currentUser] = ['']
                        if currentDate_List not in initialNames [currentUser]:
                            
                            initialNames [currentUser].append ((currentDate_List, currentTweetData))
                        
                    else:
                        
                        initialNames [currentUser] = []
                        
                        initialNames [currentUser].append ((currentDate_List, currentTweetData))
                    
                    
                    #Print the User name at the beginning of the current line to verify that it matches correctly with the current file from initialTweet_files
                    #print '\n\nLine began with Username: ', currentUser, '\n\n'
                    
                    
                else:
                    
                    print '\n\nLine did NOT begin with a User name: ', line, '\n\n'
                
            
    #Increment "i" in order to reference the next folder containing the next set of Initial Tweet files
    i += 1
                



#Verify that the expected number of Initial tweets have been read in                
#print 'Initial Tweet Count: ', initialTweetCount, '\n\n\n'

#Verify that the Initial tweet data has been properly restructured for feeding to the Search API call
#for name in initialNames:
#    
#    print "Current Initial Tweet User:", name, "\n"
#    
#    print "Current Initial Tweet Date List: ", initialNames [name][0][0], "\n"
#    
#    print "Current Initial Tweet Data: ", initialNames [name][0][1], "\n\n\n"
               

#Include this call to sys.exit () in order to terminate after running the process of importing each of the Initial Tweet files to verify that the import process
#is working properly                              
#import sys                                        
#sys.exit ()               
                
#Use tweepy to obtain data through Twitter Search API
import tweepy

#Use json to encode the Response tweets from the Search API
import json

#These are my Twitter API credentials. These match the same credentials used in the STREAM process in "1_SP.py", and
#can be obtained through Twitter's Developer Account options at Twitter.com
cKey = "SSSSSSSSSSSSSSSSSSSSSSSSS"
cSecret = "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
aToken = "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
aSecret = "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"


#Construct the Twitter Search (REST) API object
#Use the AppAuthHandler tool in order to optimize the REST Search API query process
auth = tweepy.AppAuthHandler (cKey, cSecret)
#auth.set_access_token (aToken, aSecret)

responseSearch = tweepy.API (auth, wait_on_rate_limit=True)

#Use time to create UNIQUE output file names
import time

counter = 0

#This dictionary is to help convert the MONTH of DATE to proper format of the Tweet (for which we need responses)
month = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08', 'sep':'09', 'oct':'10', 'nov':'11', 'dec':'12'}

#Cycle through each Initial Tweet Username KEY
for name in initialNames:
    
    try:
        #The beginning of each file name matches the Initial Tweet Username KEY
        fprefix = name
            
        #Concatenate the CURRENT Initial Tweet Username with the CURRENT Timestamp to make the CURRENT Response Tweet filename UNIQUE
        outFile = fprefix + '_' + time.strftime ('%Y%m%d-%H%M%S') + '.txt'
            
        #Set the Directory for the CURRENT Response Tweet file        
        completeFile = os.path.join (saveDirectory, outFile)
        
        #Open the CURRENT Response Tweet file for writing the output
        output = open (completeFile, 'w')
        
    except Exception:
        
         print ('Could not open file for Username: ', name)
         
         continue
    
    
    
    
    #print 'Username: ', name, '\t\t', 'Date: ', initialNames [name][0][0], '\n'
    
    searchName = name#.split ('>') [0]
    
    for pair in initialNames [name]:
    
        #nameDate = initialNames [name] [0].split (' ')
        #
        #print nameDate
        ##print type (nameDate)
        #dateMonth = month [nameDate [1].lower ()]
        #dateDay = nameDate [2]
        #dateYear = nameDate [5]
        
        #print '\nCurrent Date: ', date
        
        #currentDate = date.split (' ')
        currentDate = pair [0]
        
        
        dateYear = int (currentDate [0])
        dateMonth = currentDate [1]#.lower ()]
        dateDay = currentDate [2]
        
        
        currentTweetData = pair [1]
        
        #Display the Date AND Data from the CURRENT Initial Tweet at the TOP of the CURRENT output file
        output.write ("Initial Tweet Date: " + dateDay + "-" + dateMonth + "-" + str (dateYear) + "\n\n" + currentTweetData + "\n\n\n\n")
        
        
        
        
        #print 'Month: ', dateMonth, '\tDay: ', dateDay, '\tYear: ', dateYear, '\n\n'
        
        
        response = tweepy.Cursor(responseSearch.search,q=searchName, since=str (dateYear) + '-' + str (dateMonth) + '-' + str (dateDay), until=str (dateYear) + '-' + str (dateMonth) + '-' + str (int (dateDay) + 2)).items ()#since='2017-06-22',until='2017-06-23').items()
        
        
        #response = responseSearch.search (searchName + 'since:2017-6-21' + 'until:2017-6-23')#'@Sethrogen' + 'since:2017-6-21' + 'until:2017-6-23')
        
        
        
        
        for r in response:
            
            decoded = r._json#json.loads (r)
            
            #print 'Current File Name: ', completeFile, '\n\n'
            
            #print '\n\n', s.text, '\n\n'
            
            responseTweetCount += 1
            
            #output.write (r.screen_name) #output.write (r.text.encode ('ascii', 'ignore') + "\n\n\n")
            #output.write ("\n\n\n")
            
            
            
            
            
            
            
            
            
            #print "Current Response decoded: ", decoded, "\n\n\n\n"
            
            
            
            
            
            
            
            
            currentOutputLine = '\n\n\n\n\t\t@' + decoded['user']['screen_name'] + '>' + time.strftime ('%Y%m%d-%H%M%S') + '|'
                
            currentOutputLine += '\t\t\tMessage ReplyScreenNameTarget: '
            
            if decoded['in_reply_to_screen_name'] is not None:
                
                currentOutputLine += decoded['in_reply_to_screen_name']
                
            else:
                
                currentOutputLine += 'NULL'
                
            
            
            currentOutputLine += '\t\t\tResponse ReplyUserIDTarget: '
            
            if decoded['in_reply_to_user_id_str'] is not None:
                
                currentOutputLine += decoded['in_reply_to_user_id_str']
                
            else:
                
                currentOutputLine += 'NULL'
                
                
                
            currentOutputLine += '\t\t\tResponse ReplyStatusIDTarget: '
            
            if decoded['in_reply_to_status_id_str'] is not None:
                
                currentOutputLine += decoded['in_reply_to_status_id_str']
                
            else:
                
                currentOutputLine += 'NULL'
                
            
            
            currentOutputLine += '\t\t\tResponse QuotedStatusIDStr: '
            
            #if decoded['quoted_status_id_str'] is not None:
                
            #    currentOutputLine += decoded['quoted_status_id_str']
                
            #else:
                
            currentOutputLine += 'NULL'
                
                
            
            currentOutputLine += '\t\t\tResponse ScopeFollowers: '
            
            #if decoded['scopes']['followers'] is not None:
                
            #    currentOutputLine += str (decoded['scopes']['followers'])
                
            #else:
                    
            currentOutputLine += 'NULL'
                
            
            
            
            currentOutputLine += '\t\t\tResponse RetweetCount: '
            
            if decoded['retweet_count'] is not None:
                
                currentOutputLine += str (decoded['retweet_count'])
                
            else:
                
                currentOutputLine += 'NULL'
                
                
            
            
            currentOutputLine += '\t\t\tResponse Time: '
            
            if decoded['created_at'] is not None:
                
                currentOutputLine += decoded['created_at']
                
            else:
                
                currentOutputLine += 'NULL'
            
            
            
            
            #if decoded['coordinates'] is not None:
            #
            #    currentOutputLine += '\t\t\tResponse Coordinates (Longitude,Latitude): ' + str (decoded ['coordinates'][0]) + ', ' + str (decoded['coordinates'][1])
            #
            #else:
                
            currentOutputLine += '\t\t\tResponse Coordinates (Longitude,Latitude): ' + 'NULL, NULL'
            
            
            
            
            if decoded['place'] is not None:
                
                currentOutputLine += '\t\t\tResponse Location (Locale, Country): ' + decoded['place']['full_name'] + ', ' + decoded['place']['country']
                
            else:
                
                currentOutputLine += '\t\t\tResponse Location (Locale, Country): ' + 'NULL, NULL'
                
                
            
            
            currentOutputLine += '\t\t\tResponse FavCount: '
            
            if decoded['favorite_count'] is not None:

                currentOutputLine +=  str (decoded['favorite_count'])
            
            else:
                
                currentOutputLine += 'NULL'
                
                
                
            currentOutputLine += '\t\t\tResponse FavBool: '
            
            if decoded['favorited'] is not None:
                
                currentOutputLine += str (decoded['favorited'])
                
            else:
                
                currentOutputLine += 'NULL'
            
            
            
            
            currentOutputLine += '\t\t\tResponse FilterLevel: '
            
            #if decoded['filter_level'] is not None:
            #    
            #    currentOutputLine += decoded['filter_level']
            #    
            #else:
                
            currentOutputLine += 'NULL'
            
            
            
            
            currentOutputLine += '\t\t\tResponse HashTags: '
            
            if decoded['entities']['hashtags'] is not None:
                
                for hashtag in decoded['entities']['hashtags']:
                
                    currentOutputLine += '\t' + 'Hashtag: #' + hashtag ['text']
                    
                    
            else:
                
                currentOutputLine += 'NULL'
                
                
                
            currentOutputLine += '\t\t\tResponse URLs: '
            
            #if decoded['entities']['urls'] is not None:
            #    
            #    for url in decoded['entities']['urls']:
            #        
            #        if url is not None:
            #    
            #            currentOutputLine += '\t' + 'URL: ' + url['expanded_url']
            #            
            #        else:
            #            
            #            currentOutputLine += '\t' + 'URL: NULL'
            #    
            #else:
                
            currentOutputLine += 'NULL'
                
                
                
            currentOutputLine += '\t\t\tResponse Mentions: '
            
            if decoded['entities']['user_mentions'] is not None:
                
                for mention in decoded['entities']['user_mentions']:
                
                    currentOutputLine += '\t' + 'Screen Name: ' + mention['screen_name'] + ' ' + 'User ID Str: '+ mention['id_str']
            
            else:
                
                currentOutputLine += 'NULL'
            
            
            
            currentOutputLine += '\t\t\tResponse Text: ' + decoded['text'].encode('ascii', 'ignore')
            
            
            
            
            
            
            #'user' -> (X'created_at', X'default_profile', X'default_profile_image', X'description', X'favourites_count', X'followers_count', X'friends_count', X'id_str', X'listed_count', X'name', X'screen_name', X'statuses_count')
            currentOutputLine += '\t\t\tResponse User: '
            
            
            
            
            currentOutputLine += '\tName {' 
            
            if decoded['user']['name'] is not None:
                
                currentOutputLine += decoded['user']['name'].encode('ascii', 'ignore') + '}'
            
            else:
                
                currentOutputLine += 'NULL}'
            
            
            
            
            currentOutputLine += '\tScreen Name {'
            
            if decoded['user']['screen_name'] is not None:
                
                currentOutputLine += decoded['user']['screen_name'].encode('ascii', 'ignore') + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
            
            
            
            currentOutputLine += '\tID str {'
            
            if decoded['user']['id_str'] is not None:
                
                currentOutputLine += decoded['user']['id_str'] + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
            
            
            
            
            currentOutputLine += '\tDescription {'
            
            if decoded['user']['description'] is not None:
                
                currentOutputLine += decoded['user']['description'].encode('ascii', 'ignore') + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
                
                
                
            currentOutputLine += '\tHas Default Profile {'
            
            if decoded['user']['default_profile'] is not None:
                
                currentOutputLine += str (decoded['user']['default_profile']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
            
            
            
            currentOutputLine += '\tHas Default Image {'
            
            if decoded['user']['default_profile_image'] is not None:
                
                currentOutputLine += str (decoded['user']['default_profile_image']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
                
                
                
            currentOutputLine += '\tStatus Count {'
            
            if decoded['user']['statuses_count'] is not None:
                
                currentOutputLine += str (decoded['user']['statuses_count']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
            
            
            
            currentOutputLine += '\tFavourites Count {'
            
            if decoded['user']['favourites_count'] is not None:
                
                currentOutputLine += str (decoded['user']['favourites_count']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
                
            
            
            currentOutputLine += '\tFriends Count {'
            
            if decoded['user']['friends_count'] is not None:
                
                currentOutputLine += str (decoded['user']['friends_count']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
                
                
                
            currentOutputLine += '\tFollowers Count {'
            
            if decoded['user']['followers_count'] is not None:
                
                currentOutputLine += str (decoded['user']['followers_count']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
                
                
                
            currentOutputLine += '\tListed Count {'
            
            if decoded['user']['listed_count'] is not None:
                
                currentOutputLine += str (decoded['user']['listed_count']) + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
                
                
                
                
            currentOutputLine += '\tTime Created: {'
            
            if decoded['user']['created_at'] is not None:
                
                currentOutputLine += decoded['user']['created_at'] + '}'
                
            else:
                
                currentOutputLine += 'NULL}'
            
            
            
            
            
            
            
            
            
            
            
            #output.write ("\t\tResponse Screen Name: " + "@" + decoded['user']['screen_name'] + "\t\tResponse Time: " + decoded['created_at'] + "\t\tResponse Text: " + decoded['text'].encode ('ascii', 'ignore') + '\n\n\n')
            #
            
            output.write (currentOutputLine.encode('ascii', 'ignore') + '\n')
            
            counter += 1
            
            if counter >= 100:
                
                counter = 0
                
                #print 'Counter EXCEEDED 10', '\n\n\n'
                
                output.close ()
                
                outFile = fprefix + '.' + time.strftime ('%Y%m%d-%H%M%S') + '.txt'
                
                completeFile = os.path.join (saveDirectory, outFile)
                
                output = open (completeFile, 'w')
                
                
            #if r is response [-1]:
            #    
            #    output.close ()
        
        


