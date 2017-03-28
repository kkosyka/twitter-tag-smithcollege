"""
Kalynn Kosyka
Spatial Analysis Lab - Smith College
March 8, 2017
TwitterHashtag.py uses TwitterAPI to access information about tweets that contain a specific hashtag, the program will use
the data to input into a postgreSQL database (text, xcoor, ycoor, username, created, hashtags, twitterGeom (SRID 4326/GeoJSON)).
External: Database will be connected to Smith's SAL GeoServer where the data will be linked with Leaflet.

"""

#-----------------------------------------------------------------------------------
#                          Libraries
#-----------------------------------------------------------------------------------
# Import the necessary package to process data in JSON format
import json
import json as simplejson
import time
import datetime
import sched
import psycopg2
from decimal import *

#-----------------------------------------------------------------------------------
#                          Global Variables
#-----------------------------------------------------------------------------------
writeFile = "updateTestPostgres.csv" #name of csv file for twitter data

#-----------------------------------------------------------------------------------
#                          Functions
#-----------------------------------------------------------------------------------
def writeHeader():
    #writeHeader() - create header for CSV file
    newFile = writeFile
    fileName = open(newFile,"w")
    fileName.write("text, coorX, coorY, username, created at, hashtag(s) \n")

def printPretty(text, coorX, coorY, screenName, createdAt, hashtagsHolder):
    print text + "\n" + coorX + "\n" + coorY+ "\n" + screenName+ "\n" + createdAt+ "\n" + hashtagsHolder+ "\n \n"

def getData():
    #getData() - grab data from Twitter API and parsing the information in order to insert into database
    conn = psycopg2.connect("dbname='kkosyka_db' host='localhost' user='postgres' password='smithgis'") #(database information - database, host, user, password)
    cur = conn.cursor()
    
    # Import the necessary methods from "twitter" library
    from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

    # Variables that contains the user credentials to access Twitter API
    # Access values under Kalynn Kosyka, one may need to change for their projects
    ACCESS_TOKEN = '28930526-ttro9V7TUvuUfXMe4e3OBMlU38MuKn9ISLUwqMvP9'
    ACCESS_SECRET = 'dI0t4RRSJU53FciGw1jYfApDkx1x3znrWwH9zSdfetQjh'
    CONSUMER_KEY = '3KUdtFeceeLB3rs3pJDe4fbeM'
    CONSUMER_SECRET = 'vPps0BgF2Vm0UZXKdi67URWUnIl5ygk1m5KLRHbXVWwGHCoej1'
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)
    twitter = Twitter(auth=oauth)

    #Creates new file that will contain the most n-number of recent tweets that contain a particular hashtag
    newFile = writeFile
    fileName = open(newFile,"a")
    # Getting data from Twitter and going through the data
    json_input =  twitter.search.tweets(q='#sunset', result_type='recent', lang='en', count=100) #change q value for hashtag query
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
            text = str(text.replace("\n","<br/>"))
            coorX = "null"
            coorY = "null"
            coordinates = str(decoded["statuses"][x]["coordinates"]).encode('ascii', 'ignore')
            if not len(coordinates) <= 4: #if there are coordinates
                coor = True
                numCoor+=1
                coordinates = str(decoded["statuses"][x]["coordinates"]["coordinates"]).encode('ascii', 'ignore')
                coordinates = coordinates.split(",")
                coorX = (coordinates[0][1:len(coordinates[0])])
                coorY = (coordinates[1][0:len(coordinates[1])-1])
            if not coor: # filtering so we only get tweets with coordinates, otherwise we skip them
                continue
            else:
                screenName= (decoded["statuses"][x]["user"]["screen_name"]).encode('ascii', 'ignore')
                createdAt = (decoded["statuses"][x]["created_at"]).encode('ascii', 'ignore')
                hashtags = []
                for i in range(0, len(decoded["statuses"][x]["entities"]["hashtags"])):
                    hashtags.append(decoded["statuses"][x]["entities"]["hashtags"][i]["text"])
            print "num coor:\n" + str(numCoor)
            print "---------------------"
            
            #Write data in CSV format - text, coorX, coorY, username, created at, hashtag(s)
            #if one wants to save the data into a csv file, uncomment line below
            #fileName.write(text + "," + coorX +","+ coorY + ","+ screenName +"," + createdAt + ",")

            hashtagsHolder = ""
            for j in range (0, len(hashtags)):
                fileName.write("#" + hashtags[j] + " ")
                hashtagsHolder = hashtagsHolder + "#" + hashtags[j] + " "
                
            printPretty(text, coorX, coorY, screenName, createdAt, hashtagsHolder) #print data into console, comment out if not needed

            #Insert data into database - assuming database already exists
            #database - text(text), xcoor(numeric), ycoor(numeric), username(text), created(text), hashtags(text), twitterGeom (geometry - SRID 4326)
            cur.execute("""SELECT EXISTS(SELECT 1 FROM public."TwitterDataSample" WHERE text=%s AND xcoor=%s AND ycoor=%s AND username=%s AND created=%s AND hashtags=%s ) """,(text, coorX, coorY, screenName, createdAt, hashtagsHolder))

            if cur.fetchone()[0] == False:
                cur.execute("""INSERT INTO public."TwitterDataSample"(text, xcoor, ycoor, username, created, hashtags) VALUES
                        (%s,%s,%s, %s, %s, %s)""",(text, coorX, coorY, screenName, createdAt, hashtagsHolder))
            #Using and converting coordinate values into geometry value with SRID 4326
            cur.execute("""UPDATE public."TwitterDataSample" SET "twitterGeom" = ST_GeomFromText('POINT('||xcoor::text||' '||ycoor::text||')', 4326)""")
            conn.commit()

    except (ValueError, KeyError, TypeError):
        fileName.write ( "JSON format error")
    fileName.close()
    #print stars, used for pretty printing and dividing info in console - can be commented out
    print "*********************************************************"
    s.enter(3600, 1, getData, ()) #run every x sec, 3600s = 1hr
    s.run()
  
#-----------------------------------------------------------------------------------
#                          Main
#-----------------------------------------------------------------------------------
def main():
    writeHeader()
    getData()
 
main()
