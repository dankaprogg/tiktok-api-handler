from tiktok import TikTok

import asyncio

async def main():
    client = TikTok()
    user = await client.get_user("@renankkkjk")
    if user:
        print(f"User nickname: {user}")
    else:
        print("User not found")

    await client.close()
    await asyncio.sleep(1.0)

if __name__ == "__main__":
    asyncio.run(main())