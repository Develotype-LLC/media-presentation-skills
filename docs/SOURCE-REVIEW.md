# Workflow review and provenance

This toolkit generalizes media planning, deck conversion, local inference, generated shots, technical reveals, video composition, and interactive delivery into reusable instructions. Personal source documents, project paths, host profiles, hardware inventories, and access details are excluded.

## Decisions retained

- Start with audience, message, and visual concepts; review stills before producing a batch of videos.
- Keep claim sources and assumptions visible in the project. Generated scenery is not evidence for a claim.
- Separate clean footage, native labels, and narration so they can be revised independently.
- Distinguish continuous camera journeys from independently anchored shots with deliberate transitions.
- Verify a runtime with a bounded trial; historical render timings and GPU device numbers are not portable defaults.
- Treat provider endpoints, models, and credentials as recipient configuration, separate from the skills.

## Third-party source

The scroll interaction engine derives from [Scroll World](https://github.com/oso95/scroll-world). Its MIT notice is preserved beside the engine. The public-source manifest records the distributed engine hash. Other toolkit instructions and examples are curated, generalized material; private originals are not bundled.

## Limits

This is a reusable workflow and example package, not a copy of any personal environment. A provider profile connects to an existing service; it does not install models, GPU drivers, or third-party integrations. See [provider setup](../skills/configure-ai-providers/references/PROVIDERS.md) and [validation](VALIDATION.md).
