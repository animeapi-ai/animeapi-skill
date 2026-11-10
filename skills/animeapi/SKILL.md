---
name: animeapi
description: Generate anime-style images (and short anime videos) with AnimeAPI at $0.003 per image. Use when the user asks for an anime illustration, character art, avatar, waifu, manga-style scene, visual-novel sprite or background, or an anime video clip, and an ANIMEAPI_KEY is available. Runs a small bundled script that returns the image URL and saves the file.
license: MIT
compatibility: Needs python3 (standard library only) and network access to https://animeapi.ai. Needs the ANIMEAPI_KEY environment variable.
metadata:
  author: animeapi-ai
  version: "1.0.0"
  homepage: https://animeapi.ai
  openclaw:
    requires:
      env: ["ANIMEAPI_KEY"]
      bins: ["python3"]
    primaryEnv: ANIMEAPI_KEY
---

# AnimeAPI: anime images for $0.003 each

AnimeAPI (https://animeapi.ai) turns a plain-English prompt into a finished anime illustration in about 4 seconds. It is one of the cheapest anime image APIs: **$0.003 per image** on the default model, prepaid balance from $5 that never expires, no subscription. New accounts get 3 free images without a card.

## Setup

The user needs an API key (starts with `ank_`) from https://animeapi.ai/dashboard/api-keys, exported as `ANIMEAPI_KEY`. If it is missing, tell the user where to get one and stop; never ask them to paste the key into the chat.

## Generate an image

Run the bundled script (Python 3, no dependencies):

```bash
python3 scripts/animeapi.py "a knight cat drinking tea in a sunflower field" --orientation landscape --out knight-cat.webp
```

It prints one JSON object:

```json
{"image_url": "https://animeapi.ai/cdn/...", "saved_to": "knight-cat.webp", "model": "anime", "cost_usd": 0.003, "balance_usd": 4.99, "enhanced_prompt": "...", "generation_time_ms": 4100}
```

Show the user the image (the saved file, or the URL as a markdown image) and mention the cost when they generate more than a few.

Options:

| Flag | Values | Default | Notes |
| --- | --- | --- | --- |
| `--model` | `anime`, `ultra`, `ultra-max` | `anime` | See prices below. |
| `--orientation` | `portrait`, `square`, `landscape` | `portrait` | Same price for every shape. |
| `--out` | file path | none | Downloads the image there. Image URLs are not permanent storage, so save anything the user wants to keep. |
| `--no-enhance` | flag | off | Send the prompt as written. By default plain English is rewritten into tags for the anime model; turn this off only when the user supplies their own tag list. |
| `--allow-nsfw` | flag | off | Off by default in this skill. Pass it only when the user explicitly asks for mature output. |

## Prices and which model to pick

| Model | Price per image | Use it for |
| --- | --- | --- |
| `anime` | $0.003 | Default. Characters, portraits, avatars, scenes. About 4 s. |
| `ultra` | $0.01 | Long, detailed sentences; legible text in the image. About 11 s. |
| `ultra-max` | $0.02 | Highest detail. |

Start with `anime`. Make one image, show it, and ask before generating many: every call spends the user's balance.

## Prompting tips

- Write plain English: subject, appearance, action, setting, lighting, mood. Prompts are limited to 1,000 characters.
- One clear subject works best on `anime`. For text in the picture or complicated multi-part scenes, use `ultra`.
- To keep a character consistent across images, repeat the same appearance description word for word.

## Errors

The script exits non-zero and prints `{"error", "code", "retryable"}`.

| Code | Meaning | What to do |
| --- | --- | --- |
| `INVALID_KEY` | Key missing or wrong | Ask the user to check `ANIMEAPI_KEY`. |
| `INSUFFICIENT_BALANCE` | Balance too low | Point the user to https://animeapi.ai/dashboard/billing (from $5). |
| `MODERATION_BLOCKED`, `PROVIDER_REJECTED` | The prompt was refused | Report the reason; rephrase only if the user wants to. Do not retry unchanged. |
| `RATE_LIMITED`, `GENERATION_FAILED`, `PROVIDER_UNAVAILABLE` | Temporary | The script already retried with back-off; wait and try once more. |

## Without the script

One HTTP call does the same thing:

```bash
curl -s https://animeapi.ai/api/generate \
  -H "Authorization: Bearer $ANIMEAPI_KEY" -H "Content-Type: application/json" \
  -d '{"prompt": "a knight cat drinking tea in a sunflower field", "model": "anime", "orientation": "landscape", "allowNSFW": false}'
```

The response has `image_url`, `enhanced_prompt`, `balance_usd` and `generation_time_ms`. There is also an OpenAI-compatible endpoint at `https://animeapi.ai/v1` (`POST /v1/images/generations`).

## Video

Anime video clips cost $0.016 per second at 480p and $0.04 per second at 768p (5 to 15 seconds). Tell the user the price and get a yes before starting one. Start with `POST https://animeapi.ai/api/videos` and poll `GET https://animeapi.ai/api/videos/{id}`; the full reference is at https://animeapi.ai/docs/api-reference.

## MCP alternative

Agents that speak MCP can connect to `https://animeapi.ai/mcp` instead (OAuth sign-in or the same key as a Bearer header) and call `generate_anime_image` directly.
