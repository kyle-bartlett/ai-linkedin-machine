#!/usr/bin/env python3
"""
Image Optimizer Web App - Mobile-friendly web interface.

Run with:
    streamlit run image_optimizer/webapp.py

Then access from your phone at: http://YOUR_COMPUTER_IP:8501
"""

import streamlit as st
from pathlib import Path
from io import BytesIO
import tempfile
import zipfile

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

from .optimizer import ImageOptimizer, OutputFormat
from .strategies import ResizeStrategy
from .presets import SIZE_PRESETS


# Page config
st.set_page_config(
    page_title="Image Optimizer",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly UI
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
    }
    .uploadedFile {
        display: none;
    }
    div[data-testid="stImage"] {
        border: 2px solid #007acc;
        border-radius: 8px;
        padding: 5px;
    }
    .size-badge {
        background-color: #007acc;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("🖼️ Image Optimizer")
    st.caption("Resize images perfectly for any app or platform")

    # Initialize optimizer
    if not PILLOW_AVAILABLE:
        st.error("Pillow is required. Run: pip install Pillow")
        return

    optimizer = ImageOptimizer()

    # File uploader
    uploaded_file = st.file_uploader(
        "Drop an image here or tap to upload",
        type=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
        help="Supports PNG, JPEG, GIF, BMP, WebP"
    )

    if uploaded_file is None:
        st.info("👆 Upload an image to get started")

        # Show available platforms
        with st.expander("📋 Available Platforms & Sizes"):
            for platform, presets in SIZE_PRESETS.items():
                st.subheader(platform.title())
                cols = st.columns(3)
                for i, (name, (w, h)) in enumerate(sorted(presets.items())):
                    cols[i % 3].text(f"{name}: {w}x{h}")
        return

    # Load the image
    try:
        source_image = Image.open(uploaded_file)
        source_image.load()
    except Exception as e:
        st.error(f"Failed to load image: {e}")
        return

    # Display original image info
    orig_w, orig_h = source_image.size
    st.success(f"✅ Loaded: **{uploaded_file.name}** ({orig_w} x {orig_h} px)")

    # Show original image (smaller preview)
    with st.expander("🔍 View Original", expanded=False):
        st.image(source_image, use_container_width=True)

    st.divider()

    # === Resize Options ===
    st.subheader("📐 Choose Output Size")

    # Tabs for preset vs custom
    tab1, tab2 = st.tabs(["Platform Presets", "Custom Size"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            platform = st.selectbox(
                "Platform",
                options=list(SIZE_PRESETS.keys()),
                index=list(SIZE_PRESETS.keys()).index("linkedin"),
                format_func=lambda x: x.title()
            )

        with col2:
            presets = SIZE_PRESETS[platform]
            preset_options = {f"{name} ({w}x{h})": (name, w, h)
                           for name, (w, h) in presets.items()}

            selected_preset = st.selectbox(
                "Size Preset",
                options=list(preset_options.keys())
            )

            preset_name, target_w, target_h = preset_options[selected_preset]

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            custom_w = st.number_input("Width (px)", min_value=1, max_value=10000, value=512)
        with col2:
            custom_h = st.number_input("Height (px)", min_value=1, max_value=10000, value=512)

        if st.checkbox("Use custom size"):
            target_w, target_h = custom_w, custom_h
            preset_name = "custom"

    # Strategy selector
    strategy_options = {
        "Center Crop (recommended)": ResizeStrategy.CROP_CENTER,
        "Fit (letterbox)": ResizeStrategy.FIT,
        "Fill & Crop": ResizeStrategy.FILL,
        "Pad with background": ResizeStrategy.PAD,
        "Crop from Top": ResizeStrategy.CROP_TOP,
        "Crop from Bottom": ResizeStrategy.CROP_BOTTOM,
    }

    selected_strategy = st.selectbox(
        "Resize Strategy",
        options=list(strategy_options.keys()),
        help="How to handle aspect ratio differences"
    )
    strategy = strategy_options[selected_strategy]

    # Show output size
    st.markdown(f"**Output Size:** `{target_w} x {target_h}` px")

    st.divider()

    # === Preview ===
    st.subheader("👁️ Preview")

    # Generate preview
    try:
        preview = optimizer.resize(
            source_image.copy(),
            target_w,
            target_h,
            strategy
        )

        # Display preview
        st.image(preview, caption=f"Preview: {target_w}x{target_h}", use_container_width=True)

    except Exception as e:
        st.error(f"Preview failed: {e}")
        return

    st.divider()

    # === Export Options ===
    st.subheader("💾 Export")

    col1, col2 = st.columns(2)

    with col1:
        output_format = st.selectbox(
            "Format",
            options=["PNG", "JPEG", "WebP"],
            index=0
        )

    with col2:
        if output_format in ["JPEG", "WebP"]:
            quality = st.slider("Quality", 1, 100, 95)
        else:
            quality = 95

    # Generate download
    fmt_map = {"PNG": OutputFormat.PNG, "JPEG": OutputFormat.JPEG, "WebP": OutputFormat.WEBP}
    fmt = fmt_map[output_format]

    # Convert to bytes
    output_buffer = BytesIO()

    # Handle RGBA for JPEG
    if fmt == OutputFormat.JPEG and preview.mode == 'RGBA':
        background = Image.new('RGB', preview.size, (255, 255, 255))
        background.paste(preview, mask=preview.split()[3])
        preview = background

    save_kwargs = {"format": output_format}
    if output_format in ["JPEG", "WebP"]:
        save_kwargs["quality"] = quality
    if output_format == "PNG":
        save_kwargs["optimize"] = True

    preview.save(output_buffer, **save_kwargs)
    output_buffer.seek(0)

    # Download button
    file_ext = output_format.lower()
    output_filename = f"{Path(uploaded_file.name).stem}_{target_w}x{target_h}.{file_ext}"

    st.download_button(
        label=f"⬇️ Download {output_format}",
        data=output_buffer,
        file_name=output_filename,
        mime=f"image/{file_ext}",
        use_container_width=True
    )

    # === Batch Export ===
    st.divider()

    with st.expander("📦 Batch Export All Sizes"):
        st.write(f"Export all **{platform.title()}** sizes at once")

        if st.button(f"Generate All {platform.title()} Sizes", use_container_width=True):
            with st.spinner("Generating all sizes..."):
                # Create zip file in memory
                zip_buffer = BytesIO()

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for preset_name, (w, h) in SIZE_PRESETS[platform].items():
                        # Resize
                        resized = optimizer.resize(source_image.copy(), w, h, strategy)

                        # Handle RGBA for JPEG
                        if fmt == OutputFormat.JPEG and resized.mode == 'RGBA':
                            bg = Image.new('RGB', resized.size, (255, 255, 255))
                            bg.paste(resized, mask=resized.split()[3])
                            resized = bg

                        # Save to buffer
                        img_buffer = BytesIO()
                        resized.save(img_buffer, format="PNG", optimize=True)
                        img_buffer.seek(0)

                        # Add to zip
                        zf.writestr(f"{preset_name}_{w}x{h}.png", img_buffer.getvalue())

                zip_buffer.seek(0)

                st.download_button(
                    label=f"⬇️ Download All {platform.title()} Sizes (ZIP)",
                    data=zip_buffer,
                    file_name=f"{Path(uploaded_file.name).stem}_{platform}_all_sizes.zip",
                    mime="application/zip",
                    use_container_width=True
                )

                st.success(f"✅ Generated {len(SIZE_PRESETS[platform])} images!")


if __name__ == "__main__":
    main()
