import asyncio
from typing import Any

from celeste_core import AIResponse, Provider, VideoArtifact
from celeste_core.base.video_client import BaseVideoClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from google import genai


class GoogleVideoClient(BaseVideoClient):
    def __init__(self, model: str = "veo-3.0-generate-preview", **kwargs: Any) -> None:
        super().__init__(
            model=model,
            capability=Capability.VIDEO_GENERATION,
            provider=Provider.GOOGLE,
            **kwargs,
        )
        self.client = genai.Client(api_key=settings.google.api_key)

    async def generate_content(
        self, prompt: str, **kwargs: Any
    ) -> AIResponse[list[VideoArtifact]]:
        # Start video generation
        operation = await self.client.aio.models.generate_videos(
            model=self.model_name,
            prompt=prompt,
        )

        # Poll the operation status until the video is ready
        while not operation.done:
            await asyncio.sleep(10)
            operation = await self.client.aio.operations.get(operation)

        # Get the generated video URI
        generated_video = operation.response.generated_videos[0]
        video_url = generated_video.video.uri

        artifacts: list[VideoArtifact] = [VideoArtifact(url=video_url)]

        return AIResponse(
            content=artifacts,
            provider=Provider.GOOGLE,
            metadata={"model": self.model_name},
        )
