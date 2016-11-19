# Import the necessary package to process data in JSON format

import json
import simplejson as json
import time
import datetime
import sched

writeFile = "attemptTimer.csv"

def writeHeader():
    newFile = writeFile
    fileName = open(newFile,"w") #"a"
    fileName.write("text, coorX, coorY, username, created at, hashtag(s) \n")


roundCount = 0
def getData():
    global roundCount
    
    # Import the necessary methods from "twitter" library
    from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '28930526-ttro9V7TUvuUfXMe4e3OBMlU38MuKn9ISLUwqMvP9'
    ACCESS_SECRET = 'dI0t4RRSJU53FciGw1jYfApDkx1x3znrWwH9zSdfetQjh'
    CONSUMER_KEY = '3KUdtFeceeLB3rs3pJDe4fbeM'
    CONSUMER_SECRET = 'vPps0BgF2Vm0UZXKdi67URWUnIl5ygk1m5KLRHbXVWwGHCoej1'

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)
    twitter = Twitter(auth=oauth)

    #Creates new file that will contain the most 30 recent tweets that contain #smithcollege
    newFile = writeFile
    fileName = open(newFile,"a") #"a"
    #fileName.write("text, coorX, coorY, username, created at, hashtag(s) \n")
    
    """
    if (roundCount == 0):
        print "yes"
        numCount = 100
    else:
        numCount=5
        print "no"

    print numCount
    """
    json_input =  twitter.search.tweets(q='#sunset', result_type='recent', lang='en', count=100)
    json_input = json.dumps(json_input)
    s = sched.scheduler(time.time, time.sleep)
    try:
        decoded = json.loads(json_input)

        print len(decoded["statuses"])
        numCoor = 0
        for x in range(0, len(decoded["statuses"]) ):
            coor = False
            text =((decoded["statuses"][x]["text"]).encode('ascii', 'ignore'))
            text= text.replace(",", "/")
            text = text.replace("\n","<br/>")
            coorX = "null"
            coorY = "null"
            coordinates = str(decoded["statuses"][x]["coordinates"]).encode('ascii', 'ignore')
            if not len(coordinates) <= 4: #if there are coordinates
                coor = True
                numCoor+=1
                coordinates = str(decoded["statuses"][x]["coordinates"]["coordinates"]).encode('ascii', 'ignore')
                coordinates = coordinates.split(",")
                coorX = coordinates[0][1:len(coordinates[0])]
                coorY = coordinates[1][0:len(coordinates[1])-1]
            if not coor: #filtering so we only get tweets with coordinates, otherwise we skip them
                continue
            else:
                screenName= (decoded["statuses"][x]["user"]["screen_name"]).encode('ascii', 'ignore')
                createdAt = (decoded["statuses"][x]["created_at"]).encode('ascii', 'ignore')
                hashtags = []
                for i in range(0, len(decoded["statuses"][x]["entities"]["hashtags"])):
                    hashtags.append(decoded["statuses"][x]["entities"]["hashtags"][i]["text"])
            print "num coor:\n" + str(numCoor)
            print "---------------------"
            
            #write file in CSV format
            fileName.write(text + "," + coorX +","+ coorY + ","+ screenName +"," + createdAt + ",")
            for j in range (0, len(hashtags)):
                fileName.write("#" + hashtags[j] + " ")
            fileName.write("\n")
            
    except (ValueError, KeyError, TypeError):
        fileName.write ( "JSON format error")
    
    fileName.close()
    print "*********************************************************"
    roundCount += 1
    s.enter(900, 1, getData, ())#1800
    s.run()

def main():
    writeHeader()
    getData()
 
main()



"""
#write file in easy to read format
fileName.write("TEXT: \n" + text + "\n\n"+"COORDINATES: \n" + coordinates + "\n\n"+ "USERNAME: \n" + screenName + "\n\n"+"CREATED AT: \n" + createdAt + "\n\n")
fileName.write("HASHTAG(S) \n")
for j in range (0, len(hashtags)):
    fileName.write(hashtags[j]+"\n")
fileName.write("----------------------------------------------------------" + "\n")
"""
