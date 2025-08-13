"""Celeste Video Generation unified interface."""

from typing import Any, Union

from celeste_core import Provider
from celeste_core.base.client import BaseClient
from celeste_core.config.settings import settings

SUPPORTED_PROVIDERS: set[Provider] = {
    Provider.REPLICATE,
}


def create_video_client(provider: Union[Provider, str], **kwargs: Any) -> BaseClient:
    if isinstance(provider, str):
        provider = Provider(provider)

    if provider not in SUPPORTED_PROVIDERS:
        supported = [p.value for p in SUPPORTED_PROVIDERS]
        raise ValueError(
            f"Unsupported provider: {provider.value}. Supported: {supported}"
        )

    settings.validate_for_provider(provider.value)

    provider_mapping = {
        Provider.REPLICATE: (".providers.replicate", "ReplicateVideoClient"),
    }
    module_path, class_name = provider_mapping[provider]
    module = __import__(f"celeste_video_generation{module_path}", fromlist=[class_name])
    client_class = getattr(module, class_name)
    return client_class(**kwargs)


__all__ = [
    "create_video_client",
]
