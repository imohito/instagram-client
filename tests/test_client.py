import unittest
import os
import uuid
from instagram_client import Instagram

class TestClient(unittest.TestCase):

	def setUp(self):
		Instagram.KEY = os.environ['IGKEY'] 			# do NOT ask me for the key
		Instagram.DEVICEID = uuid.uuid4().hex
		self.username = os.environ['IGUSER']
		self.password = os.environ['IGPASSWD']
		
		if 	not Instagram.KEY or\
			not Instagram.DEVICEID or\
			not self.username or\
			not self.password:
			print "*** You must define IGKEY, DEVICEID, IGUSER and IGPASSWORD ***"
			self.assertTrue(False)

	def testUpload(self):
		client = Instagram()
		client.login(self.username, self.password)
		self.assertTrue(client.r.status_code == 200)
		
		dir = os.path.dirname(os.path.abspath( __file__ ))
		media_id = client.upload(dir+'/test.jpg')
		self.assertTrue(media_id)
		self.assertTrue(client.r.status_code == 200)
		
		client.configure(media_id, "My caption")
		self.assertTrue(client.r.status_code == 200)
