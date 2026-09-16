---
name: build-scroll-video
description: Build a scroll-controlled camera journey with a fixed world stage, reversible video scrubbing, and editable text overlays.
---

# Scroll world

The viewport is a fixed window into a world. Scrolling moves the camera; stopping freezes it; reverse scroll retraces it. Keep copy and navigation in lightweight fixed overlays. A long document with background video is a different product.

Define a world bible: terrain, landmarks, adjacency, subject scale, entry/exit vectors, and camera height. Choose between:
- Continuous flight: each leg starts from the previous rendered leg's extracted last frame. Inspect each handoff before proceeding.
- Dive/connect: independently framed scenes linked by connectors conditioned on the actual last and first rendered frames of their neighbors.
- Anchored companion: independent shots deliberately transitioned to preserve deck meaning. Name this tradeoff; it does not establish continuous flight.

Endpoint conditioning can still miss. Inspect both forward and reverse seams; a crossfade cannot repair a large content jump. Longer chains can accumulate visual drift. Run a low-cost sequence proof before the full batch and switch architecture openly if needed.

Use the bundled `references/scrub-engine.js` as the starting engine; its header documents configuration. It is adapted from MIT-licensed Scroll World; retain `references/LICENSE-scroll-world`. Use actual video clips, one fixed stage, a scroll track, and editable DOM copy. For production templates start with the repository's `examples/scroll-demo`; the bundled diagnostic media is not AI quality evidence.

Encode seek-friendly media with ffmpeg (example):
```sh
ffmpeg -i input.mp4 -an -c:v libx264 -crf 20 -g 8 -pix_fmt yuv420p -movflags +faststart output.mp4
```
Keep native dimensions. Treat mobile portrait as a distinct composition when needed; do not silently crop essential content. Keep reduced-motion and keyboard navigation usable. Put detailed evidence behind intentional controls rather than obscuring the world.

Verify forward, stop, reverse, seams, resize, failed media, keyboard access, and reduced motion in a browser. Inspect actual camera movement, not only `currentTime`. Preserve QA evidence and report any missing mobile/browser coverage.
