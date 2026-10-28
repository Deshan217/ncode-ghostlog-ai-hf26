"""Test REAL Ollama Gemma inference via application API and save evidence."""
from datetime import datetime,timezone
import json,os,platform
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
sample={"logs":"[00:03:11] archived-session resumed after 13 years\n[00:03:12] user: nobody_here\n[00:03:13] room-temperature sensor: 2.1 C\n[00:03:14] playback.wav duration: 00:00:00\n[00:03:15] notification: you forgot the light","mood":"unsettling"}
req=Request("http://127.0.0.1:8766/api/haunt",data=json.dumps(sample).encode(),headers={"Content-Type":"application/json","Origin":"http://127.0.0.1:8766"},method="POST")
Path("evidence").mkdir(exist_ok=True)
try:
 with urlopen(req,timeout=330) as r: result=json.load(r)
except HTTPError as exc:
 error=exc.read().decode("utf-8",errors="replace")
 Path("evidence/inference-failure.json").write_text(json.dumps({"input":sample,"status":exc.code,"error":error},indent=2),encoding="utf-8")
 raise SystemExit("Real inference rejected: "+error) from exc
words=len(result.get("signal","").split())
inference=result.get("inference",{})
if result.get("generator")!="real-local-open-weight-model" or result.get("model")!="gemma3:1b" or not 110<=words<=190 or len(result.get("clues",[]))!=3 or inference.get("done") is not True or inference.get("model")!="gemma3:1b":raise SystemExit("Actual model verification failed")
raw=json.loads(inference["response"])
if raw.get("signal","").strip()!=result["signal"]:raise SystemExit("Application output does not match actual model response")
with urlopen("http://127.0.0.1:11434/api/version",timeout=10) as r: version=json.load(r)
with urlopen("http://127.0.0.1:11434/api/tags",timeout=10) as r: models=json.load(r)
Path("evidence").mkdir(exist_ok=True)
Path("evidence/real-gemma-story.json").write_text(json.dumps({"generated_at_utc":datetime.now(timezone.utc).isoformat(),"commit":os.environ.get("GITHUB_SHA"),"run_id":os.environ.get("GITHUB_RUN_ID"),"python":platform.python_version(),"ollama":version,"models":models,"story_word_count":words,"input":sample,"actual_model_output":result},ensure_ascii=False,indent=2),encoding="utf-8")
print("VERIFIED REAL GEMMA INFERENCE: "+result["model"]+" title="+result["title"]+" clues="+str(len(result["clues"]))+" story_words="+str(words))
