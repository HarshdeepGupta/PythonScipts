
from pytube import YouTube
from pprint import pprint
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import sys

# yt = YouTube("http://www.youtube.com/watch?v=Ik-RsDGPI5Y")

# # pprint(yt.get_videos())
# video = yt.get('3gp', '144p')

# video.download('Desktop'+yt.filename+'.mp4');

link = ""
counter = 0
if len(sys.argv) == 1:
    link = input("URL of the youtube video to start: ")
    counter_ = input("No. of Videos to download: ")
elif len(sys.argv) == 3:
    link = sys.argv[1]
    counter_ = sys.argv[2]
else:
    raise ValueError("Incorrect initilization: Correct Usage is \n Either give no arguements or give link of the video followed by the no. of videos to download.")
    sys.exit()


try:
   counter = int(counter_)
except ValueError:
   print("Counter must be an integer")
    
print("Starting Video : " + link )
print("Count : " + str(counter))

http = httplib2.Http()
status, response = http.request(link)

print("Connection Established")
while counter:
    print(counter)
    # Download the video to which link points
    yt = YouTube(link);
    print("Downloading : " + yt.filename);   
    # video = yt.get('mp4', '720p')
    # video.download('Desktop'+yt.filename+'.mp4');
    ###########Downloading Finished. Prepare for the next step#############################
    # Parse the HTML received 
    soup = BeautifulSoup(response,"lxml")
    # Select the div containg the link to the next video
    div = soup.findAll('div', class_="autoplay-bar");      
    div = str(div);
    link_start_pos = div.find("href");
    link ='https://www.youtube.com' +  div[link_start_pos+6 : link_start_pos+26];
    status, response = http.request(link)
    counter -= 1;



print("Script finished")
