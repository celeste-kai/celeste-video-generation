import asyncio
from typing import Any

import replicate
from celeste_core import AIResponse, Provider, VideoArtifact
from celeste_core.base.video_client import BaseVideoClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability


class ReplicateVideoClient(BaseVideoClient):
    def __init__(self, model: str, **kwargs: Any) -> None:
        super().__init__(
            model=model,
            capability=Capability.VIDEO_GENERATION,
            provider=Provider.REPLICATE,
            **kwargs,
        )
        self.client = replicate.Client(api_token=settings.replicate.api_token)

    async def generate_content(
        self, prompt: str, **kwargs: Any
    ) -> AIResponse[list[VideoArtifact]]:
        # See: https://replicate.com/bytedance/seedance-1-lite/api
        inputs = {"prompt": prompt, **kwargs}
        # Request plain URL strings from Replicate to avoid FileOutput objects
        outputs = await asyncio.to_thread(
            self.client.run, self.model, input=inputs, use_file_output=False
        )

        # Normalize to a list of HTTP URLs with minimal branching
        urls: list[str] = []
        if isinstance(outputs, list):
            urls = [u for u in outputs if isinstance(u, str) and u.startswith("http")]
        elif isinstance(outputs, str) and outputs.startswith("http"):
            urls = [outputs]

        artifacts: list[VideoArtifact] = [VideoArtifact(url=u) for u in urls]

        return AIResponse(
            content=artifacts,
            provider=Provider.REPLICATE,
            metadata={"model": self.model},
        )
