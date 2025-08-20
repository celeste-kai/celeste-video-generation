"""Celeste Video Generation unified interface."""

from importlib import import_module
from typing import Any, Union

from celeste_core import Provider
from celeste_core.base.client import BaseClient
from celeste_core.config.settings import settings

from .mapping import PROVIDER_MAPPING


def create_video_client(provider: Union[Provider, str], **kwargs: Any) -> BaseClient:
    prov = Provider(provider) if isinstance(provider, str) else provider
    if prov not in PROVIDER_MAPPING:
        raise ValueError(f"Provider '{prov.value}' is not wired for video generation.")

    settings.validate_for_provider(prov.value)
    module_path, class_name = PROVIDER_MAPPING[prov]
    module = import_module(f"celeste_video_generation{module_path}")
    return getattr(module, class_name)(**kwargs)


__all__ = [
    "create_video_client",
]
