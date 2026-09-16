---
name: generate-image-and-video
description: Generate coherent stills and short video shots using a chosen local or cloud provider, with reviewed concepts and recorded provenance.
---

# AI shot production

Use the selected brief and beat IDs. Keep one style preamble, aspect ratio, persistent subject description, and lighting plan across related shots. Separate atmosphere from evidence: generated scenery cannot substantiate a product claim or technical mechanism.

For endpoint configuration, read the sibling `configure-ai-providers` skill and use the selected media profile.

For local jobs, qualify the runtime before batching: inspect the live queue, installed model names and node input contracts through the authorized media API. A historical working graph may target models that are no longer installed. Adapt only to verified compatible components, record the change, and prove one bounded output before scaling. Media-job access and host-administration access are separate capabilities; use an existing authorized media API without assuming permission to change services or credentials.

For cloud jobs, verify the provider's current UI/API capabilities, upload scope, output rights, and cost before the first paid batch. Higgsfield is an optional provider, not an assumed installed MCP or CLI. Use available documented tooling; do not invent commands or silently switch providers.

1. For image-to-video, make a small still batch with deliberate concept differences. For a text-to-video runtime probe, use one bounded shot and record that no still conditioning was tested. Save prompt, seed if supported, model/adapter version, dimensions, provider, and asset ID.
2. Review subject recognition, consistency, room for text, and misleading details. Preserve rejection reasons. Generate image-conditioned video from selected stills; review the first text-to-video output before producing related shots.
3. Measure one bounded shot before estimating the batch. Set attempt, time, and money limits. Serialize shared GPU jobs unless the operator has validated concurrency.
4. Inspect the opening, middle, ending, and real playback. Check morphing, identity, camera direction, flicker, unwanted text, and duration. Prompted motion is not guaranteed camera control.
5. For continuous scroll sequences, read `build-scroll-video` before choosing a model: actual endpoint conditioning and continuity matter more than attractive isolated clips.

Keep exact words, numbers, labels, and charts in editable overlays. Narration is its own asset per beat; use an authorized voice and keep replacement takes. Preserve clean clips. Document any still-only fallback as incomplete video work.

Deliver clean media, settings and job IDs, contact sheet, actual generation cost/time, and review decisions. Do not publish or send the output unless included in the user's request.
