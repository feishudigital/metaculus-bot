"""
Free health check (no LLM calls): which account the token belongs to, and the
status and open/close times of the newest questions in each tournament. Standard library only. Run via the "Check Metaculus" workflow.
"""

import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime

API = "https://www.metaculus.com/api"
TOURNAMENTS = ["33121", "minibench"]


def get(path: str, **params: str) -> dict:
    time.sleep(3)  # Metaculus answers rapid requests with 429
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url, headers={"Authorization": f"Token {os.environ['METACULUS_TOKEN']}"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def field(post: dict, name: str) -> str | None:
    return post.get(name) or (post.get("question") or {}).get(name)


def hours_between(start: str | None, end: str | None) -> str:
    if not start or not end:
        return "?"
    delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
    return f"{delta.total_seconds() / 3600:.1f} h"


me = get("/users/me")
print(f"Account: {me.get('username')} (id {me.get('id')}, is_bot={me.get('is_bot')})")

for tournament in TOURNAMENTS:
    print(f"\n== Tournament {tournament}")
    newest = get("/posts/", tournaments=tournament, order_by="-open_time", limit="8")
    for post in newest.get("results", []):
        opened = field(post, "open_time")
        closes = field(post, "scheduled_close_time")
        print(
            f"  {post['id']} {post.get('status')} open {opened} close {closes}"
            f" ({hours_between(opened, closes)}) {post['title'][:60]}"
        )
