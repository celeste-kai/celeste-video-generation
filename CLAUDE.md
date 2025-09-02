# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`celeste-video-generation` is a domain-specific package within the Celeste multi-modal AI framework that provides unified video generation capabilities across multiple AI providers. It's built on `celeste-core` and follows the standard Celeste architecture patterns.

## Architecture

### Core Components
- **BaseVideoClient**: Abstract base class inherited from `celeste-core/base/video_client.py`
- **Provider Implementations**: Concrete classes for each supported video generation provider
- **PROVIDER_MAPPING**: Central registry linking Provider enums to implementation classes
- **Factory Pattern**: `create_video_client()` function for dynamic client instantiation

### Supported Providers
- **Replicate**: Bytedance SeedDance models and other video generation models
- **Google**: Veo 3.0 video generation (via Google AI Studio)

### Provider Structure
```
src/celeste_video_generation/
├── __init__.py              # Factory function and public API
├── mapping.py               # PROVIDER_MAPPING configuration
└── providers/
    ├── replicate.py         # Replicate video generation client
    └── google.py            # Google video generation client
```

## Development Commands

### Package Installation
```bash
uv add celeste-video-generation  # Add as dependency
pip install -e .                 # Local development install
```

### Testing
```bash
python example.py                # Run example usage
pytest tests/                    # Run tests (when available)
```

### Code Quality
```bash
ruff check . --fix               # Lint and fix
ruff format .                    # Format code
mypy .                           # Type checking
pre-commit run --all-files       # Run all pre-commit hooks
```

## Key Patterns

### Provider Implementation
1. Inherit from `BaseVideoClient` in `celeste-core`
2. Implement `generate_content()` method returning `AIResponse[list[VideoArtifact]]`
3. Implement `stream_generate_content()` for streaming support (optional)
4. Handle provider-specific authentication via `celeste_core.config.settings`
5. Normalize outputs to standard `VideoArtifact` format

### Adding New Models
1. Ensure model exists in `celeste-core/src/celeste_core/models/catalog.py`
2. Update `PROVIDER_MAPPING` in `mapping.py` if adding new provider
3. Test with example usage patterns

### Environment Configuration
Required environment variables are validated through `celeste-core` settings:
- `REPLICATE_API_TOKEN` for Replicate provider
- `GOOGLE_API_KEY` for Google provider

## Response Format

All providers return standardized `AIResponse` objects:
```python
response = await client.generate_content(prompt)
for video in response.content:
    video.url      # Video URL if available
    video.data     # Raw bytes if available  
    video.metadata # Provider-specific info
```

## Implementation Notes

- Video generation is inherently async - all methods use `async/await`
- Providers handle polling for long-running operations internally
- Use `asyncio.to_thread()` for sync API calls within async methods
- URLs are preferred over raw bytes for video artifacts due to size
- Provider-specific parameters passed through `**kwargs` to `generate_content()`

## Dependencies

- `celeste-core`: Base classes, enums, response types, settings
- `replicate`: Replicate API client
- `google-genai`: Google AI Studio API client