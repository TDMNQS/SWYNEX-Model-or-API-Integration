"""Local browser app. Run python app.py and open http://127.0.0.1:8000."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from engine import PaperAssistant

assistant = PaperAssistant()
HTML = (Path(__file__).parent / 'web' / 'index.html').read_bytes()


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, data, content_type='application/json; charset=utf-8'):
        payload = data if isinstance(data, bytes) else json.dumps(data).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/': self.reply(200, HTML, 'text/html; charset=utf-8')
        elif path == '/api/papers': self.reply(200, [{'id':p['id'], 'title':p['title'], 'url':p['url']} for p in assistant.papers])
        elif path == '/health': self.reply(200, {'status':'ok', 'papers':len(assistant.papers), 'task':3})
        elif path == '/api/evaluation':
            report = Path(__file__).parent / 'examples' / 'evaluation_report.json'
            if report.exists(): self.reply(200, report.read_bytes())
            else: self.reply(404, {'error':'Run python evaluate.py to generate the report.'})
        else: self.reply(404, {'error':'Not found'})

    def do_POST(self):
        if self.path not in ('/api/ask', '/api/compare'):
            self.reply(404, {'error':'Not found'}); return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 8192: raise ValueError('Invalid request size.')
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict): raise ValueError('Request must be a JSON object.')
            result = assistant.compare(body.get('question'), body.get('paper_ids')) if self.path == '/api/compare' else assistant.ask(body.get('question'), body.get('paper_id'))
            self.reply(200, result)
        except (ValueError, TypeError) as exc:
            self.reply(400, {'error':str(exc)})
        except Exception:
            self.reply(500, {'error':'Unable to process this request. Please try again or restart the app.'})

    def log_message(self, *args):
        pass  # Do not log user questions.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'SWYNEX Research Q&A: http://127.0.0.1:{args.port} (Ctrl+C to stop)', flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
