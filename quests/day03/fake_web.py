"""A pretend internet for day 3. Don't edit this file.

fetch(url) waits 0.2 s like a real page would, then returns its HTML.
URLs containing "slow" hang for 5 seconds.
It also counts how many fetches run at the same time, so the tests can check your limits.
"""
import asyncio

running = 0
max_running = 0


def reset() -> None:
    global running, max_running
    running = max_running = 0

    
async def fetch(url: str) -> str:
    global running, max_running
    running += 1
    max_running = max(max_running, running)
    try:
        await asyncio.sleep(5 if "slow" in url else 0.2)
        return f"<html><body>{url}</body></html>"
    finally:
        running -= 1
