# Install into a project

Python 3.10+ is needed for the packaging tools. No Python packages are required. Run commands from this repository root.

```sh
python3 scripts/install.py --harness codex --project /path/to/project
python3 scripts/install.py --harness claude --project /path/to/project
python3 scripts/install.py --harness copilot --project /path/to/project
```

The installer copies all eight self-contained skill folders, including references, example configuration, and helper scripts. It excludes real environment/profile files, keys, model weights, and caches, and refuses source symlinks. It preflights every destination and refuses to overwrite existing folders. Use `--dry-run` to inspect the plan. Upgrade by reviewing changes and removing only the old installed copies you intend to replace; originals remain in this repository.

| Harness | Project destination | Use |
|---|---|---|
| Codex | `.agents/skills/` | Ask for the named skill; `$plan-media-story` where supported |
| Claude Code | `.claude/skills/` | `/plan-media-story` or name it in the request |
| GitHub Copilot | `.github/skills/` | Ask the agent to use the named skill |
| Other coding agents | Choose a folder | Ask the agent to read the relevant `SKILL.md` and its references explicitly |

Reload/restart your agent session if new skills are not discovered. For Cursor, Gemini CLI, OpenCode, or another harness, use explicit file reading first; discovery paths vary by version and are not certified here. Do not rename the skill body into global rules that activate on every task.

Official references checked September 15, 2026: [Agent Skills specification](https://agentskills.io/specification), [Codex skills](https://developers.openai.com/codex/skills), [Claude Code skills](https://code.claude.com/docs/en/skills), [Copilot skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills). These describe discovery conventions; cross-harness end-to-end generation has not been certified.

## Tools are separate from skills

A skill tells the assistant how to work. A CLI, API, MCP server, or app gives it actions. Start with your existing agent, Python, and a browser. Add ffmpeg for the scroll demo, Node/Remotion for composition, Blender for geometry, and one media backend when you need generated footage. Do not install everything to try the planning workflow.

Never put credentials or machine access instructions in skill files. Keep personal configuration outside the distributed repository. See [tools](TOOLS.md).

## Configure services after installing

Use the installed `configure-ai-providers` skill's [setup instructions](../skills/configure-ai-providers/references/PROVIDERS.md). Its `assets/` folder contains `.env.example` and `providers.example.json`; its `scripts/ai_client.py` runs independently of this repository. Copy the examples into your working project and set your own values. Installation does not copy any real `.env` or grant service access.

The new capability-based names replace the initial package names; see [migration](SKILL-NAMES.md) before updating an existing installation.
