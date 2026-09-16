# Validation status

Packaging checks are recorded here after execution. Structural validation is separate from real media quality, remote runtime availability, or harness discovery.

The original packaging tests did not perform AI image or video generation. Existing production workflows have real image, video, Blender and presentation artifacts; see [the evidence review](WORKFLOW-EVIDENCE.md). Execution of the bundled Blender starter and full cross-harness behavioral testing are not certified. See the final recorded checks below.

## Executed checks — September 15, 2026

- All eight skills passed the skill-creator frontmatter validator.
- Package validator passed: metadata, relative Markdown links, JSON, Python syntax, and configured private-data patterns. This is a bounded scan, not a comprehensive secret audit.
- Installer copied the complete collection to isolated Codex, Claude Code, and Copilot project layouts. A repeat install refused to overwrite the existing skills. Agent discovery inside those three products was not exercised.
- Bundled Scroll World JavaScript passed Node syntax checking.
- FFmpeg produced two real four-second synthetic diagnostic clips; these are not AI-generated quality samples.
- Playwright/Chromium loaded both demo clips with no page JavaScript exceptions. At 1440×900, forward scroll moved the first clip to 1.345504 s, stopping held that exact time, and reverse scroll returned to 0.340480 s. Desktop and 600×800 screenshots were inspected. Seam, keyboard, reduced-motion, Safari, and physical-phone checks remain unverified.
- The requested agent-browser executable was unavailable; the browser check used the already-installed Playwright runtime instead.
- Remotion 4.0.518 dependencies installed with a lockfile and zero reported npm audit findings at installation time. The starter rendered a still and complete MP4; the still was visually inspected. ffprobe reported 1280×720, 24 fps, and approximately 12.05 seconds. Full playback and audio review were not performed.
- Blender starter was syntax checked but not executed in Blender. Remote local-AI and paid-cloud generation were not run.

These checks establish a working package and bounded examples. They do not establish production-ready generated media, a configured recipient GPU, or universal harness compatibility.

## Portable-provider revision — September 15, 2026

- Renamed all eight skills by capability and updated references and the demo's engine import. All skill frontmatter validators passed.
- Added private environment/profile templates and a standard-library client for OpenAI-compatible text, native Ollama text, self-hosted ComfyUI, and manual handoff.
- The protocol/privacy test suite exercises fake loopback services, request shapes, bearer authentication, dry runs, redirects, redacted errors, malformed responses, API graph validation, job status, and installation without private configuration. No real model or paid endpoint is used by these tests.
- Distribution validation checks Git-visible files and excludes ignored personal files. It flags personal home paths, non-loopback IP literals, selected token/private-key patterns, credential-bearing URLs, and tracked personal configuration/model files. It reports categories, not matched secret values. This is a bounded scan, not proof that every possible secret format can be detected.
- Private source-path, personal-name, and machine-context references were removed from current distributed content. Upstream license attribution and organizational ownership remain.
- New client protocol behavior is mock-tested; real provider compatibility, generated-media quality, and coding-harness model configuration remain environment-specific and unverified.

## Prior subagent media trial — September 15, 2026

A fictional pilot-planning brief produced SVG storyboard sketches, an interactive HTML presentation, and a 30-second Remotion motion-graphics MP4. These are planning, presentation, and composition results. **They are not AI-generated photographic images or generative-video footage.** The trial used mock provider responses; it did not qualify a real inference server. Local trial files and system-generated narration are not included in the public package.

## Public-release media trial — September 16, 2026

The built-in cloud image tool generated the [Pilot Lab still](../examples/generated-media/README.md) from a synthetic prompt, with no private source inputs. The original 1672 × 941 PNG was visually inspected and copied without modification. The provider did not return model, seed, or cost information. This verifies one cloud image-generation/manual-import path, not the generic client or a recipient's harness. A new AI-video trial through this portable package remains pending an available media service; historical local AI-video generation is established by the separate evidence review.

Release-preparation checks passed: all 19 unit tests, distribution validation, and a fresh Codex-layout installation. The provider tests required permission to bind a temporary loopback server; they still used simulated inference only. The new binary guard rejects an altered sample and an unapproved binary path.

## Fresh local video and branded presentation trial

An independent agent passed all eight structural skill checks and all 19 unit tests. A new local text-to-video trial then produced three original four-second clips (512 × 288, 97 frames, 24 fps) with an installed LTX 2.5 runtime. Total submission/poll/download wall time was 345.91 seconds. Queue and node/model inventory were checked first; clips were generated sequentially and contact sheets inspected. No cloud generation was used, although planning and coding used cloud assistants.

The generic client accepted the graph in dry-run mode. A runtime-specific driver handled actual submission, polling and download; this does not qualify the bundled client end-to-end, image conditioning, or another device.

A ten-beat website-branded HTML presentation integrates the three clips with editable copy, speaker notes and a static leave-behind. Browser checks covered desktop/mobile layout, all-beat navigation, direct links, notes, video loading/playback and pause on exit. One in-app preview tab crashed; a fresh tab played the same clip successfully. Reduced-motion/print styles were source-reviewed only. Original trial files remain outside the public distribution.

The trial added reusable website-brand capture guidance and explicit live-runtime qualification to the skills. Preview-resolution B-roll is not a production-quality or technical-accuracy certification.

## Public preview packaging

All 20 tests passed, including integrity checks for every explicitly reviewed binary asset. The public showcase contains the validated presentation and three local clips. Font licenses and logo rights are recorded alongside the assets. A fresh repository snapshot keeps earlier private history and runtime records outside the public repository.
