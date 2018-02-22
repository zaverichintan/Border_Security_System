import requests
import json

url = 'http://www.bordersec.olbx.in/ci/test_api'
files = {'file': open('/home/zaverichintan/Study/final_year_project/file-video-stream/detection_images/detetected20180208-001541.png', 'rb')}

payload = {"device":"Chintan","data_type":"data","zone":1,"camera_no":1}
data = json.dumps(payload)
r = requests.post(url, files=files, data = payload)
print(r.text)
