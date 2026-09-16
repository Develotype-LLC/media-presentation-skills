# Personal configuration and distribution

The published working tree contains generic workflow instructions, blank configuration templates, and loopback examples. Users provide their own endpoints, models, and credentials in ignored files. Personal source documents, home paths, host inventories, GPU assignments, SSH identities, and private source-file hashes are outside the distribution.

## Before sharing a change

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git status --short
```

The validator scans the distributable file set, including tracked files that were accidentally added despite ignore rules. It does not open ignored `.env` files. The installer excludes personal configuration, keys, model weights, and common generated folders, and refuses to follow symlinks from skill sources.

These checks catch common mistakes; review the actual diff as well. A private project name or unusual secret format may evade automated detection. Keep credentials in the user's own environment/secret manager, never in shared prompts, source examples, or JSON profile values.

The client prints no endpoint or credential values in diagnostics and does not echo raw provider error bodies. It does print requested model output, which may itself contain the prompt. Store sensitive outputs only in your approved project environment.

## Git history is separate

Deleting or sanitizing a current file does not remove older versions from Git history or someone else's clone. History cleanup changes commit IDs and needs coordination with existing users. If credentials were exposed, rotate them; rewriting Git does not revoke a credential or guarantee removal from external caches.

Bundled sample media, logo and fonts are explicitly allowlisted by path and SHA-256 in REVIEWED-ASSETS.json. Other binaries and changed assets fail validation. A checksum prevents unnoticed changes; it is not a content or metadata privacy audit. Review replacement media before updating the manifest.
