from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider

# Capability for this domain package
CAPABILITY: Capability = Capability.VIDEO_GENERATION

# Provider wiring for video generation clients
PROVIDER_MAPPING: dict[Provider, tuple[str, str]] = {
    Provider.REPLICATE: (".providers.replicate", "ReplicateVideoClient"),
    Provider.GOOGLE: (".providers.google", "GoogleVideoClient"),
}

__all__ = ["CAPABILITY", "PROVIDER_MAPPING"]
