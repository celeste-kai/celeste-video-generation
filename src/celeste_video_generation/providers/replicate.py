import asyncio
from typing import Any

import replicate
from celeste_core import AIResponse, Provider, VideoArtifact
from celeste_core.base.client import BaseClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability


class ReplicateVideoClient(BaseClient):
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
        # client.run is synchronous; offload to a thread
        outputs = await asyncio.to_thread(
            self.client.run, self.model_name, input=inputs
        )
        artifacts: list[VideoArtifact] = []
        # Replicate returns file-like or URLs; normalize to VideoArtifact
        if isinstance(outputs, list):
            for out in outputs:
                url = None
                if hasattr(out, "url"):
                    try:
                        url = out.url()  # type: ignore[call-arg]
                    except Exception:
                        url = None
                if isinstance(out, str) and out.startswith("http"):
                    url = out
                artifacts.append(VideoArtifact(url=url))
        else:
            url = None
            if hasattr(outputs, "url"):
                try:
                    url = outputs.url()  # type: ignore[call-arg]
                except Exception:
                    url = None
            if isinstance(outputs, str) and outputs.startswith("http"):
                url = outputs
            artifacts.append(VideoArtifact(url=url))

        return AIResponse(
            content=artifacts,
            provider=Provider.REPLICATE,
            metadata={"model": self.model_name},
        )
