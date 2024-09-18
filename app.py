import streamlit as st
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import urllib.parse

# Configure Cloudinary
cloudinary.config(
    cloud_name=st.secrets["CLOUDINARY_CLOUD_NAME"],
    api_key=st.secrets["CLOUDINARY_API_KEY"],
    api_secret=st.secrets["CLOUDINARY_API_SECRET"]
)

st.title("Product Image Variation Generator")

# File uploader for the image
uploaded_file = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])
prompt = st.text_input("Enter a prompt for background variation")
num_variations = st.number_input("Number of variations", min_value=1, max_value=10, value=1)

# Aspect ratio or custom dimensions choice
option = st.selectbox(
    "Do you want to select an aspect ratio or define custom dimensions?",
    ("Aspect Ratio", "Custom Dimensions")
)

# Choose between aspect ratio or custom size
if option == "Aspect Ratio":
    aspect_ratio = st.selectbox(
        "Select an aspect ratio",
        ("16:9 (Portrait)", "5:4", "1:1")
    )
    aspect_ratios = {
        "16:9 (Portrait)": "9:16",
        "5:4": "5:4",
        "1:1": "1:1"
    }
    selected_aspect_ratio = aspect_ratios[aspect_ratio]
    width, height = None, None
else:
    width = st.number_input("Enter the width (pixels)", min_value=1, value=800)
    height = st.number_input("Enter the height (pixels)", min_value=1, value=600)

# Button to generate variations
if st.button("Generate Variations"):
    if uploaded_file and prompt:
        try:
            # Upload the image to Cloudinary
            upload_result = cloudinary.uploader.upload(uploaded_file)
            public_id = upload_result['public_id']

            variations = []
            for _ in range(num_variations):
                transformation = {
                    'effect': f'gen_background_replace:prompt_{prompt.replace(" ", "_")}'
                }

                if option == "Aspect Ratio":
                    transformation.update({
                        'aspect_ratio': selected_aspect_ratio,
                        'crop': 'fill',
                        'gravity': 'auto',
                        'height': 1500
                    })
                else:
                    transformation.update({
                        'width': width,
                        'height': height,
                        'crop': 'fill',
                        'gravity': 'auto'
                    })

                # Generate the URL using cloudinary_url
                variation_url, _ = cloudinary_url(public_id, transformation=transformation, secure=True)
                variations.append(variation_url)

            # Display the generated URLs for debugging
            st.write("Generated Variation URLs:")
            for var in variations:
                st.write(var)

            # Display the variations (images) to the user
            for var in variations:
                st.image(var, use_column_width=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please upload an image and enter a prompt.")
