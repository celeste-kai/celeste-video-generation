<div align="center">

# 🎬 Celeste Video Generation

### Multi-Provider Video Generation with Unified Interface

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Providers](https://img.shields.io/badge/Providers-Replicate-orange?style=for-the-badge&logo=databricks&logoColor=white)](#-supported-providers)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow?style=for-the-badge)](#-roadmap)

</div>

---

## 🎯 Why Celeste Video Generation?

<div align="center">
  <table>
    <tr>
      <td align="center">🎥<br><b>Video Creation</b><br>Generate videos from text prompts</td>
      <td align="center">🔄<br><b>Unified Interface</b><br>Same API across all providers</td>
      <td align="center">🌊<br><b>Streaming Support</b><br>Real-time generation updates</td>
      <td align="center">🎛️<br><b>Provider Flexibility</b><br>Switch providers with one line</td>
    </tr>
  </table>
</div>

`celeste-video-generation` provides a unified interface for video generation across multiple AI providers. Built on `celeste-core`, it normalizes different provider APIs while maintaining provider-specific features.

## 🚀 Quick Start

```bash
pip install -e .
```

Generate a video with Replicate:

```python
import asyncio
from celeste_video_generation.providers.replicate import ReplicateVideoClient

async def main():
    # Initialize client with a video model
    client = ReplicateVideoClient(model="bytedance/seedance-1-lite")

    # Generate video
    prompt = "A serene landscape with a waterfall at sunset, cinematic"
    response = await client.generate_content(prompt)

    # Access video artifacts
    for video in response.content:
        print(f"Video URL: {video.url}")
        # video.data contains bytes if available

asyncio.run(main())
```

## 📦 Installation

<details open>
<summary><b>Using pip</b></summary>

```bash
git clone https://github.com/yourusername/celeste
cd celeste/celeste-video-generation
pip install -e .
```

</details>

<details>
<summary><b>Using uv</b></summary>

```bash
git clone https://github.com/yourusername/celeste
cd celeste/celeste-video-generation
uv pip install -e .
```

</details>

## 🔧 Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Replicate (Currently supported)
REPLICATE_API_TOKEN=your_replicate_token

# Future providers
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

### Provider API Keys

| Provider | Environment Variable | Get API Key | Status |
|----------|----------------------|-------------|--------|
| 🔄 **Replicate** | `REPLICATE_API_TOKEN` | [Replicate](https://replicate.com/account/api-tokens) | ✅ Supported |
| 🤖 **OpenAI** | `OPENAI_API_KEY` | [OpenAI](https://platform.openai.com/api-keys) | 🔜 Coming Soon |
| 🌈 **Google** | `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) | 🔜 Coming Soon |

## 🎬 Supported Providers

### Replicate
- **Models**: `bytedance/seedance-1-lite`, custom models
- **Features**: Text and image-to-video generation
- **Output**: Video URLs, optional raw bytes

## 💻 Usage Examples

### Basic Video Generation

```python
from celeste_video_generation.providers.replicate import ReplicateVideoClient

client = ReplicateVideoClient(model="bytedance/seedance-1-lite")
response = await client.generate_content(
    "A robot dancing in a futuristic city"
)
```

### Streaming Generation

```python
async for chunk in client.stream_generate_content(
    "Ocean waves crashing on a beach"
):
    print(f"Generation progress: {chunk.content}")
```

### Custom Model Parameters

```python
response = await client.generate_content(
    prompt="Abstract art in motion",
    fps=30,
    aspect_ratio="16:9"
)
```

## 📊 Response Format

All providers return a standardized `AIResponse` containing `VideoArtifact` objects:

```python
response = await client.generate_content(prompt)

# Access video artifacts
for video in response.content:
    video.url      # Video URL (if available)
    video.data     # Raw video bytes (if available)
    video.metadata # Provider-specific metadata

# Provider information
response.provider  # Provider.REPLICATE
response.metadata  # Additional response metadata
```

## 🗺️ Roadmap

- [x] Replicate provider support
- [ ] OpenAI Sora integration (when available)
- [ ] Google video generation models
- [ ] Stability AI video models
- [ ] Local model support (ComfyUI, Auto1111)
- [ ] Video editing capabilities
- [ ] Multi-modal inputs (image-to-video)
- [ ] Advanced streaming with progress callbacks
- [ ] Video format conversion utilities

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Running the Example

```bash
python example.py
```

## 🌌 Celeste Ecosystem

| Package | Description | Status |
|---------|-------------|--------|
| 🧩 **celeste-core** | Core types, enums, and base classes | ✅ Available |
| 💬 **celeste-client** | Text generation & chat | ✅ Available |
| 🎨 **celeste-image-generation** | Multi-provider image generation | ✅ Available |
| ✏️ **celeste-image-edit** | Image editing capabilities | ✅ Available |
| 🎧 **celeste-audio-intelligence** | Audio processing & transcription | ✅ Available |
| 📄 **celeste-document-intelligence** | Document analysis & QA | ✅ Available |
| 🔢 **celeste-embeddings** | Text embeddings | ✅ Available |
| 🚀 **celeste-api** | FastAPI backend | ✅ Available |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Adding a New Provider

1. Create a new file in `src/celeste_video_generation/providers/`
2. Extend `BaseClient` from `celeste-core`
3. Implement `generate_content` and `stream_generate_content` methods
4. Add provider-specific configuration to settings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ by the Celeste Team

  <a href="#-celeste-video-generation">⬆ Back to Top</a>
</div>
