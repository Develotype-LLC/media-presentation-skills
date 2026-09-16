#!/usr/bin/env python3
"""Copy skill source and examples without personal configuration or build artifacts."""
import argparse
from pathlib import Path
import shutil


def private_or_generated(name):
    return (name in {'.git', '__pycache__', 'node_modules', '.DS_Store', 'out', 'outputs'}
            or (name.startswith('.env') and name != '.env.example')
            or name.endswith(('.pyc', '.local.json', '.local.yaml', '.local.yml', '.pem', '.key', '.gguf', '.safetensors')))


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--harness',choices=['codex','claude','copilot'],required=True)
    p.add_argument('--project',type=Path,required=True)
    p.add_argument('--dry-run',action='store_true')
    a=p.parse_args(argv)
    base=Path(__file__).resolve().parents[1]
    dest=a.project.expanduser().resolve() / {'codex':'.agents/skills','claude':'.claude/skills','copilot':'.github/skills'}[a.harness]
    folders=sorted(x.parent for x in (base/'skills').glob('*/SKILL.md'))
    conflicts=[dest/x.name for x in folders if (dest/x.name).exists() or (dest/x.name).is_symlink()]
    if conflicts:
        p.exit(1,'Refusing to overwrite: '+', '.join(map(str,conflicts))+'\n')
    for folder in folders:
        # Never follow a source symlink into personal files outside the package.
        if folder.is_symlink() or any(x.is_symlink() for x in folder.rglob('*')):
            p.exit(1,'Refusing skill source containing symlinks\n')
    for folder in folders:
        print(('Would copy ' if a.dry_run else 'Copying ')+folder.name+' -> '+str(dest/folder.name))
    if not a.dry_run:
        dest.mkdir(parents=True,exist_ok=True)
        for folder in folders:
            shutil.copytree(folder,dest/folder.name,ignore=lambda directory,names:[n for n in names if private_or_generated(n)])
    print('INSTALL PLAN OK' if a.dry_run else 'INSTALL OK')
    return 0


if __name__=='__main__':raise SystemExit(main())
