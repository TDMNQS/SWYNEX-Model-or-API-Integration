import json
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from app import Handler, ThreadingHTTPServer


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:'+str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def post(self, body):
        return urlopen(Request(self.base+'/api/compare',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'}),timeout=5)

    def test_comparison_roundtrip(self):
        with self.post({'question':'retriever','paper_ids':['P03','P04']}) as response:
            r=json.load(response)
        self.assertEqual(r['status'],'comparison')
        self.assertEqual(len(r['citations']),2)

    def test_invalid_requests_return_actionable_http_400(self):
        for body in [[], {'question':'retriever','paper_ids':['P03','P03']}, {'question':'retriever','paper_ids':['P03',{}]}]:
            with self.assertRaises(HTTPError) as e: self.post(body)
            self.assertEqual(e.exception.code,400)
            self.assertIn('error',json.load(e.exception))

    def test_invalid_json(self):
        with self.assertRaises(HTTPError) as e:
            urlopen(Request(self.base+'/api/compare',data=b'{bad json',headers={'Content-Type':'application/json'}),timeout=5)
        self.assertEqual(e.exception.code,400)

    def test_ui_and_evaluation_route(self):
        with urlopen(self.base,timeout=5) as response: self.assertIn(b'Compare two research notes',response.read())
        with urlopen(self.base+'/api/evaluation',timeout=5) as response: self.assertEqual(json.load(response)['total'],13)
