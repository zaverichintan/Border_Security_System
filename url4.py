import requests
import json

url = 'http://www.bordersec.olbx.in/chintan/simple.php'
files = {'file': open('/home/zaverichintan/Study/final_year_project/file-video-stream/detection_images/detetected20180208-001541.png', 'rb')}

payload = {"device":"gabriel","data_type":"data","zone":1}
data = json.dumps(payload)
r = requests.post(url, files=files, data = payload)