#!/usr/bin/env python3
"""Generate one anime image with AnimeAPI ($0.003 per image on the default model).

Usage: animeapi.py "prompt" [--model anime|ultra|ultra-max]
       [--orientation portrait|square|landscape] [--out FILE] [--no-enhance] [--allow-nsfw]

Reads the key from ANIMEAPI_KEY. Prints one JSON object. Standard library only.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("ANIMEAPI_BASE_URL", "https://animeapi.ai").rstrip("/")
PRICES = {"anime": 0.003, "ultra": 0.01, "ultra-max": 0.02}
USER_AGENT = "animeapi-skill/1.0"


def fail(error, code, retryable=False):
    print(json.dumps({"error": error, "code": code, "retryable": retryable}))
    sys.exit(1)


def generate(key, body):
    request = urllib.request.Request(
        BASE_URL + "/api/generate",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    last = None
    for attempt in range(3):
        if attempt:
            time.sleep(wait)
        wait = 2 * (attempt + 1)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.load(response)
        except urllib.error.HTTPError as e:
            try:
                last = json.load(e)
            except ValueError:
                last = {"error": "AnimeAPI returned HTTP %d" % e.code, "code": "HTTP_%d" % e.code}
            retryable = bool(last.get("retryable")) or e.code in (500, 503)
            last["retryable"] = retryable
            if not retryable:
                break
            retry_after = e.headers.get("Retry-After", "")
            if retry_after.isdigit():
                wait = min(int(retry_after), 30)
        except (urllib.error.URLError, TimeoutError) as e:
            last = {"error": "Could not reach AnimeAPI: %s" % e, "code": "NETWORK_ERROR", "retryable": True}
    fail(last.get("error", "Unknown error"), last.get("code", "UNKNOWN"), last.get("retryable", False))


def main():
    parser = argparse.ArgumentParser(description="Generate one anime image with AnimeAPI.")
    parser.add_argument("prompt", help="What to draw, in plain English (up to 1,000 characters).")
    parser.add_argument("--model", choices=sorted(PRICES), default="anime")
    parser.add_argument("--orientation", choices=["portrait", "square", "landscape"], default="portrait")
    parser.add_argument("--out", help="Download the image to this file.")
    parser.add_argument("--no-enhance", action="store_true", help="Send the prompt as written.")
    parser.add_argument("--allow-nsfw", action="store_true", help="Allow mature output (off by default).")
    args = parser.parse_args()

    key = os.environ.get("ANIMEAPI_KEY", "").strip()
    if not key:
        fail("Set ANIMEAPI_KEY (create a key at https://animeapi.ai/dashboard/api-keys).", "INVALID_KEY")
    if len(args.prompt) > 1000:
        fail("The prompt is longer than 1,000 characters.", "VALIDATION_ERROR")

    data = generate(key, {
        "prompt": args.prompt,
        "model": args.model,
        "orientation": args.orientation,
        "enhance": not args.no_enhance,
        "allowNSFW": args.allow_nsfw,
    })
    result = {
        "image_url": data["image_url"],
        "model": args.model,
        "orientation": args.orientation,
        "cost_usd": PRICES[args.model],
        "balance_usd": data.get("balance_usd"),
        "enhanced_prompt": data.get("enhanced_prompt"),
        "generation_time_ms": data.get("generation_time_ms"),
    }
    if args.out:
        download = urllib.request.Request(data["image_url"], headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(download, timeout=120) as response, open(args.out, "wb") as f:
            f.write(response.read())
        result["saved_to"] = args.out
    print(json.dumps(result))


if __name__ == "__main__":
    main()
