"""Protocol/credential tests use a fake loopback server, never real AI services."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
CLIENT=ROOT/'skills/configure-ai-providers/scripts/ai_client.py'
spec=importlib.util.spec_from_file_location('ai_client',CLIENT)
client=importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)


class Handler(BaseHTTPRequestHandler):
    calls=[]
    def log_message(self,*args): pass
    def do_GET(self): self.respond()
    def do_POST(self): self.respond()
    def respond(self):
        data=json.loads(self.rfile.read(int(self.headers['Content-Length']))) if self.headers.get('Content-Length') else None
        self.calls.append((self.command,self.path,dict(self.headers),data))
        if self.path.startswith('/redirect'):
            self.send_response(302);self.send_header('Location','/v1/models');self.end_headers();return
        if self.path.startswith('/error'):
            self.send_response(401);self.end_headers();self.wfile.write(b'synthetic-secret private-error');return
        if self.path.startswith('/bad-json'):
            self.send_response(200);self.end_headers();self.wfile.write(b'not JSON');return
        bodies={
            '/v1/models':{'data':[{'id':'example-model'}]},
            '/v1/chat/completions':{'choices':[{'message':{'content':'three concepts'}}]},
            '/api/tags':{'models':[{'name':'example-model'}]},
            '/api/chat':{'message':{'content':'three concepts'}},
            '/system_stats':{'system':{'runtime':'synthetic'}},
            '/prompt':{'prompt_id':'test-job','node_errors':{}},
            '/history/test-job':{'test-job':{'status':{'completed':True,'status_str':'success'}}},
            '/history/unknown':{},
            '/empty/chat/completions':{'choices':[{'message':{'content':None}}]},
        }
        if self.path not in bodies:
            self.send_response(404);self.end_headers();return
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
        self.wfile.write(json.dumps(bodies[self.path]).encode())


class ClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def setUp(self): Handler.calls.clear()
    def configured(self,adapter='openai-chat',suffix='/v1',**options):
        config={'routes':{'language':'text','media':'media'},'profiles':{
            'text':dict(adapter=adapter,base_url_env='ENDPOINT',model_env='MODEL',api_key_env='KEY',**options),
            'media':{'adapter':'manual'}}}
        return client.resolve_profile(config,{'ENDPOINT':self.url+suffix,'MODEL':'example-model','KEY':'synthetic-secret'})
    def test_openai_request_and_bearer(self):
        p=self.configured(max_output_tokens=42,token_limit_field='max_completion_tokens')
        self.assertEqual(client.chat(p,'example'),'three concepts')
        method,path,headers,body=Handler.calls[-1]
        self.assertEqual((method,path),('POST','/v1/chat/completions'))
        self.assertEqual(headers['Authorization'],'Bearer synthetic-secret')
        self.assertEqual(body['max_completion_tokens'],42)
        self.assertEqual(body['messages'],[{'role':'user','content':'example'}])
        self.assertIs(body['stream'],False)
    def test_ollama_request(self):
        self.assertEqual(client.chat(self.configured('ollama-chat',''),'example'),'three concepts')
        self.assertEqual(Handler.calls[-1][1],'/api/chat')
        self.assertEqual(Handler.calls[-1][3]['options'],{'num_predict':512})
    def test_probes_do_not_generate(self):
        for adapter,suffix in [('openai-chat','/v1'),('ollama-chat',''),('comfyui','')]:
            self.assertIn('reachable',client.probe(self.configured(adapter,suffix))['status'])
        self.assertTrue(all(call[0]=='GET' for call in Handler.calls))
    def test_comfy_submit_and_status(self):
        p=self.configured('comfyui','')
        graph={'1':{'class_type':'ExampleNode','inputs':{'seed':7}}}
        self.assertEqual(client.submit_workflow(p,graph)['prompt_id'],'test-job')
        self.assertEqual(Handler.calls[-1][3]['prompt'],graph)
        self.assertIn('completed',client.job_status(p,'test-job')['status'])
        self.assertIn('not in history',client.job_status(p,'unknown')['status'])
    def test_ui_workflow_is_rejected_before_network(self):
        with self.assertRaises(client.ConfigError):
            client.submit_workflow(self.configured('comfyui',''),{'nodes':[]})
        self.assertEqual(Handler.calls,[])
    def test_errors_do_not_print_response_or_secret(self):
        p=self.configured(suffix='/error')
        with self.assertRaises(client.ConfigError) as error:client.probe(p)
        self.assertIn('401',str(error.exception))
        self.assertNotIn('synthetic-secret',str(error.exception))
        self.assertNotIn('private-error',str(error.exception))
        self.assertNotIn(self.url,str(error.exception))
    def test_redirect_does_not_forward_auth(self):
        with self.assertRaises(client.ConfigError):client.probe(self.configured(suffix='/redirect'))
        self.assertEqual(len(Handler.calls),1)
    def test_bad_json_and_empty_model_response(self):
        with self.assertRaises(client.ConfigError):client.probe(self.configured(suffix='/bad-json'))
        with self.assertRaises(client.ConfigError):client.chat(self.configured(suffix='/empty'),'example')
    def test_secret_not_required_on_no_auth_server(self):
        p=self.configured();p['headers'].pop('Authorization')
        client.probe(p)
        self.assertNotIn('Authorization',Handler.calls[-1][2])
    def test_required_key_is_validated_before_network(self):
        cfg={'routes':{'language':'x'},'profiles':{'x':{'adapter':'openai-chat','base_url_env':'URL','model_env':'M','api_key_env':'K','require_api_key':True}}}
        with self.assertRaises(client.ConfigError):client.resolve_profile(cfg,{'URL':self.url+'/v1','M':'example'})
        self.assertEqual(Handler.calls,[])
    def test_literal_dotenv_and_process_override(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'.env';p.write_text('TEST_A="file"\nTEST_B=$(not-executed)\nTEST_C=literal#hash\n')
            with patch.dict(os.environ,{'TEST_A':'process'},clear=True):
                values=client.load_env(p)
            self.assertEqual(values['TEST_A'],'process')
            self.assertEqual(values['TEST_B'],'$(not-executed)')
            self.assertEqual(values['TEST_C'],'literal#hash')
    def test_url_credentials_and_remote_http_are_rejected(self):
        cfg={'routes':{'language':'x'},'profiles':{'x':{'adapter':'openai-chat','base_url_env':'URL','model_env':'M'}}}
        for url in ['https://' + 'user:pass@service.example/v1','https://service.example/v1?key=secret','http://service.example/v1']:
            with self.assertRaises(client.ConfigError):client.resolve_profile(cfg,{'URL':url,'M':'example'})
    def test_manual_and_dry_run_never_send(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            cfg={'version':1,'routes':{'language':'text','media':'manual'},'profiles':{'text':{'adapter':'openai-chat','base_url_env':'URL','model_env':'MODEL'},'manual':{'adapter':'manual'}}}
            (d/'config.json').write_text(json.dumps(cfg));(d/'.env').write_text('URL='+self.url+'/v1\nMODEL=example\n');(d/'prompt.txt').write_text('private-prompt')
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(client.main(['--config',str(d/'config.json'),'--env-file',str(d/'.env'),'chat','--prompt-file',str(d/'prompt.txt')]),0)
                self.assertEqual(client.main(['--config',str(d/'config.json'),'--env-file',str(d/'.env'),'--role','media','probe']),0)
            self.assertEqual(Handler.calls,[])
            self.assertNotIn('private-prompt',output.getvalue())
            self.assertNotIn(self.url,output.getvalue())
    def test_portable_installed_folder_contains_client_and_templates(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--harness','claude','--project',d],check=True,capture_output=True)
            skill=Path(d)/'.claude/skills/configure-ai-providers'
            self.assertTrue((skill/'assets/.env.example').is_file())
            subprocess.run([sys.executable,str(skill/'scripts/ai_client.py'),'--help'],check=True,capture_output=True)


if __name__=='__main__':unittest.main()
