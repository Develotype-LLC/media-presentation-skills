# Tools and execution routes

| Need | Starting point | Boundary |
|---|---|---|
| Cloud still/video generation | [Higgsfield](https://higgsfield.ai/) | Check current features, price, data terms, and account access; no bundled CLI/MCP integration |
| Local generation | [ComfyUI](https://github.com/Comfy-Org/ComfyUI) | Requires compatible nodes, models, hardware, and workflow |
| Local language model | [llama.cpp](https://github.com/ggml-org/llama.cpp) | Configure your harness separately; rendering locally does not localize its prompts |
| Controlled 3D | [Blender](https://www.blender.org/) | Inspect geometry and renders; no technical validation implied |
| Exact text and timed assembly | [Remotion](https://www.remotion.dev/docs) | Check its own license and installed versions |
| Media encoding / inspection | [FFmpeg](https://ffmpeg.org/) | Preserve originals and record output parameters |
| Scroll camera interface | [Scroll World](https://github.com/oso95/scroll-world) | MIT notice retained for bundled engine |

Local costs include hardware, electricity, setup, and render time. “No API credits” does not mean free. Do not carry over performance numbers from an old workstation snapshot.

## Provider configuration

[Provider setup](../skills/configure-ai-providers/references/PROVIDERS.md) is the canonical guide for `.env`, `providers.local.json`, adapters, routes, authentication, dry runs, and connection checks. Text and media endpoints are independent. The language client accepts OpenAI-compatible Chat Completions and native Ollama; other protocols need an adapter or gateway. ComfyUI receives a user-supplied API graph, with no fixed model or hardware selection. Mileage varies by endpoint, model, and workflow.

## Capability record

For each backend record: endpoint alias (no secrets), OS, GPU identities, software versions, workflow hash, installed model/adapter files, allowed input classification, output rights, and a measured still/clip trial. Label each feature configured, observed, or untested. For cloud record quoted and actual cost; for local record wall-clock time and resource limits.

## Local setup

Read [the runtime reference](../skills/configure-ai-providers/references/setup.md). Install ComfyUI following its current platform instructions, add models and nodes for one chosen official workflow, and export that working workflow in API format. Reuse that graph instead of guessing node names. This toolkit deliberately does not redistribute weights or silently install drivers.

LTX and Wan are candidate model families from the reviewed workflows, not universal defaults. Validate exact installed revisions, frame constraints, and adapter compatibility. Restricted/noncommercial adapters must not be assumed usable in client work. Cloud and local versions of similarly named products may have different capabilities and licenses.
