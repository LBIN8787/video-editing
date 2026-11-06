import json,tempfile,unittest
from pathlib import Path
from auth import save_token
from watch_windows_oauth import desktop_client
class SetupTests(unittest.TestCase):
 def test_only_matching_google_desktop_client_is_accepted(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'client.json';data={'installed':{'project_id':'project-a','client_id':'fixture-client','client_secret':'fixture-only','token_uri':'https://oauth2.googleapis.com/token','auth_uri':'https://accounts.google.com/o/oauth2/auth'}}
   p.write_text(json.dumps(data),encoding='utf-8')
   self.assertTrue(desktop_client(p,'project-a'));self.assertFalse(desktop_client(p,'project-b'))
   data['installed']['token_uri']='https://example.invalid/token';p.write_text(json.dumps(data),encoding='utf-8');self.assertFalse(desktop_client(p,'project-a'))
 def test_service_account_file_is_not_a_desktop_client(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'client.json';p.write_text('{"type":"service_account"}',encoding='utf-8');self.assertFalse(desktop_client(p,'project-a'))
 def test_local_secret_writer_uses_utf8(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'private.json';save_token(p,'{"label":"한글 연결 검사"}');self.assertEqual(json.loads(p.read_text(encoding='utf-8'))['label'],'한글 연결 검사')
if __name__=='__main__':unittest.main()
