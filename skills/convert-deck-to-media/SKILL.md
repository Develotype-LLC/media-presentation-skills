---
name: convert-deck-to-media
description: Convert an existing slide deck into a source-faithful video or interactive presentation, preserving claims and documenting editorial changes.
---

# Deck to media

Read the deck's text, notes, charts, and visual layout using the available document tools. For Google Slides, use an authorized connector or a user-supplied export; private access failure is not permission to make it public. Keep the original intact. Render or inspect representative slides where text extraction misses layout or diagram meaning.

Create `facts.csv`: claim ID, exact value/text, units, source slide, evidence status, caveat, and dependency on other assumptions. A number in a deck is source-backed to that deck, not independently verified. Keep notes that limit claims.

Choose the transformation mode from the user's request:
- Companion: preserve order, language, and figures; record every departure.
- Adaptation: propose a shorter story and record merged/dropped/reworded beats before implementation.

Map slide IDs to beat IDs. Rebuild charts in editable DOM/SVG or the presentation format; keep all repeated numbers in one data source. Preserve a chart's baseline, denominator, units, and uncertainty. Carry brand tokens from the source but check contrast on the new background.

Route the storyboard through `plan-media-story`, then `build-scroll-video`, `compose-video`, or `build-interactive-presentation`. For smaller models, split work into extraction → facts → one beat → verification → remaining beats. Write a checkpoint after each stage with files, completed checks, and next command. An exit code alone is not visual acceptance.

Deliver the source mapping, change log, editable output, and QA record. A scroll companion may use anchored clips with deliberate transitions; do not call it a continuous camera flight unless its seams pass continuity review.
