"""Test REAL Ollama Gemma inference via application API and save evidence."""
from datetime import datetime,timezone
import json
from pathlib import Path
from urllib.request import Request,urlopen
sample={"logs":"[00:03:11] archived-session resumed after 13 years\n[00:03:12] user: nobody_here\n[00:03:13] room-temperature sensor: 2.1 C\n[00:03:14] playback.wav duration: 00:00:00\n[00:03:15] notification: you forgot the light","mood":"unsettling"}
req=Request("http://127.0.0.1:8766/api/haunt",data=json.dumps(sample).encode(),headers={"Content-Type":"application/json","Origin":"http://127.0.0.1:8766"},method="POST")
with urlopen(req,timeout=180) as r: result=json.load(r)
if result.get("generator")!="real-local-open-weight-model" or not result.get("signal") or len(result.get("clues",[]))!=3:raise SystemExit("Actual model verification failed")
Path("evidence").mkdir(exist_ok=True)
Path("evidence/real-gemma-story.json").write_text(json.dumps({"generated_at_utc":datetime.now(timezone.utc).isoformat(),"input":sample,"actual_model_output":result},ensure_ascii=False,indent=2))
print("VERIFIED REAL GEMMA INFERENCE: "+result["model"]+" title="+result["title"]+" clues="+str(len(result["clues"])))
