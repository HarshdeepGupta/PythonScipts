
from pytube import YouTube
from pprint import pprint
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import sys
import os
import sqlite3

def insert_in_database(database, f) :
    cursor = database.execute("SELECT name FROM SONGS WHERE name = (?)", (f,))
    data = cursor.fetchone()
    if data is None :
        database.execute("INSERT INTO SONGS VALUES (?);", (f,))
        database.commit() # Can do a commit before closing too.
        return 1
    else :
        return 0

def create_database(database,r) :
    database.execute('''CREATE TABLE IF NOT EXISTS SONGS (NAME TEXT NOT NULL);''')
    if r :
        files = os.listdir("../Songs/")
        for f in files:
            insert_in_database(database, os.path.splitext(f)[0])

def download_video(http, link, database) :
    status, response = http.request(link)
    curr_video_obj = YouTube(link)

    # Check if exits and add to database if it doesnt. Returns 1 if new video
    to_download  = insert_in_database(database, curr_video_obj.filename)
    if to_download :
        print("Downloading : " + curr_video_obj.filename)
        video = curr_video_obj.get('3gp', '144p')
        video.download('../Songs/' + curr_video_obj.filename + '.mp4')
    else :
        print ("Already Exists : " + curr_video_obj.filename)
    soup = BeautifulSoup(response,"lxml")

    # Select the div containg the link to the next video
    div = soup.findAll('div', class_="autoplay-bar")
    div = str(div)
    link_start_pos = div.find("href")
    return ('https://www.youtube.com' +  div[link_start_pos+6 : link_start_pos+26])

def download_videos(http, link, database, counter) :
    while counter:
        link = download_video(http,link, database)
        counter -= 1

def parse_input() :
    link = ""
    counter_ = 0;
    if len(sys.argv) == 1 :
        link = input("URL of the youtube video to start: ")
        counter_ = input("No. of Videos to download: ")
    elif len(sys.argv) == 3 :
        link = sys.argv[1]
        counter_ = sys.argv[2]
    else :
        raise ValueError("Incorrect initilization: Correct Usage is \n Either give no arguements or give link of the video followed by the no. of videos to download.")
        sys.exit()

    try :
       counter = int(counter_)
    except ValueError :
       print("Counter must be an integer")

    return link,counter


def main() :

    link , counter = parse_input()

    print("Starting Video : " + link )
    print("Count : " + str(counter))

    http = httplib2.Http()

    conn = sqlite3.connect('downloadedsongs.db')
    create_database(conn,0)

    download_videos(http,link, conn, counter)

    conn.close()
    print("Script finished")

main()
