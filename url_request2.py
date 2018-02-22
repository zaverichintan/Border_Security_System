import pycurl

wrapper = []
c = pycurl.Curl()
c.setopt(pycurl.URL, "http://www.bordersec.olbx.in/chintan/php-receive-file.php")
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, c.FORM_FILE, "/home/zaverichintan/Study/final_year_project/file-video-stream/detection_images/detetected20180208-001541.png")


c.perform()
c.close()
data = b.getvalue()
