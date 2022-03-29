import random
import time
import requests
from urllib.parse import urlparse
import os
import ctypes
import time as t
import shutil
from datetime import datetime
from screeninfo import get_monitors

if not os.path.exists(os.getcwd()+"\Image"):
    os.mkdir("Image")
mratio = get_monitors()[0].width/get_monitors()[0].height

def download(src):
    mypath = os.getcwd()+r"\Image\image"
    r = requests.get(src, stream=True)
    if r.status_code == 200:
        path = urlparse(src).path
        ext = os.path.splitext(path)[1]
        with open(mypath+ext, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            return mypath+ext

def choose_wallpaper(query, apikey):
    while True:
        try:
            global mratio
            srces = []
            URL = "https://api.pexels.com/v1/search?query="+query

            for i in range(10):

                HEADERS = {
                    "Authorization": apikey
                }
                data = requests.get(URL, headers=HEADERS).json()

                for photo in data["photos"]:
                    src = photo["src"]["original"]
                    dr = max(photo["width"], photo["height"])/min(photo["width"], photo["height"])
                    if dr >= (mratio - 0.3) and dr <= (mratio + 0.2) and photo["width"] - photo["height"] > 300:
                        srces.append(src)
                
                URL = data["next_page"]
            
            src = random.choice(srces)
            path = download(src)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            break
        except:
            pass

def dt_time(current_time):
    if current_time > 17 or current_time <= 5:
        time = "night sky"
    if current_time > 5 and current_time <= 7:
        time = "sunrise"
    if current_time > 7 and current_time <= 10:
        time = "morning sun"
    if current_time > 10 and current_time <= 15:
        time = "midday wallpaper"
    if current_time > 15 and current_time <= 17:
        time = "sunset"

    return time

APIKEY = ""
now = datetime.now()
current_time = int(now.strftime("%H"))
time = dt_time(current_time)
choose_wallpaper(time, APIKEY)

while True:
    n = datetime.now()
    ct = int(n.strftime("%H"))

    if ct is not current_time:
        time = dt_time(ct)
        choose_wallpaper(time, APIKEY)
        current_time = ct
    else:
        pass
    t.sleep(60)
