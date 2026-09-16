#!/usr/bin/env python3
"""Portable endpoint client. No model installation, implicit generation, or cloud fallback."""
import argparse
import json
import os
from pathlib import Path
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


class ConfigError(ValueError):
    pass


def load_env(path):
    """Literal dotenv subset. Existing process variables take precedence."""
    values = {}
    if path.exists():
        for number, raw in enumerate(path.read_text().splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            key, sep, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if not sep or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
                raise ConfigError(f'Invalid .env assignment at line {number}; contents hidden')
            if value.startswith(('"', "'")):
                if len(value) < 2 or value[-1] != value[0]:
                    raise ConfigError(f'Unclosed .env quote at line {number}')
                value = value[1:-1]
            values[key] = value
    values.update(os.environ)
    return values


def load_config(path):
    try:
        config = json.loads(path.read_text())
    except (OSError, ValueError):
        raise ConfigError('Cannot read valid provider configuration JSON') from None
    if not isinstance(config, dict) or config.get('version') != 1:
        raise ConfigError('Provider configuration must have version 1')
    profiles, routes = config.get('profiles'), config.get('routes')
    if not isinstance(profiles, dict) or not profiles or not isinstance(routes, dict):
        raise ConfigError('Profiles and routes must be objects')
    for name, profile in profiles.items():
        if not re.fullmatch(r'[a-z0-9-]+', name) or not isinstance(profile, dict):
            raise ConfigError('Profile names must be lowercase letters, numbers, or hyphens')
        if profile.get('adapter') not in {'openai-chat', 'ollama-chat', 'comfyui', 'manual'}:
            raise ConfigError(f'Unsupported adapter in profile {name}')
    for role in ['language', 'media']:
        if routes.get(role) not in profiles:
            raise ConfigError(f'Missing or unknown profile for {role} route')
    if profiles[routes['language']]['adapter'] not in {'openai-chat', 'ollama-chat', 'manual'}:
        raise ConfigError('Language route requires a chat or manual adapter')
    if profiles[routes['media']]['adapter'] not in {'comfyui', 'manual'}:
        raise ConfigError('Media route requires a ComfyUI or manual adapter')
    return config


def resolve_profile(config, env, role='language', selected=None):
    name = selected or config['routes'][role]
    if name not in config['profiles']:
        raise ConfigError('Unknown profile')
    p = dict(config['profiles'][name])
    p['name'] = name
    if p['adapter'] == 'manual':
        return p

    def variable(field, required=False):
        key = p.get(field)
        if key is not None and (not isinstance(key, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key)):
            raise ConfigError(f'{field} must name an environment variable')
        value = env.get(key, '') if key else ''
        if required and not value:
            raise ConfigError(f'Set the environment variable referenced by {field} for {name}')
        return value

    p['base_url'] = variable('base_url_env', True).rstrip('/')
    try:
        parsed = urllib.parse.urlsplit(p['base_url'])
        _ = parsed.port  # validate port syntax
    except ValueError:
        raise ConfigError('Invalid endpoint URL; value hidden') from None
    if parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ConfigError('Use an HTTP(S) base URL without credentials, query, or fragment')
    if any(c.isspace() for c in p['base_url']):
        raise ConfigError('Endpoint URL contains whitespace')
    loopback = parsed.hostname in {'localhost', '127.0.0.1', '::1'}
    if parsed.scheme == 'http' and not loopback and p.get('allow_insecure_http') is not True:
        raise ConfigError('Use HTTPS or a loopback tunnel; trusted HTTP requires allow_insecure_http: true')
    if 'require_api_key' in p and not isinstance(p['require_api_key'], bool):
        raise ConfigError('require_api_key must be a boolean')
    key = variable('api_key_env', p.get('require_api_key', False))
    headers = {'Accept': 'application/json'}
    if key:
        headers['Authorization'] = 'Bearer ' + key
    if not isinstance(p.get('headers_env', {}), dict):
        raise ConfigError('headers_env must be an object of header-to-variable mappings')
    for header, variable_name in p.get('headers_env', {}).items():
        if not re.fullmatch(r'[A-Za-z0-9-]+', header) or header.lower() in {'host', 'content-length', 'connection'}:
            raise ConfigError('Invalid custom header name')
        if not isinstance(variable_name, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', variable_name):
            raise ConfigError('Custom header must reference an environment variable')
        if not env.get(variable_name):
            raise ConfigError('A custom header environment variable is missing')
        headers[header] = env[variable_name]
    if any('\r' in v or '\n' in v for v in headers.values()):
        raise ConfigError('Header values must be single-line')
    p['headers'] = headers
    p['timeout_seconds'] = p.get('timeout_seconds', 60)
    if type(p['timeout_seconds']) not in {int, float} or not 1 <= p['timeout_seconds'] <= 600:
        raise ConfigError('timeout_seconds must be between 1 and 600')
    if p['adapter'].endswith('-chat'):
        p['model'] = variable('model_env', True)
        p['max_output_tokens'] = p.get('max_output_tokens', 512)
        if type(p['max_output_tokens']) is not int or not 1 <= p['max_output_tokens'] <= 32768:
            raise ConfigError('max_output_tokens must be between 1 and 32768')
        if p.get('token_limit_field', 'max_tokens') not in {'max_tokens', 'max_completion_tokens'}:
            raise ConfigError('Unsupported token_limit_field')
    return p


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(profile, suffix, body=None):
    # Do not silently forward credentials to a redirected origin or ambient proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    headers = dict(profile['headers'])
    data = None
    if body is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(body).encode()
    req = urllib.request.Request(profile['base_url'] + suffix, data=data, headers=headers)
    try:
        with opener.open(req, timeout=profile['timeout_seconds']) as response:
            raw = response.read(8 * 1024 * 1024 + 1)
            if len(raw) > 8 * 1024 * 1024:
                raise ConfigError('Response exceeds 8 MiB; inspect with the provider UI')
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        # Error bodies/URLs may echo keys, prompts, or personal server information.
        code = e.code
        e.close()
        raise ConfigError(f'Provider returned HTTP {code}; response body hidden. No automatic retry.') from None
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError):
        raise ConfigError('Connection failed or timed out; details hidden. Request may have reached provider; check before retrying.') from None
    except (json.JSONDecodeError, UnicodeError):
        raise ConfigError('Provider did not return valid JSON; response hidden') from None


def chat(profile, prompt):
    if profile['adapter'] not in {'openai-chat', 'ollama-chat'}:
        raise ConfigError('Select a chat profile')
    body = {'model': profile['model'], 'messages': [{'role': 'user', 'content': prompt}], 'stream': False}
    if profile['adapter'] == 'openai-chat':
        body[profile.get('token_limit_field', 'max_tokens')] = profile['max_output_tokens']
        result = request_json(profile, '/chat/completions', body)
        try:
            content = result['choices'][0]['message']['content']
        except (KeyError, TypeError, IndexError):
            raise ConfigError('No Chat Completions text response; inspect adapter/model support') from None
    else:
        body['options'] = {'num_predict': profile['max_output_tokens']}
        result = request_json(profile, '/api/chat', body)
        try:
            content = result['message']['content']
        except (KeyError, TypeError):
            raise ConfigError('No Ollama text response; inspect adapter/model support') from None
    if not isinstance(content, str) or not content.strip():
        raise ConfigError('No visible text returned; model may need a larger budget or different configuration')
    return content


def probe(profile):
    adapter = profile['adapter']
    if adapter == 'manual':
        return {'adapter': adapter, 'status': 'manual handoff; no request sent'}
    suffix = {'openai-chat': '/models', 'ollama-chat': '/api/tags', 'comfyui': '/system_stats'}[adapter]
    result = request_json(profile, suffix)
    if not isinstance(result, dict):
        raise ConfigError('Unexpected provider response shape')
    if adapter in {'openai-chat', 'ollama-chat'}:
        models = result.get('data' if adapter == 'openai-chat' else 'models')
        if not isinstance(models, list):
            raise ConfigError('Model listing unsupported; chat may still work with an exact model ID')
        return {'adapter': adapter, 'status': 'model list reachable; generation untested', 'model_count': len(models)}
    if not isinstance(result.get('system'), dict):
        raise ConfigError('Unexpected ComfyUI system response')
    return {'adapter': adapter, 'status': 'ComfyUI reachable; workflow untested'}


def validate_graph(graph):
    if not isinstance(graph, dict) or not graph:
        raise ConfigError('Use a nonempty exported ComfyUI API-format graph')
    for node in graph.values():
        if not isinstance(node, dict) or not isinstance(node.get('class_type'), str) or not isinstance(node.get('inputs'), dict):
            raise ConfigError('Use API-format nodes with class_type and inputs, not a UI workflow export')


def submit_workflow(profile, graph):
    if profile['adapter'] != 'comfyui':
        raise ConfigError('Workflow submission requires a ComfyUI profile')
    validate_graph(graph)
    response = request_json(profile, '/prompt', {'prompt': graph, 'client_id': uuid.uuid4().hex})
    if not isinstance(response, dict) or response.get('node_errors') or not isinstance(response.get('prompt_id'), str):
        raise ConfigError('Workflow was not accepted cleanly; inspect the provider UI before retrying')
    return {'status': 'submitted, not rendered or reviewed', 'prompt_id': response['prompt_id']}


def job_status(profile, prompt_id):
    if profile['adapter'] != 'comfyui':
        raise ConfigError('Job status requires a ComfyUI profile')
    response = request_json(profile, '/history/' + urllib.parse.quote(prompt_id, safe=''))
    if not isinstance(response, dict):
        raise ConfigError('Unexpected history response')
    job = response.get(prompt_id)
    if not isinstance(job, dict):
        return {'status': 'not in history; may be queued, running, unknown, or removed'}
    status = job.get('status', {})
    if status.get('status_str') == 'error':
        return {'status': 'failed; inspect provider UI'}
    return {'status': 'completed; media still needs review' if status.get('completed') else 'not completed'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('providers.local.json'))
    parser.add_argument('--env-file', type=Path, default=Path('.env'))
    parser.add_argument('--role', choices=['language', 'media'], default='language')
    parser.add_argument('--profile', help='Explicit profile overrides the selected route')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('check', help='Validate selected profile without network or generation')
    sub.add_parser('probe', help='Read-only network capability check; does not generate')
    c = sub.add_parser('chat', help='Send one prompt (can incur cost) and print model output')
    c.add_argument('--prompt-file', type=Path, required=True)
    c.add_argument('--execute', action='store_true')
    w = sub.add_parser('submit-workflow', help='Submit one user-prepared ComfyUI graph')
    w.add_argument('--workflow', type=Path, required=True)
    w.add_argument('--execute', action='store_true')
    j = sub.add_parser('job-status', help='Read status of a known ComfyUI prompt ID')
    j.add_argument('--prompt-id', required=True)
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        env = load_env(args.env_file)
        profile = resolve_profile(config, env, args.role, args.profile)
        if args.command == 'check':
            result = {'adapter': profile['adapter'], 'status': 'configuration valid; no network request sent'}
        elif args.command == 'probe':
            result = probe(profile)
        elif args.command == 'chat':
            prompt = args.prompt_file.read_text()
            if not prompt.strip():
                raise ConfigError('Prompt file is empty')
            if profile['adapter'] not in {'openai-chat', 'ollama-chat'}:
                raise ConfigError('Select a chat profile')
            if args.execute:
                print(chat(profile, prompt))
                return 0
            result = {'status': 'dry run; add --execute to send prompt', 'adapter': profile['adapter'], 'prompt_characters': len(prompt)}
        elif args.command == 'submit-workflow':
            graph = json.loads(args.workflow.read_text())
            validate_graph(graph)
            if profile['adapter'] != 'comfyui':
                raise ConfigError('Select a ComfyUI profile')
            result = submit_workflow(profile, graph) if args.execute else {'status': 'dry run; add --execute to submit graph', 'node_count': len(graph)}
        else:
            result = job_status(profile, args.prompt_id)
        print(json.dumps(result))
        return 0
    except ConfigError as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, AttributeError):
        print('ERROR: Invalid or unreadable input/configuration; values hidden', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
