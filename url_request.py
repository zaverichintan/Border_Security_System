import urllib.parse
import urllib.request

url = 'http://localhost/border_security/api.php'
values = {'detected' : 'human',
          'location' : 'camera_1',
          'url_of_image' : '/home/ea' }

data = urllib.parse.urlencode(values).encode("utf-8")
req = urllib.request.Request(url, data)

response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page)