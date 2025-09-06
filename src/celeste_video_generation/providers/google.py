import asyncio
import tempfile
from typing import Any

from celeste_core import AIResponse, Provider, VideoArtifact
from celeste_core.base.video_client import BaseVideoClient
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.types.image import ImageArtifact
from google import genai
from google.genai import types


class GoogleVideoClient(BaseVideoClient):
    def __init__(self, model: str = "veo-3.0-generate-preview", **kwargs: Any) -> None:
        super().__init__(
            model=model,
            capability=Capability.VIDEO_GENERATION,
            provider=Provider.GOOGLE,
            **kwargs,
        )
        self.client = genai.Client(api_key=settings.google.api_key)

    def _prepare_image(self, image: ImageArtifact | None) -> types.Image | None:
        """Convert ImageArtifact to types.Image format."""
        if not image:
            return None
        if image.path:
            return types.Image.from_file(location=image.path)
        elif image.data:
            # For byte data, save to temp file and use from_file
            # Detect file extension from image data
            ext = ".jpg"  # default
            if image.data.startswith(b"\x89PNG"):
                ext = ".png"
            elif image.data.startswith(b"RIFF") and b"WEBP" in image.data[:12]:
                ext = ".webp"

            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(image.data)
                tmp_file.flush()
                return types.Image.from_file(location=tmp_file.name)
        else:
            raise ValueError("ImageArtifact must have either data or path")

    async def generate_content(
        self,
        prompt: str,
        image: ImageArtifact | None = None,
        **kwargs: Any,  # noqa: ARG002
    ) -> AIResponse[list[VideoArtifact]]:
        # Start video generation
        operation = await self.client.aio.models.generate_videos(
            model=self.model,
            prompt=prompt,
            image=self._prepare_image(image),
        )

        # Poll the operation status until the video is ready
        while not operation.done:
            await asyncio.sleep(10)
            operation = await self.client.aio.operations.get(operation)

        # Get the generated video with both URI and bytes
        generated_video = operation.response.generated_videos[0]
        video_url = generated_video.video.uri
        video_data = generated_video.video.video_bytes

        artifacts: list[VideoArtifact] = [VideoArtifact(url=video_url, data=video_data)]

        return AIResponse(
            content=artifacts,
            provider=Provider.GOOGLE,
            metadata={"model": self.model, "output": generated_video},
        )
