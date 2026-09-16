# Getting started

The goal is to make a clear, distinctive 30–60 second explanation or a touchable presentation you can reuse for portfolio companies. Your judgment about the story matters more than the choice of generator.

## Start here: cloud AI, no local AI server

Use this route if you have a coding assistant and want a cloud service to generate the imagery. You do **not** need specialized hardware, local models, ComfyUI, or personal scripts.

**Cloud AI generation is different from running everything in the cloud.** Your coding assistant can use a cloud model, your media service can generate the shots remotely, and Remotion can still assemble the video on your ordinary computer. The included examples use local Python/Node/browser tools. A completely browser-only production setup is not bundled here.

### Step 1 — Install the skills into your working project

Follow [installation](INSTALL.md) for your coding assistant. Installing all eight skills is fine: it does not install or activate local AI. Tell the assistant to use the cloud route. Use `configure-ai-providers` when you want to connect a text or media endpoint.

If you only use a browser chat, you can provide the relevant `SKILL.md` files as instructions and obtain plans and prompts. Automatic project editing, rendering, and provider access still require tools available in that chat; the repository does not add those capabilities by itself.

### Step 2 — Plan before buying generation

Use `plan-media-story`, plus `convert-deck-to-media` if you have a deck. Supply your audience, message, source material, and target length. Ask for a few concepts and select one. The copyable first-project request below is a starting point.

### Step 3 — Generate stills with your cloud service

Choose a service/account you can use, such as [Higgsfield](https://higgsfield.ai/). Check its current capabilities and budget in that account. Ask:

> Use generate-image-and-video with my chosen cloud provider. Use my chosen cloud service for generation. Produce one still-image prompt per beat, with a consistent style and subject description. Leave exact text out of the generated images. My generation budget is [amount]. If you cannot access the provider, give me prompts and a file naming checklist so I can generate and download the images myself.

The reliable starting path is manual: paste the prompts into the provider, generate stills, download them to your project, and have the assistant review the actual files. For example, use `assets/stills/B01-v001.png` and record the settings in the [asset manifest](../examples/story-kit/asset-manifest.json).

**This repository contains workflow skills, not a working Higgsfield API/MCP adapter.** An installed, authenticated integration may automate the handoff; otherwise use the manual path. Installing the skills alone does not connect your paid account.

### Step 4 — Animate only the selected stills

Use the provider’s supported image-to-video workflow if available. Ask the assistant for a motion prompt per selected scene. Download clips as, for example, `assets/video/B01-v001.mp4`. Return those files to the assistant for motion, identity, and continuity review. Keep unsuccessful takes and their rejection reasons.

For a first video, independent short shots are sufficient. A continuous Scroll World has extra requirements: adjacent endpoint frames and the camera journey must match. If the provider cannot support the required control, use deliberate transitions or an interactive presentation and document the change.

### Step 5 — Assemble the chosen output

- **MP4:** use `compose-video` with downloaded cloud clips. Node and Remotion run in your working environment; no local AI model or dedicated GPU server is needed. Start with the [Remotion example](../examples/remotion/README.md).
- **Scroll-controlled website:** use `build-scroll-video` with reviewed, compatible clips. Start with the [interaction demo](../examples/scroll-demo/README.md), then replace diagnostic media with your shots.
- **Presenter-led interactive story:** use `build-interactive-presentation` with the downloaded clips, editable labels, and optional narration.
- **Precise 3D mechanism:** add `create-3d-explainer` when geometry matters. Blender is a separate renderer, not a local language or diffusion model; it is optional for the cloud-generated video route.

Ask the assistant to inspect the actual finished output and deliver the editable project. Keep captions, exact numbers, and narration separate from the generated footage.

## Which skills need local AI?

“Cloud route” below means cloud AI generates the imagery; ordinary editing/rendering software may still run on your computer.

| Distributed skill | Works on the cloud route? | Works with local AI? | What it actually needs |
|---|---|---|---|
| `plan-media-story` | Yes | Yes | Assistant + brief/source material |
| `convert-deck-to-media` | Yes | Yes | Assistant with access to the deck and extraction tools |
| `generate-image-and-video` | Yes | Yes | Chosen cloud service **or** configured local generation backend |
| `configure-ai-providers` | Yes | Yes | Your provider profiles; local setup only when you select a local service |
| `build-scroll-video` | Yes | Yes | Compatible video assets + browser/web tools; generation is separate |
| `create-3d-explainer` | Yes, as an optional production step | Yes | Blender runtime; no local AI model required |
| `compose-video` | Yes | Yes | Node/Remotion + media; no local AI model required |
| `build-interactive-presentation` | Yes | Yes | Web project tools + browser + media |

For the first cloud project, start with **plan-media-story → generate-image-and-video → compose-video**. Add `convert-deck-to-media` only when converting a deck. Skip local-server setup for this route.

## Configure your own services

Follow [provider setup](../skills/configure-ai-providers/references/PROVIDERS.md) to create a private `.env` and `providers.local.json`. Set the language and media routes independently: a local language model can plan a project whose images come from a cloud service, or a cloud assistant can work with locally rendered media.

For text inference, the bundled client supports OpenAI-compatible Chat Completions and native Ollama chat. For media it supports self-hosted ComfyUI API graphs, plus a manual handoff to cloud services. Other protocols need a compatible gateway or a provider adapter. **Your mileage will vary:** a reachable endpoint does not prove good reasoning, vision, tool use, or video-generation quality.

## Five building blocks

1. **A coding assistant** reads the source and builds the presentation.
2. **The planning skills** turn a message into concepts and short scenes.
3. **A media generator** creates stills and then selected shots; Higgsfield is one cloud option, ComfyUI is a local option.
4. **Blender and/or Remotion** supply controlled geometry and accurate editable overlays.
5. **The browser or MP4** is the delivery surface; Scroll World makes scrolling control the camera.

You can begin with your current assistant and these skills. A local AI server is optional.

## First project: why AI initiatives get stuck

Use a public or synthetic deck. Aim for a 45-second pilot, not a full campaign. Four themes from the workflow discussion are talent, choosing the right problems, speed, and governance. Treat them as the proposed narrative, not as universally established claims about every company.

Copy this request into your coding assistant after [installing](INSTALL.md):

> Use plan-media-story and convert-deck-to-media. Help me make a 45-second explainer for portfolio-company leaders using my supplied deck. Preserve the source claims and flag missing evidence. Pitch three visual concepts that show how talent, prioritization, speed, and governance affect delivery. Avoid generic floating dashboards. For each concept describe what the viewer sees and why it helps. Start with a storyboard and still plan. My first output is an MP4, with an interactive version as a later option. Ask for my cloud provider and budget before paid generation.

Choose or combine concepts. Give feedback such as “the bottleneck is clear, but this looks too industrial” or “keep that camera reveal; simplify the props.” Reject weak concepts early.

## A suggested 45-second beat plan

| Time | Meaning | Visual proposal | Method |
|---|---|---|---|
| 0–7 s | There is a promising idea | A single object enters a delivery path | AI shot or Blender |
| 7–16 s | Skills and problem choice shape progress | Wrong tools / unclear fork in the path | Controlled reveal |
| 16–26 s | Delays accumulate | A visible queue of unfinished work | Blender or native animation |
| 26–37 s | Guardrails allow movement | A clear guided route replaces ambiguous turns | Blender + overlays |
| 37–45 s | Choose one bounded pilot | One route and one clear next step | Remotion text + clean footage |

This is a proposed metaphor with no performance statistics. Keep the imagery sophisticated and simple; no particular claymation or cartoon style is required.

## What to ask for at handoff

- The editable story and individual scenes, not only a flattened video.
- Clean clips, separate narration takes, exact overlays, and source notes.
- Actual cost/time and the prompts/settings that produced selected shots.
- Playback on your intended device and a readable leave-behind.

For a zero-provider first look, run the [scroll interaction demo](../examples/scroll-demo/README.md). Its synthetic footage only demonstrates the control mechanic. For real cloud imagery, start at [Higgsfield](https://higgsfield.ai/) and verify current account capabilities and pricing; old conversation prices are not a quote.

## Definition of a successful first pilot

An unfamiliar viewer can explain the point after one viewing; the metaphor does not invent evidence; text is readable; footage moves intentionally; narration can be changed without regenerating scenes; and you can reproduce the result from the saved project.

Use this guide with your own source material, accounts, and approved execution environment.
