import asyncio

from celeste_core.config.settings import settings
from celeste_video_generation.providers.replicate import ReplicateVideoClient


async def main() -> None:
    # Validate provider credentials via celeste-core settings
    settings.validate_for_provider("replicate")

    client = ReplicateVideoClient()
    prompt = "A serene landscape with a waterfall at sunset, cinematic"

    _ = await client.generate_content(prompt, duration=5, resolution="480p")
    # Video output available in resp.content

    async for _chunk in client.stream_generate_content(
        prompt, duration=5, resolution="480p"
    ):
        # Event content available in chunk.content
        pass


if __name__ == "__main__":
    asyncio.run(main())
