"""
Run this script once locally to generate TG_SESSION_STRING for .env.

Usage:
    python generate_session.py
"""
import asyncio
import os

from telethon import TelegramClient
from telethon.sessions import StringSession


async def main() -> None:
    api_id = int(input("Enter TG_API_ID: ").strip())
    api_hash = input("Enter TG_API_HASH: ").strip()

    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        await client.start()
        session_string = client.session.save()

    print("\n✅ Add this to your .env file:")
    print(f"TG_SESSION_STRING={session_string}\n")


if __name__ == "__main__":
    asyncio.run(main())
