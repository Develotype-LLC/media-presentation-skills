---
name: configure-ai-providers
description: Connect text inference and image/video generation to user-selected local or cloud services using private environment files and provider profiles.
---

# Configure AI providers

Read [provider setup](references/PROVIDERS.md) when connecting or switching an endpoint. The bundled client, examples, and documentation remain usable after this entire skill folder is installed into another project.

1. Identify the job: text planning, image/video generation, or both. Select language and media profiles independently. Ask for the user's service choice only when it is missing; use the existing approved choice otherwise.
2. Copy the provided templates into the working project as `.env` and `providers.local.json`. Keep values and credentials private, with environment-variable names in the profile. The user fills their own credentials outside shared agent transcripts. Never dump `.env`, headers, raw provider errors, or private endpoints into reports.
3. Validate only the selected profile with `scripts/ai_client.py check`. Use `probe` for a read-only connectivity check. Neither proves generation quality. Do not change the coding harness's model configuration: the helper's provider routing is separate.
4. For language inference use an exact model ID with OpenAI-compatible Chat Completions or native Ollama. This client performs one text request; it is not an agent loop, tool executor, vision client, or universal provider SDK.
5. For ComfyUI use an API-format graph exported from the target installation. Match its nodes, models, and input files to that installation. Dry-run then submit one bounded job within the user's authorization. Record the prompt ID and inspect the actual output in the operator's UI or authorized storage.
6. For a cloud media service without a supported adapter, use the manual prompt/download handoff from `generate-image-and-video`. Do not route media through a text endpoint or silently move a failed local job to cloud.

Your mileage will vary across models and runtimes: endpoint compatibility does not establish vision, tool use, context capacity, instruction-following quality, precise motion, or render speed. Run a small representative trial before a batch and report configured, observed, and untested capabilities separately.

For local hardware, inspect device identity, memory budgets, installed models, and current queue before generation. Preserve other workloads and managed resource limits. This skill does not provision machines or embed a personal host profile.
