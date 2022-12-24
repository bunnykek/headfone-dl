import requests
import re
import json
import subprocess
import os

class Headfone:
    def __init__(self):
        self.session = requests.Session()

    def download(self, url: str):
        response = self.session.get(url)
        raw_json = re.search("tracks = (.+);", response.text).group(1)
        channel_name = re.search("<div class=channel-info-title> (.+?) </div>", response.text).group(1)
        folder_path = os.path.join(os.getcwd(), "Downloads", channel_name)
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        json_data = json.loads(raw_json)
        num = 1
        cdn = re.search("https://(.+?).cloudfront.net", json_data[0]['url']).group(1)

        for audio in json_data:
            title =  f"{str(num).zfill(2)}. {audio['title']}.m4a"
            num+=1
            print("Downloading", title)
            url = audio['url']
            if "cdn" in url:
                url = url.replace("cdn", cdn)
            # print(url)
            file_path = os.path.join(folder_path, title)
            if(os.path.exists(file_path)): continue
            subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", url, "-c", "copy", file_path])
        
if __name__ == "__main__":
    url = input("Enter the Headfone channel url: ")
    headfone = Headfone()
    headfone.download(url)