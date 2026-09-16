# Media & Presentation Skills

A portable toolkit for turning an idea or deck into a useful video, scroll world, or interactive presentation—with local AI, cloud AI, Blender, and Remotion.

**Start with the message. Review concepts. Produce the selected shots. Keep the story editable.**

**Release status: early preview.** See the [release checklist](docs/RELEASE.md) for tested capabilities and remaining gates.

By [Develotype](https://develotype.com). Start with [the cloud-AI walkthrough and skill compatibility table](docs/GETTING-STARTED.md), then [installation](docs/INSTALL.md). No local AI server is required for the cloud route.

## See it working

[![Locally generated video in the Develotype presentation](examples/showcase/poster.jpg)](https://develotype-llc.github.io/media-presentation-skills/examples/showcase/presentation/)

**[Open the live presentation →](https://develotype-llc.github.io/media-presentation-skills/examples/showcase/presentation/)** · [Source and results](examples/showcase/README.md) · [Cloud-generated image example](examples/generated-media/README.md)

A complete ten-section presentation with three real locally generated video clips, editable notes and a static leave-behind. The trial produced its clips in **5m46s** total. Video is preview resolution (512 × 288); timing is one observed run, not a hardware promise. **20 tests pass.** See [exact validation boundaries](docs/VALIDATION.md).

## What is included

| Skill | Job |
|---|---|
| plan-media-story | Audience, message, concepts, storyboard, tool choice |
| convert-deck-to-media | Source-faithful deck ingestion and adaptation |
| generate-image-and-video | Still review, local/cloud shots, provenance |
| configure-ai-providers | Connect text and media providers through portable profiles |
| build-scroll-video | Fixed-stage reversible camera journeys |
| create-3d-explainer | Precise spatial reveals and editable geometry |
| compose-video | Accurate overlays, timing, narration, MP4 assembly |
| build-interactive-presentation | Beat navigation and selectable narration |

These are reusable agent instructions plus starter assets and utilities. They do not install GPU drivers, models, paid subscriptions, or proprietary connectors.

## Quick start

```sh
git clone https://github.com/Develotype-LLC/media-presentation-skills.git
cd media-presentation-skills
python3 scripts/validate.py
python3 scripts/install.py --harness codex --project /path/to/your-project
```

Then ask your agent: “Use plan-media-story to turn my idea into a 45-second explainer. Give me three visual concepts before rendering. My audience is portfolio-company leaders; my message is that AI delivery needs talent, prioritization, speed, and governance. Use illustrative examples, no invented performance claims.”

No GPU or paid service is needed to plan a story or run the [synthetic scroll demo](examples/scroll-demo/README.md). Actual AI generation needs a configured provider. The [Remotion starter](examples/remotion/README.md) and [Blender starter](examples/blender/README.md) show editable output structures.

## Routes

- **Cloud:** coding assistant + selected media service → review → Remotion/HTML.
- **Local:** local assistant + local ComfyUI → review → Blender/Remotion/HTML.
- **Hybrid:** sanitized creative brief to cloud; approved local sources and exact overlays remain local.

See [tools and runtime](docs/TOOLS.md), [workflow provenance](docs/SOURCE-REVIEW.md), [validation status](docs/VALIDATION.md), and [contributing](CONTRIBUTING.md).

## Point the toolkit at your own AI

Follow [provider setup](skills/configure-ai-providers/references/PROVIDERS.md) to copy the example `.env` and provider file, then select your language and media services. The real files stay ignored by Git.

- **Text:** OpenAI-compatible Chat Completions or native Ollama; local servers or compatible cloud gateways.
- **Media:** your self-hosted ComfyUI API graph, or manual prompt/download handoff for cloud services.
- **Other APIs:** use a compatible gateway or implement an adapter. No automatic provider switching.

The bundled Python client validates configuration, probes services, sends one test prompt, and submits/checks ComfyUI jobs. No GPU brand or model is hardcoded. **Your mileage will vary:** interface compatibility does not guarantee model quality, vision, tool use, or video performance. It does not reconfigure your coding harness's own model.

## Distribution

See [personal configuration and sharing checks](docs/PRIVACY.md).

All skills use plain `SKILL.md` folders. Codex, Claude Code, and Copilot installation targets are supplied, with a manual path for other harnesses. Installing instructions does not give a harness unavailable tools or make a cloud session local. Compatibility claims and test limits are in the installation guide.

Original toolkit content is MIT licensed. The bundled Scroll World engine retains its upstream notice. Models, adapters, fonts, provider services, and Remotion have separate terms; no model weights, private source decks, transcript, voice samples, or customer media are bundled.

## Start a production folder

Copy [the story kit](examples/story-kit/brief.md), [beat table](examples/story-kit/beats.csv), and [asset manifest](examples/story-kit/asset-manifest.json) into your project. Fill them as work proceeds; keep generated files and private source material in that project rather than this skill repository.

For existing installations, see [renamed skills and migration](docs/SKILL-NAMES.md).
