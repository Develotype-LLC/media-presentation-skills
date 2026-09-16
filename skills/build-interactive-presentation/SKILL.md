---
name: build-interactive-presentation
description: Build audience-controlled or presenter-controlled HTML presentations with beat navigation, optional narration, and a usable leave-behind.
---

# Interactive presentation

Choose the interaction that serves the audience: presenter next/back, self-guided exploration, or a scroll-controlled world. Preserve the approved narrative; interactivity is not a reason to replace a long-form story with a shorter one.

Give beats stable IDs. Separate title, body, evidence, media, narration takes, and navigation in data. Provide next/back, keyboard controls, visible focus, and direct links where appropriate. Narration is selectable/mutable per beat and should stop or switch when navigation changes. Do not autoplay sound without user interaction.

Use video where motion explains something; use diagrams where relationships need precision. Record the footage/motion-graphic/still mix during editorial review. Reuse diagrams for a new explanation; avoid repeating an unrelated generated shot to fill time.

Keep exact labels and citations in native elements. Evidence details can open on demand. Include a readable reduced-motion/static path and clear media-failure fallback. A static fallback is not proof of working video.

Verify opening, middle, closing, all navigation paths, media playback, optional voice-over, small screens, and the downloadable or hosted leave-behind as applicable. Publishing is a separate action unless the user requested it.

Deliver editable source, beat manifest, local run instructions, QA results, and export/hosting status. Use `build-scroll-video` when scroll itself must be the reversible camera controller.
