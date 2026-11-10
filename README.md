# AnimeAPI agent skill

An agent skill that lets Claude Code, Codex, Cursor, OpenClaw and other skill-aware agents generate anime images with [AnimeAPI](https://animeapi.ai) at **$0.003 per image**, one of the cheapest anime image APIs. Prepaid balance from $5 that never expires, no subscription; new accounts get 3 free images without a card.

The skill is one `SKILL.md` and one small Python script with no dependencies. The agent runs the script, gets back the image URL and a saved file, and tells you what it cost.

## Install

With the [skills CLI](https://skills.sh) (works for Claude Code, Codex, Cursor, OpenCode and many more):

```bash
npx skills add animeapi-ai/animeapi-skill
```

Claude Code plugin marketplace:

```text
/plugin marketplace add animeapi-ai/animeapi-skill
/plugin install animeapi@animeapi
```

By hand: copy `skills/animeapi/` into your agent's skills folder (for Claude Code, `~/.claude/skills/animeapi/`).

Then give the agent a key. Create one at https://animeapi.ai/dashboard/api-keys and export it:

```bash
export ANIMEAPI_KEY=ank_your_key
```

## Use

Ask for what you want:

> Draw a knight cat drinking tea in a sunflower field, landscape, and save it as knight-cat.webp.

Or run the script yourself:

```bash
python3 skills/animeapi/scripts/animeapi.py "a knight cat drinking tea in a sunflower field" \
  --orientation landscape --out knight-cat.webp
```

```json
{"image_url": "https://animeapi.ai/cdn/...", "model": "anime", "orientation": "landscape", "cost_usd": 0.003, "balance_usd": 4.99, "saved_to": "knight-cat.webp"}
```

## Prices

| Model | Price per image | Use it for |
| --- | --- | --- |
| `anime` (default) | **$0.003** | Characters, portraits, avatars, scenes. About 4 seconds. |
| `ultra` | $0.01 | Long, detailed prompts; legible text in the image. |
| `ultra-max` | $0.02 | Highest detail. |

Video clips cost $0.016 per second (480p) or $0.04 per second (768p).

## Options

`--model`, `--orientation portrait|square|landscape`, `--out FILE`, `--no-enhance` (send the prompt exactly as written), `--allow-nsfw`. Mature output is **off by default** in this skill; the agent passes `--allow-nsfw` only when you ask for it.

## Prefer MCP?

AnimeAPI is also a remote MCP server at `https://animeapi.ai/mcp`: see [animeapi-ai/animeapi-mcp](https://github.com/animeapi-ai/animeapi-mcp).

## Licence

MIT
