import pyperclip
import time
import requests

machine_id = 1001
# to support ios , ws is not applied.
base_url = "http://127.0.0.1:5000" + "/"
pyperclip.set_clipboard("xsel")
clip_cache=""
while True:
    clipb = pyperclip.paste()
    if clipb != clip_cache:
        print("change detected")
        clip_cache = clipb
        #update to server
        requests.get(base_url+"update?data="+clipb)
    time.sleep(0.1)