import json
import importlib.util
from pathlib import Path
import unittest
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validate',ROOT/'scripts/validate.py')
validate=importlib.util.module_from_spec(spec);spec.loader.exec_module(validate)


class DistributionTests(unittest.TestCase):
    def test_only_reviewed_unchanged_sample_binary_is_allowed(self):
        path=ROOT/'examples/generated-media/pilot-still.png'
        data=path.read_bytes()
        self.assertTrue(validate.reviewed_binary(path,data))
        self.assertFalse(validate.reviewed_binary(path,data+b'changed'))
        self.assertFalse(validate.reviewed_binary(ROOT/'unreviewed.png',data))
    def test_every_reviewed_asset_exists_and_matches(self):
        assets=json.loads((ROOT/'docs/REVIEWED-ASSETS.json').read_text())['assets']
        self.assertEqual(len(assets),len({a['path'] for a in assets}))
        for asset in assets:
            path=ROOT/asset['path']
            self.assertTrue(validate.reviewed_binary(path,path.read_bytes()),asset['path'])
            self.assertFalse(validate.reviewed_binary(path,path.read_bytes()+b'changed'))

    def test_detects_private_paths_and_credentials_without_returning_value(self):
        samples=['/Users/'+'example/private', 'https://' + 'user:pass@service.example', 'gh'+'p_'+'a'*30, '-----BEGIN '+'PRIVATE KEY-----']
        for sample in samples:
            findings=validate.privacy_findings(Path('sample.md'),sample)
            self.assertTrue(findings)
            self.assertNotIn(sample,str(findings))
    def test_private_config_filenames_rejected_but_example_allowed(self):
        for name in ['.env','.env.backup','providers.local.json','machine.local.yaml','access.pem']:
            self.assertTrue(validate.privacy_findings(Path(name),''))
        self.assertEqual(validate.privacy_findings(Path('.env.example'),'API_KEY='),[])
    def test_non_loopback_addresses_rejected(self):
        self.assertTrue(validate.privacy_findings(Path('sample.md'),'.'.join(['10','3','4','5'])))
        self.assertEqual(validate.privacy_findings(Path('sample.md'),'http://127.0.0.1:8188'),[])

    def test_installer_excludes_private_configuration_and_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'package'
            (root/'scripts').mkdir(parents=True)
            shutil.copyfile(ROOT/'scripts/install.py',root/'scripts/install.py')
            skill=root/'skills/example';skill.mkdir(parents=True)
            (skill/'SKILL.md').write_text('example')
            (skill/'.env.example').write_text('API_KEY=')
            (skill/'.env').write_text('API_KEY=synthetic')
            (skill/'providers.local.json').write_text('{}')
            (skill/'__pycache__').mkdir();(skill/'__pycache__/ignored.pyc').write_text('cache')
            dest=Path(directory)/'recipient'
            subprocess.run([sys.executable,str(root/'scripts/install.py'),'--harness','codex','--project',str(dest)],check=True,capture_output=True)
            target=dest/'.agents/skills/example'
            self.assertEqual({p.name for p in target.iterdir()},{'SKILL.md','.env.example'})


if __name__=='__main__':unittest.main()
