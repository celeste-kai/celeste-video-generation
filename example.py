import asyncio

import streamlit as st
from celeste_core import Provider, list_models
from celeste_core.enums.capability import Capability
from celeste_core.types.image import ImageArtifact

from celeste_video_generation import create_video_client


async def main() -> None:
    st.set_page_config(page_title="Celeste Video Generation", page_icon="🎬", layout="wide")
    st.title("🎬 Celeste Video Generation")

    # Get providers that support video generation
    providers = sorted(
        {m.provider for m in list_models(capability=Capability.VIDEO_GENERATION)},
        key=lambda p: p.value,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")
        provider = st.selectbox("Provider:", [p.value for p in providers], format_func=str.title)
        models = list_models(provider=Provider(provider), capability=Capability.VIDEO_GENERATION)
        model_names = [m.display_name or m.id for m in models]
        selected_idx = st.selectbox("Model:", range(len(models)), format_func=lambda i: model_names[i])
        model = models[selected_idx].id

        # Video generation options
        st.subheader("Options")
        uploaded_image = st.file_uploader("Starting Image (optional)", type=["png", "jpg", "jpeg", "webp"])

    st.markdown(f"*Powered by {provider.title()}*")

    # Show uploaded image if provided
    if uploaded_image:
        st.subheader("Starting Image")
        st.image(
            uploaded_image,
            caption="This image will be used as the starting frame",
            width="stretch",
        )

    # Prompt input
    prompt = st.text_area(
        "Enter your video prompt:",
        "A serene landscape with a waterfall at sunset, cinematic",
        height=100,
        placeholder="Describe the video you want to generate...",
    )

    if st.button("🎬 Generate Video", type="primary", width="stretch"):
        if not prompt.strip():
            st.error("Please enter a video prompt.")
        else:
            client = create_video_client(Provider(provider), model=model)

            # Prepare image if uploaded
            image_artifact = None
            if uploaded_image:
                image_artifact = ImageArtifact(data=uploaded_image.read())

            with st.spinner("Generating video... This may take several minutes."):
                response = await client.generate_content(
                    prompt,
                    image=image_artifact,
                )

                if response.content:
                    st.success("✅ Video generated successfully!")

                    # Display the first video
                    video = response.content[0]
                    if video.url:
                        st.video(video.url)
                    elif video.data:
                        st.video(video.data)
                    else:
                        st.warning("Video generated but no URL or data available")

                    # Show metadata
                    with st.expander("📊 Details"):
                        st.write(f"**Provider:** {provider}")
                        st.write(f"**Model:** {model}")
                        if video.metadata:
                            st.json(video.metadata)
                else:
                    st.error("Failed to generate video. Please try again.")

    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Celeste")


if __name__ == "__main__":
    asyncio.run(main())
