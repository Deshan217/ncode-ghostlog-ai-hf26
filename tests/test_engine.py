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
  output={"title":"The Signal","signal":"A strange story","clues":["a","b","c"],"final_line":"It returned."}
  with patch("engine.urlopen",return_value=Fake()),patch("engine.json.load",return_value={"response":engine.json.dumps(output)}):
   result=engine.generate_story({"logs":"[00:00] unusual message"})
  self.assertEqual(result["generator"],"real-local-open-weight-model")
