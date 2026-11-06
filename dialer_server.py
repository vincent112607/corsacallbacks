#!/usr/bin/env python3
"""Corsa Life Dialer helper.
Runs the dialer at http://localhost:8765 and passes Call clicks to Dialpad.
It only listens on this computer. Close this window to stop it."""
import http.server, json, os, sys, urllib.request, urllib.error, webbrowser, threading

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "index.html")
ALLOWED = ("/initiate_call", "")

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, body, ctype="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(PAGE, "rb") as f: self.send(200, f.read(), "text/html; charset=utf-8")
        else: self.send(404, "{}")
    def do_POST(self):
        if self.path != "/api/dialpad" or self.headers.get("Origin", f"http://localhost:{PORT}") not in (f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}"):
            return self.send(403, "{}")
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            path, method = req.get("path", ""), req.get("method", "GET")
            if path not in ALLOWED or method not in ("GET", "POST"): return self.send(400, "{}")
            user = urllib.request.quote(str(req.get("user") or "me"), safe="")
            body = json.dumps(req["body"]).encode() if req.get("body") else None
            r = urllib.request.Request(f"https://dialpad.com/api/v2/users/{user}{path}", data=body, method=method,
                headers={"Authorization": "Bearer " + req.get("key", ""), "Content-Type": "application/json", "Accept": "application/json"})
            try:
                with urllib.request.urlopen(r, timeout=20) as resp: status, text = resp.status, resp.read().decode()
            except urllib.error.HTTPError as e: status, text = e.code, e.read().decode(errors="replace")
            self.send(200, json.dumps({"status": status, "body": text}))
            if path: print(("Dialed " if status < 300 else f"Dial failed ({status}) ") + (req.get("body") or {}).get("phone_number", ""))
        except Exception as e:
            self.send(200, json.dumps({"status": 0, "body": json.dumps({"error": {"message": str(e)}})}))

if __name__ == "__main__":
    if not os.path.exists(PAGE): sys.exit("Put this file in the same folder as index.html")
    try: srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H)
    except OSError: print("Dialer is already running."); webbrowser.open(f"http://localhost:{PORT}"); sys.exit()
    print(f"Corsa Life Dialer is running at http://localhost:{PORT}\nKeep this window open while you dial. Close it to stop.")
    threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    srv.serve_forever()
