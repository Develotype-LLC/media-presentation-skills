# Release notes

**v0.1.0 — public preview.** Portable skills and a complete local-video presentation showcase.

## What users can expect

Eight task-named skills, user-controlled provider profiles, an installer, and editable starters. Cloud media can be generated in a separate service and imported manually; no local GPU is required. Local text supports compatible Chat Completions and Ollama APIs. Local media requires a working ComfyUI API workflow with the correct installed nodes and models.

Other inference servers need a compatible gateway or an adapter. Your mileage will vary with model capabilities, memory, drivers, workflow nodes, provider limits, and the coding harness's tools. This is not a universal inference driver.

| Capability | Evidence | Release claim |
|---|---|---|
| Skill packaging and private-config exclusion | Automated validator and tests | Tested within documented patterns |
| Codex, Claude Code, Copilot installation folders | Isolated installation tests | Layout tested; native discovery not certified |
| Text and ComfyUI protocol client | Mock HTTP services | Protocol tests; real servers unqualified |
| Scroll interaction | Synthetic clips in Chromium | Bounded forward/hold/reverse test |
| Video composition | Remotion MP4 rendered | Deterministic animation works |
| AI-generated still | Built-in cloud image tool; output visually inspected | One original raster sample, with prompt and provenance |
| AI-generated video | Historical artifacts plus fresh LTX trial | Fresh three-clip local trial completed; bundled client dry-run only |
| Blender | Existing rendered clips and source projects; starter syntax checked | Established source workflow; bundled starter runtime pending |

See [validation details](VALIDATION.md). Visual quality and real model behavior require separate review from code tests.

## Publication review

The public repository is created from a reviewed snapshot. Earlier private history, Actions records and original production logs remain in a separate private archive and are not copied. The public showcase includes only selected presentation files, three videos, a poster and font/logo assets with notices. Raw endpoint inventory, private configuration and job logs are excluded.

Source validation, 19 unit tests and the documented media/browser checks form the release evidence. This is an early preview; see [validation](VALIDATION.md) for remaining limits.

## Reproduce packaging checks

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/install.py --harness codex --project /tmp/media-skills-release-check
```

Use a fresh destination for each installer test. Create a distribution from a reviewed commit with `git archive`, not by zipping a working directory: ignored local output, dependencies, private profiles, and history backups must not ship.

## v0.1.0

Initial preview: eight reusable skills for story planning, deck adaptation, image/video generation, provider configuration, scroll video, Blender explainers, Remotion composition, and interactive presentations. Includes blank private configuration templates, portable provider helpers, editable examples, and explicit validation limits. Existing workflows have produced real AI video and Blender renders. Fresh-install qualification of the portable client and bundled Blender starter remains pending. See [workflow evidence](WORKFLOW-EVIDENCE.md).
