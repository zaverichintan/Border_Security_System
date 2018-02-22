import pycurl

c = pycurl.Curl()
c.setopt(c.URL, 'http://www.bordersec.olbx.in/chintan/simple.php')
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.HTTPHEADER, ['Accept:application/image'])
c.setopt(c.HTTPPOST, [
    ('fileupload', (
        # upload the contents of this file
        c.FORM_FILE, "/home/zaverichintan/Study/final_year_project/file-video-stream/detection_images/detetected20180208-001541.png"
    )),
])

c.perform()
# HTTP response code, e.g. 200.
print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
# Elapsed time for the transfer.
print('Time: %f' % c.getinfo(c.TOTAL_TIME))

c.close()
	