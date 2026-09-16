# Presentation QA

## Source and structural checks

- Ten stable beat IDs, each with title, body, three supporting points, source/evidence, editable notes, and planned duration.
- Approximately six-minute presenter narrative; no invented client numbers or proof claims.
- Three distinct video mappings; no repeated shot.
- Local logo/fonts; no analytics, trackers, external scripts, or private endpoint values.
- Native playback controls, no autoplay, pause-on-exit logic, direct hash navigation, focus styles, reduced-motion styles, responsive layout, print path, separate static leave-behind.

## Actual verification

JavaScript syntax and JSON checks run by author. Browser display, keyboard interaction, mobile overflow, actual media loading/playback, and print layout require parent verification and must be reported independently of structural checks. Native controls alone do not prove playback. No audio track has been produced or listened to for this presentation.

## Parent browser verification

- Inspected desktop opening and final video layouts, and 390 × 844 mobile build beat. No horizontal overflow in checked views.
- Verified next/back traversal through all ten beats, disabled boundary buttons, right-arrow navigation, direct hash entry, and presenter-note toggle.
- All three real local MP4s loaded with duration 4.041667 seconds and no media errors. First standalone clip played to its end; second and third played in presentation. Changing beats paused videos. No missing-media fallback remained after final files arrived.
- Static leave-behind loaded all ten sections and full speaker text. Fonts loaded locally.
- One in-app browser tab crashed during a native video-control interaction after reload; a fresh tab loaded and played the same final clip successfully. No cause established.
- Reduced-motion and print styles were source-reviewed, not separately exercised. Physical phone/Safari and print/PDF export remain untested. No narration audio generated; the full script is editable presenter notes.
