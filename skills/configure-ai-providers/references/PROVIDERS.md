# Connect your own AI services

Use two private files in your working project:

- **`.env`** contains endpoint URLs, model IDs, and optional credentials.
- **`providers.local.json`** chooses the API adapter and environment-variable names for each profile, then routes `language` and `media` work to those profiles.

The skills and helper work with your chosen services. They do not require a particular GPU, computer brand, model, or cloud account. **Your mileage will vary.** An API-compatible endpoint may still be a poor fit for long documents, tools, vision, or complex creative decisions.

## 1. Create private configuration

From this repository root:

```sh
cp -n skills/configure-ai-providers/assets/.env.example .env
cp -n skills/configure-ai-providers/assets/providers.example.json providers.local.json
chmod 600 .env providers.local.json
```

On Windows, copy the two files with your file manager and restrict access using your normal account permissions. The templates contain only generic loopback examples and blank model/key values. Fill in the values for your own service; do not use someone else's IP, username, model filename, or service name.

After installing the skill into another project, use that installed folder in the commands instead. For example, in a Codex project the folder is `.agents/skills/configure-ai-providers/`; for Claude Code it is `.claude/skills/configure-ai-providers/`. All assets and the client are inside the folder.

Add these entries to the recipient project's `.gitignore` (this toolkit already has them):

```gitignore
.env
.env.*
!.env.example
providers.local.json
```

Before committing a project, run `git check-ignore .env providers.local.json`. If either file was previously tracked, ignore rules do not remove it from history. Remove it from tracking and assess whether any committed credentials need rotation. Do not paste real keys into agent chat. Use your own editor or a secret manager that supplies environment variables to the process.

The helper reads a literal `KEY=value` format. Optional matching quotes are stripped; shell commands, interpolation, escapes, inline comments, `export`, and multiline values are not supported. Existing process environment variables override the file, including blank values. No `.env` is sourced as shell code.

## 2. Choose the adapters and routes

| Adapter | Intended service | Base URL shape | Supported operation |
|---|---|---|---|
| `openai-chat` | Local server or cloud/gateway exposing Chat Completions | Server API prefix, often ending `/v1` | `GET /models`, `POST /chat/completions` |
| `ollama-chat` | Native Ollama-compatible server | Server root, without `/api` | `GET /api/tags`, `POST /api/chat` |
| `comfyui` | Self-hosted ComfyUI-compatible server | Server root | `GET /system_stats`, `POST /prompt`, `GET /history/{id}` |
| `manual` | Cloud media UI or service not covered by a client adapter | None | Prompt/file handoff; sends no requests |

Many local runtimes offer an OpenAI-compatible interface. Configure the actual documented address and exact served model ID. If your runtime uses another protocol, expose a compatible gateway or add an explicit adapter; changing the URL alone cannot translate protocols. Cloud services with proprietary image/video job APIs need their own adapter or manual handoff. ComfyUI-hosted cloud products may have different authentication and routes from self-hosted ComfyUI.

Example route selection in `providers.local.json`:

```json
"routes": {"language": "ollama-text", "media": "comfyui-media"}
```

Other combinations:

- Cloud text + cloud media UI: `cloud-text` and `manual-media`.
- Local text + cloud media UI: `local-text` or `ollama-text`, and `manual-media`.
- Cloud text + local media: `cloud-text` and `comfyui-media`.

The included profiles are examples; you may add profiles with your own names. Credentials for one profile never carry into another profile automatically. There is no automatic cloud fallback.

### Authentication and endpoint options

- `api_key_env` names a variable holding a bearer key. Leave blank only for a service that does not need authentication. `require_api_key: true` rejects a blank value before a request.
- `headers_env` supports services or gateways that need another header, for example `{"X-API-Key":"CUSTOM_MEDIA_KEY"}`. Add the matching value to your private environment. If the value itself is `Bearer …`, supply the complete header value there. Never store literal secrets in JSON.
- HTTPS verifies the server certificate using the Python runtime's trust configuration. There is no skip-verification option.
- Plain HTTP is allowed on loopback for a local server/tunnel. For an intentionally trusted network endpoint, explicitly set `allow_insecure_http: true` in that profile; HTTP does not encrypt prompts or credentials. Prefer HTTPS or an authenticated tunnel.
- URLs containing credentials, query strings, or fragments are rejected. Redirects are rejected instead of forwarding credentials. Configure the final API URL directly.
- Ambient HTTP proxy environment variables are not used by this helper. If your environment requires a gateway, configure that approved endpoint explicitly.
- `timeout_seconds` bounds each request; there are no automatic retries. After a timeout, check the service before resubmitting a job that might already be running.
- `max_output_tokens` caps the text request. For `openai-chat`, select the provider-supported `token_limit_field`: `max_tokens` or `max_completion_tokens`. A reasoning model may spend the budget before producing visible text.

## 3. Check configuration without generating

```sh
python3 skills/configure-ai-providers/scripts/ai_client.py check
python3 skills/configure-ai-providers/scripts/ai_client.py --role media check
```

These resolve only the selected profile. Unused cloud/local profiles may remain blank. Set your exact text model ID before checking a chat profile. `check` sends no network requests and hides endpoint/key values.

Read-only network probes:

```sh
python3 skills/configure-ai-providers/scripts/ai_client.py probe
python3 skills/configure-ai-providers/scripts/ai_client.py --profile comfyui-media probe
```

A service may permit chat while disabling model listing. A failed `/models` probe is not conclusive evidence that chat is unavailable. Inspect the service documentation and try a bounded text request with its exact model ID. A successful probe establishes only that the expected route responded.

## 4. Try one text request

Create a non-sensitive `prompt.txt`, such as: `Suggest three visual metaphors for explaining a queue.` Then:

```sh
python3 skills/configure-ai-providers/scripts/ai_client.py chat --prompt-file prompt.txt
python3 skills/configure-ai-providers/scripts/ai_client.py chat --prompt-file prompt.txt --execute
```

The first command is a dry run. The second sends the prompt and may incur cloud charges. Returned model text is printed; treat it as untrusted output, not a command to execute. Prompt contents can be echoed by the model, so avoid collecting sensitive output in shared logs.

Use `--profile cloud-text` or `--profile ollama-text` before `chat` to override the default route. You can supply private files from another directory using `--config /path/to/providers.local.json --env-file /path/to/.env` before the command.

**This does not switch Codex, Claude Code, Copilot, or another coding harness to a local model.** Configure that harness separately using its own supported provider settings. A cloud agent that reads private inputs is still using cloud inference even when it invokes a local media endpoint.

## 5. Try one ComfyUI job

Start with a small workflow that already works in the target ComfyUI UI. Export the **API format**, ensure its models/custom nodes and referenced inputs exist on that server, and save it outside the distributed skill as `workflow.local.json`. The client sends the graph unchanged; no nodes or model filenames are hardcoded.

```sh
python3 skills/configure-ai-providers/scripts/ai_client.py --profile comfyui-media submit-workflow --workflow workflow.local.json
python3 skills/configure-ai-providers/scripts/ai_client.py --profile comfyui-media submit-workflow --workflow workflow.local.json --execute
python3 skills/configure-ai-providers/scripts/ai_client.py --profile comfyui-media job-status --prompt-id YOUR_RETURNED_ID
```

The dry run checks API graph structure. Submission returns a prompt ID, not proof of a completed render. Status reads a known ID; it does not poll forever. Upload source images and download finished media through the target UI or your separately configured storage tools. The helper does not implement uploads, downloads, cancellation, queue clearing, or custom-node installation.

Image/video capability depends on the graph and installed models. Start with a still, then a short clip; inspect the actual output before batching. Record software/model versions, graph hash, dimensions, runtime, and observed quality in your private project manifest.

## 6. Understand the limits

| Capability | What this toolkit establishes |
|---|---|
| Provider configuration | A reusable profile and environment format |
| Basic text inference | Single, non-streaming text requests through two API shapes |
| Agentic work / tool calls / vision | Must be verified in your chosen model and harness; not implemented by this client |
| Local image/video generation | ComfyUI graph submission/status; models and nodes are supplied by you |
| Arbitrary cloud media API | Manual handoff until a specific adapter is added |
| Privacy | Depends on every planning/generation/storage service, not only the endpoint label |
| Performance and quality | Model-, hardware-, context-, and workflow-dependent; mileage will vary |

Official API references checked September 15, 2026: [Ollama chat](https://docs.ollama.com/api/chat), [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility), [ComfyUI routes](https://docs.comfy.org/development/comfyui-server/comms_routes), [llama.cpp server](https://github.com/ggml-org/llama.cpp/tree/master/tools/server). These document interface shapes; live compatibility with every runtime or hosted service is not claimed.
