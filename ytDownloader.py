
from pytube import YouTube
from pprint import pprint
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

# yt = YouTube("http://www.youtube.com/watch?v=Ik-RsDGPI5Y")

# # pprint(yt.get_videos())
# video = yt.get('3gp', '144p')

# video.download('Desktop'+yt.filename+'.mp4');


http = httplib2.Http()
status, response = http.request('https://www.youtube.com/watch?v=mWRsgZuwf_8')

print("pageLoaded")
soup = BeautifulSoup(response, "lxml");
counter = 10;
while counter:
    print(counter)
    link="";
    soup = BeautifulSoup(response,"lxml")
    div = soup.findAll('div', class_="autoplay-bar");
    div = str(div);
    a = div.find("href");
    # print(a)
    # print(div[a+6:a+26])
    link ='https://www.youtube.com' +  div[a+6:a+26];
    yt = YouTube(link);
    print(yt.filename);
    status, response = http.request(link)
    counter -= 1;



print("Script finished")
