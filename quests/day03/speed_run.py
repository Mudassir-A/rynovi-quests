"""Day 3 · The speed run

20 pages, 0.2 seconds each. One by one that's 4 seconds. Together it's about 0.2.
Use fake_web.fetch(url) for every request.

Run `python quest.py 3` after each TODO.
"""

import asyncio  # noqa: F401

from quests.day03 import fake_web


async def fetch_one(url: str) -> tuple[str, int]:
    """TODO 3.1 · Fetch one page with `await fake_web.fetch(url)` and return (url, length of the page)."""
    page = await fake_web.fetch(url)
    return (url, len(page))


async def fetch_all(urls: list[str]) -> list[tuple[str, int]]:
    """TODO 3.2 · Fetch every url AT THE SAME TIME (hint: asyncio.gather) and return results in the same order."""
    return await asyncio.gather(*(fetch_one(url) for url in urls))


async def fetch_all_limited(urls: list[str], limit: int = 3) -> list[tuple[str, int]]:
    semaphore = asyncio.Semaphore(limit)

    async def limited_fetch(url):
        async with semaphore:
            page = await fake_web.fetch(url)
            return (url, len(page))

    return await asyncio.gather(*(limited_fetch(url) for url in urls))


async def fetch_all_safe(
    urls: list[str], timeout: float = 0.5
) -> list[tuple[str, int | None]]:

    async def safe_fetch(url):
        try:
            page = await asyncio.wait_for(fake_web.fetch(url), timeout=timeout)
            return (url, len(page))

        except TimeoutError:
            return (url, None)

    return await asyncio.gather(*(safe_fetch(url) for url in urls))
