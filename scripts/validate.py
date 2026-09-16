#!/usr/bin/env python3
"""Validate distributable files only, without reading ignored personal configuration."""
from pathlib import Path
import ast
import hashlib
import ipaddress
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def reviewed_binary(path, data):
    """Only the explicitly reviewed sample, with its recorded hash, may ship."""
    try:
        rel=path.relative_to(ROOT).as_posix()
        manifest=json.loads((ROOT/'docs/REVIEWED-ASSETS.json').read_text())
        matches=[a for a in manifest['assets'] if a['path']==rel]
        return (len(matches)==1 and rel.startswith('examples/')
                and path.suffix in {'.png','.jpg','.mp4','.woff2'}
                and matches[0]['sha256']==hashlib.sha256(data).hexdigest())
    except (OSError, ValueError, KeyError, TypeError):
        return False


def privacy_findings(path, text):
    findings=[]
    name=path.name
    if (name.startswith('.env') and name!='.env.example') or name.endswith(('.local.json','.local.yaml','.local.yml','.pem','.key','.gguf','.safetensors')):
        findings.append('private configuration, key, or model file is in distributable set')
    patterns={
        'personal home path': r'(?:/Users/|/home/)[A-Za-z][A-Za-z0-9_-]*/|[A-Z]:\\Users\\[A-Za-z]',
        'private key material': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'access token': r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16})',
        'credential in URL': r'https?://[^\s/@:]+:[^\s/@]+@',
    }
    for label,pattern in patterns.items():
        if re.search(pattern,text):findings.append(label)
    for value in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text):
        try:address=ipaddress.ip_address(value)
        except ValueError:continue
        if not address.is_loopback and not address.is_unspecified:
            findings.append('non-loopback IP literal; use recipient configuration')
            break
    return findings


def distributable_files():
    result=subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT,capture_output=True)
    if result.returncode:
        raise RuntimeError('Run validation from a Git checkout so ignored local files stay private')
    return sorted({ROOT/x for x in result.stdout.decode().split('\0') if x and (ROOT/x).is_file()})


def validate():
    errors=[]
    for path in distributable_files():
        rel=path.relative_to(ROOT)
        try:text=path.read_text()
        except UnicodeError:
            if not reviewed_binary(path,path.read_bytes()):
                errors.append(f'{rel}: unexpected or changed binary file; review before distribution')
            continue
        for label in privacy_findings(path,text):errors.append(f'{rel}: {label}')
        if path.name=='SKILL.md':
            match=re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n',text)
            if not match or match[1]!=path.parent.name:errors.append(f'{rel}: invalid skill metadata')
        if path.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in link or link.startswith('#'):continue
                if not (path.parent/link.split('#')[0]).exists():errors.append(f'{rel}: missing relative link')
        if path.suffix=='.json':
            try:json.loads(text)
            except ValueError:errors.append(f'{rel}: invalid JSON')
        if path.suffix=='.py':
            try:ast.parse(text)
            except SyntaxError:errors.append(f'{rel}: invalid Python syntax')
    if errors:
        print('\n'.join(errors));return 1
    print(f'PASS: {len(list((ROOT/"skills").glob("*/SKILL.md")))} skills; distributable metadata, links, syntax, and privacy patterns')
    return 0


if __name__=='__main__':raise SystemExit(validate())
