---
name: compose-video
description: Assemble video, accurate text and data overlays, captions, and independently editable narration with Remotion.
---

# Remotion composition

Use the approved beat list and clean media. Verify installed Remotion/React versions against the project lockfile. For a new project, use the repository starter under `examples/remotion` or the current official initializer; do not assume a global CLI.

Define fps, dimensions, duration, and beat start frames explicitly. Drive all motion from frame time, not wall-clock timers or random values. Use one data source for exact copy and quantities; preserve source/assumption labels. Avoid baked-in words from AI footage.

Keep separate tracks for clean footage, overlays, narration, captions, and music. Narration takes must be replaceable per beat. Preserve clean masters as well as the composite. Check text contrast, safe areas, clipping, caption timing, and audio intelligibility.

Render representative frames at transitions and densest text, then a short MP4. Inspect actual playback and metadata. Verify that replacing a narration take or changing an overlay does not require regenerating the background footage. Track whether missing footage has been temporarily replaced by a still or motion graphic.

Deliver composition source, pinned dependencies/lockfile, render command, input manifest, final MP4, captions if requested, and QA notes. Check the current Remotion license for the intended organization/use; this skill repository's license does not license Remotion itself.
