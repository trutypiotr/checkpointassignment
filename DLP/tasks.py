import re

from api_client import api_client


async def fetch_patterns():
    return await api_client.get("patterns/")


async def send_caught_message(content: str, pattern_id: int, ts: float, channel: str):
    payload = {"content": content, "pattern": pattern_id, "ts": ts, "channel": channel}
    await api_client.post("caught-messages/", payload)


async def handle_message(message: str, ts: float, channel: str) -> None:
    """
    Now that I think about it, it would be better to move the retrieving of the patterns somewhere to the main file,
    so that you don't make request every time. But thanks to this solution we can dynamically add patterns,
    without restarting the container.
    """
    patterns = await fetch_patterns()
    if patterns:
        for pattern in patterns:
            if re.match(pattern["regex"], message):
                await send_caught_message(message, pattern["id"], ts, channel)
                break
