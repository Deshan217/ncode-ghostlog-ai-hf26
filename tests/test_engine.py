import unittest
from unittest.mock import patch
import engine
class Tests(unittest.TestCase):
 def test_moods(self):
  for mood in engine.MOODS:self.assertEqual(engine.validate({"logs":"[01:00] strange event","mood":mood})["mood"],mood)
 def test_short(self):
  with self.assertRaises(ValueError):engine.validate({"logs":"short"})
 def test_long(self):
  with self.assertRaises(ValueError):engine.validate({"logs":"a"*5001})
 def test_invalid_mood(self):
  with self.assertRaises(ValueError):engine.validate({"logs":"[01:00] strange event","mood":"other"})
 def test_not_object(self):
  with self.assertRaises(ValueError):engine.validate([])
 def test_model_unavailable(self):
  with patch("engine.urlopen",side_effect=OSError("offline")):
   with self.assertRaises(RuntimeError):engine.generate_story({"logs":"[01:00] strange event"})
 def test_offline_status(self):
  with patch("engine.urlopen",side_effect=OSError("offline")):self.assertFalse(engine.model_status()["online"])
 def test_output_validation(self):
  with self.assertRaises(RuntimeError):engine.required({},"title",120)
 def test_three_clues(self):
  class Fake:
   def __enter__(self):return self
   def __exit__(self,*args):pass
  output={"title":"The Signal","signal":" ".join(["whisper"]*120),"clues":["a","b","c"],"final_line":"It returned."}
  with patch("engine.urlopen",return_value=Fake()),patch("engine.json.load",return_value={"model":engine.MODEL,"done":True,"response":engine.json.dumps(output)}):
   result=engine.generate_story({"logs":"[00:00] unusual message"})
  self.assertEqual(result["generator"],"real-local-open-weight-model")

 def test_rejects_short_story(self):
  output={"title":"Signal","signal":"Only a summary.","clues":["a","b","c"],"final_line":"It returned."}
  with self.assertRaisesRegex(RuntimeError,"110 to 190"):
   engine.parse_story({"model":engine.MODEL,"done":True,"response":engine.json.dumps(output)})

 def test_malformed_envelopes(self):
  for value in (None, [], "wrong", {}, {"response":None}, {"response":"{}","done":False}, {"response":"{}","model":"other","done":True}):
   with self.subTest(value=value),self.assertRaises(RuntimeError):engine.parse_story(value)

 def test_retry_then_success(self):
  from io import BytesIO
  bad={"model":engine.MODEL,"done":True,"response":"{}"}
  good={"model":engine.MODEL,"done":True,"response":engine.json.dumps({"title":"Signal","signal":" ".join(["whisper"]*120),"clues":["a","b","c"],"final_line":"It returned."})}
  with patch("engine.urlopen",side_effect=[BytesIO(engine.json.dumps(bad).encode()),BytesIO(engine.json.dumps(good).encode())]) as call:
   result=engine.generate_story({"logs":"[00:00] unusual message"})
  self.assertEqual(result["attempts"],2)
  self.assertEqual(call.call_count,2)

 def test_retry_limit(self):
  from io import BytesIO
  with patch("engine.urlopen",side_effect=[BytesIO(b'null'),BytesIO(b'null')]) as call:
   with self.assertRaisesRegex(RuntimeError,"after two attempts"):engine.generate_story({"logs":"[00:00] unusual message"})
  self.assertEqual(call.call_count,2)

 def test_malformed_status(self):
  from io import BytesIO
  with patch("engine.urlopen",return_value=BytesIO(b'null')):self.assertFalse(engine.model_status()["online"])
