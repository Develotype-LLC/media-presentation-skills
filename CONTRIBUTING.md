# Contributing

Keep one capability per skill and describe when it should be selected. Put provider-specific detail behind references. Use relative paths and operator-supplied configuration. Preserve source claims and document uncertainty.

For a change, run `python3 scripts/validate.py`, exercise modified scripts, and record representative behavioral checks. For media workflows include actual frames/playback evidence and software versions; a rendered file is not audience acceptance. Never commit private decks, transcripts, keys, voice samples, weights, or personal host profiles.

New provider adapters should take an explicit endpoint, avoid hardcoded models, set timeouts/retry budgets, record job IDs, and never cancel other users' work. Do not describe a provider as verified until a bounded job has been inspected.
