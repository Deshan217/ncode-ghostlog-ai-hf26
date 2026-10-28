"""Local-only GhostLog HTTP service using the Python standard library."""
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from engine import generate_story,model_status
ROOT=Path(__file__).resolve().parent/"static"
ROUTES={"/":("index.html","text/html; charset=utf-8"),"/style.css":("style.css","text/css; charset=utf-8"),"/app.js":("app.js","application/javascript; charset=utf-8")}
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def respond(self,status,body,kind="application/json; charset=utf-8"):
        self.send_response(status)
        for k,v in {"Content-Type":kind,"Content-Length":str(len(body)),"Cache-Control":"no-store","X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","Content-Security-Policy":"default-src 'self'; connect-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'"}.items():self.send_header(k,v)
        self.end_headers();self.wfile.write(body)
    def reply(self,status,data):self.respond(status,json.dumps(data).encode())
    def do_GET(self):
        p=urlsplit(self.path).path
        if p=="/api/status":return self.reply(200,model_status())
        if p not in ROUTES:return self.reply(404,{"error":"Not found"})
        name,mime=ROUTES[p];self.respond(200,(ROOT/name).read_bytes(),mime)
    def do_POST(self):
        if urlsplit(self.path).path!="/api/haunt":return self.reply(404,{"error":"Not found"})
        if self.headers.get("Origin","") not in ("","http://127.0.0.1:8766","http://localhost:8766"):return self.reply(403,{"error":"Local origin required"})
        if not self.headers.get("Content-Type","").startswith("application/json"):return self.reply(415,{"error":"JSON required"})
        try:
            length=int(self.headers.get("Content-Length","0"))
            if not 0<length<=11000:return self.reply(413,{"error":"Invalid body size"})
            self.reply(200,generate_story(json.loads(self.rfile.read(length))))
        except ValueError as e:self.reply(400,{"error":str(e)})
        except RuntimeError as e:self.reply(503,{"error":str(e)})
if __name__=="__main__":
    print("N-CODE GhostLog AI: http://127.0.0.1:8766",flush=True)
    ThreadingHTTPServer(("127.0.0.1",8766),Handler).serve_forever()
