# Develotype presentation trial

A ten-beat, approximately six-minute presentation demonstrating the skill library. This is an interpretation of public Develotype positioning, not approved sales copy, a customer case study, or evidence of business outcomes.

## Open

Serve the parent `showcase` directory with `python3 -m http.server 8793`, then open `http://localhost:8793/presentation/`. Keep the sibling `video/` folder alongside this folder. No external services are required for playback; logo and fonts are local copies of public website assets.

- Next/back buttons and arrow keys change beats. Home/End jump to first/last. Keyboard navigation leaves video controls and focused links/buttons alone.
- Each beat has a stable hash, such as `#diagnose`.
- Videos play only when the viewer uses native playback controls. They pause on leaving a beat.
- Presenter notes expose the full narrative. No generated voice track is included.
- `static.html` is a readable no-JavaScript leave-behind. Print the interactive page to include every beat; print output is static, not a video export.

## Edit

Edit `beats.json` for copy, notes, sources, timing, and media mapping, then run `python3 sync-content.py` to regenerate `beats.js`, `NARRATION.md`, and `static.html`. Change layout in `styles.css` and behavior in `app.js`.

## Media mix

Three unique local AI video clips: opening, build, and portable workflow. Six native HTML diagrams and one closing typographic panel. AI footage is atmospheric illustration; exact relationships remain editable HTML. No Blender media was produced for this particular trial, and no video is repeated across beats.

Video files: `../video/01-parts.mp4`, `../video/02-connect.mp4`, `../video/03-system.mp4`. See the sibling media manifest for method, timing and validation boundaries. All three clips were checked in the browser.

## Status and credits

Browser checks covered desktop/mobile layout, all-beat navigation, notes and actual video playback. See [QA](QA.md) and [media provenance](../MEDIA-MANIFEST.json). This published example contains no connection configuration or raw job logs.

Geist and Geist Mono use the included SIL Open Font License. The Develotype logo is used by its owner for this example; trademark rights are reserved. Original presentation code follows the repository MIT license. Generated footage is labeled illustrative and is not technical evidence.
