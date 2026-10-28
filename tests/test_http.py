import unittest,json,threading
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from unittest.mock import patch
from server import Handler
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
  cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
  cls.url="http://127.0.0.1:"+str(cls.server.server_port)
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
 def test_home(self):
  with urlopen(self.url) as r:self.assertEqual(r.status,200)
 def test_static(self):
  for p in ("/app.js","/style.css"):
   with urlopen(self.url+p) as r:self.assertEqual(r.status,200)
 def test_unknown(self):
  with self.assertRaises(HTTPError) as x:urlopen(self.url+"/nothing");self.assertEqual(x.exception.code,404)
 def test_bad_origin(self):
  req=Request(self.url+"/api/haunt",data=b'{"logs":"something strange"}',headers={"Content-Type":"application/json","Origin":"https://example.org"},method="POST")
  with self.assertRaises(HTTPError) as x:urlopen(req)
  self.assertEqual(x.exception.code,403)
 def test_model_offline(self):
  req=Request(self.url+"/api/haunt",data=json.dumps({"logs":"[00:00] strange message"}).encode(),headers={"Content-Type":"application/json"},method="POST")
  with patch("server.generate_story",side_effect=RuntimeError("offline")):
   with self.assertRaises(HTTPError) as x:urlopen(req)
  self.assertEqual(x.exception.code,503)
