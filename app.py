import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# Configure Streamlit page
st.set_page_config(
    page_title="AI Fashion Designer",
    page_icon="🛍️",
    layout="centered"
)

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        color: #FF4081;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4081;
        color: white;
        border-radius: 10px;
        font-size: 1.2rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🛍️ AI Fashion Designer</h1>", unsafe_allow_html=True)
st.markdown("### Create Stunning Custom Fashion with AI! ✨")

# Input Fields
prompt = st.text_area("Describe your fashion design:", placeholder="Example: A pastel saree with floral embroidery")

col1, col2 = st.columns(2)
with col1:
    clothing_type = st.selectbox(
        "Select Clothing Type:",
        ["T-Shirt", "Hoodie", "Jacket", "Jeans", "Dress", "Sweater", "Saree", "Frock", "Girls' Fabric Design", "Bridal Dress"]
    )
with col2:
    quality = st.select_slider(
        "Image Quality:",
        options=["Standard", "High", "Ultra"],
        value="High"
    )

# Image Generation Function
def generate_clothing_design(prompt, clothing_type):
    try:
        base_url = "https://image.pollinations.ai/prompt/"
        enhanced_prompt = f"{clothing_type}, {prompt}, high-quality fashion design, detailed fabric texture, model wearing it, runway style"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        image_url = f"{base_url}{encoded_prompt}"
        
        response = requests.get(image_url, timeout=15)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content)), None
        else:
            return None, f"Error: {response.status_code}"
    except Exception as e:
        return None, str(e)

# Generate Button
if st.button("👗 Generate Fashion Design"):
    if not prompt:
        st.error("Please enter a description for your design!")
    else:
        with st.spinner("✨ Creating your unique fashion design..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            if quality == "High":
                prompt += ", high quality, detailed"
            elif quality == "Ultra":
                prompt += ", ultra high quality, extremely detailed, 4K, professional photography"
            
            generated_image, error = generate_clothing_design(prompt, clothing_type)
            
            if error:
                st.error(f"Generation failed: {error}")
            elif generated_image:
                st.image(generated_image, caption=f"{clothing_type} Design", use_column_width=True)
                
                img_bytes = io.BytesIO()
                generated_image.save(img_bytes, format='PNG')
                st.download_button(
                    label="📥 Download Your Design",
                    data=img_bytes.getvalue(),
                    file_name=f"custom_fashion_{clothing_type}.png",
                    mime="image/png"
                )
                st.success("✨ Your fashion design is ready!")

# Upload Section
st.markdown("## 📤 Upload Your Own Fashion Image")
uploaded_file = st.file_uploader("Upload an image to customize:", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully! You can now apply transformations.")