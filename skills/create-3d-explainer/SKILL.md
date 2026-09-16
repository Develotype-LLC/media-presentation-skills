---
name: create-3d-explainer
description: Create editable Blender scenes for mechanisms, spatial relationships, cutaways, and controlled camera motion in explainers.
---

# Blender explainer

Start with one teaching objective and the misconception the reveal must resolve. Separate real geometry and connections from illustrative teaching devices. Build a small reusable scene rather than a continuous feature-length render.

Write a shot brief: source references, required parts, topology, camera start/reveal/end, moving elements, duration, and overlay anchors. Use native diagrams if depth adds no understanding. Reuse existing geometry in copies after checking units and provenance.

Keep text out of clean footage. Put labels, arrows, numeric values, and narration in the composition layer. For fluid/heat explanations, keep circuit identities fixed; show heat and mass with distinct encodings; a separating wall must remain continuous. Label omitted systems and illustrative quantities in the companion explanation.

Create source `.blend` and deterministic build script when practical. Use relative asset paths or packed assets; record Blender version, render engine, fps, resolution, frame range, and device. Verify one frame and a short motion before a large render. Deliver short reveals with useful holds and a clean camera view for overlays.

Inspect opening/reveal/final frames and playback for interpenetration, disappearing parts, impossible connections, and wrong motion. Reopen the saved scene. A pretty render is not technical validation. Route the clean clip and anchor timing to `compose-video`.

Deliver source, clean clip, review stills, a shot manifest, observed render time, and unresolved technical decisions. The repository starter under `examples/blender` demonstrates an abstract reveal, not a physically validated system.
