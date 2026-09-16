# Reporting security issues

Do not post credentials, private endpoints, customer documents, or personal configuration in an issue or pull request. For a suspected vulnerability, use GitHub's private vulnerability reporting option on this repository if it is enabled. If it is unavailable, ask a maintainer for a private reporting channel without including sensitive details.

This early preview has no promised security response time or supported-version policy. Use current source and review changes before running provider workflows.

Keep real `.env` and `*.local.json` files in your own project, outside this distribution. If a credential is exposed, revoke or rotate it with its provider; deleting a commit is not revocation. See [privacy and distribution guidance](docs/PRIVACY.md).
