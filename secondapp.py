import streamlit as st
import os
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64
import time

# Set page configuration
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🔮",
    layout="centered"
)

# Custom CSS to style the app
st.markdown("""
<style>
    .main {
        background-color: #f0f0f0;
    }
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle {
        font-size: 24px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #333;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        width: 100%;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Function to generate mandala using DALL-E 3
def generate_mandala(prompt):
    client = OpenAI(api_key=st.session_state.openai_api_key)
    
    # Create a detailed prompt for the mandala
    detailed_prompt = f"Create a detailed, intricate, black and white mandala design inspired by the concept of '{prompt}'. The mandala should be symmetrical, meditative, and feature patterns related to {prompt}. Use only black and white with high contrast."
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=detailed_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        return image
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

# Function to convert PIL Image to downloadable format
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download {text}</a>'
    return href

# Title and description
st.markdown('<p class="title">✨ Black & White Mandala Generator ✨</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform a word into a beautiful mandala design</p>', unsafe_allow_html=True)

# Initialize session state for the API key
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""
if 'mandala_image' not in st.session_state:
    st.session_state.mandala_image = None

# API key input
api_key = st.text_input("Enter your OpenAI API Key:", type="password", value=st.session_state.openai_api_key)
if api_key:
    st.session_state.openai_api_key = api_key

# Only show the rest if API key is provided
if st.session_state.openai_api_key:
    # Input for the inspiration word
    inspiration_word = st.text_input("Enter a word for inspiration:", placeholder="e.g. ocean, harmony, forest")
    
    # Generate button
    if st.button("Generate Mandala"):
        if inspiration_word:
            with st.spinner(f"Creating a mandala inspired by '{inspiration_word}'..."):
                # Show a loading message
                start_time = time.time()
                
                # Generate the mandala
                image = generate_mandala(inspiration_word)
                
                if image:
                    st.session_state.mandala_image = image
                    generation_time = time.time() - start_time
                    st.success(f"Mandala generated in {generation_time:.2f} seconds!")
                else:
                    st.error("Failed to generate mandala. Please try again.")
        else:
            st.warning("Please enter an inspiration word.")
    
    # Display the generated image
    if st.session_state.mandala_image:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(st.session_state.mandala_image, caption=f"Mandala inspired by your input", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download link
        st.markdown(get_image_download_link(st.session_state.mandala_image, f"mandala_{inspiration_word}.png", "Mandala"), unsafe_allow_html=True)
else:
    st.info("Please enter your OpenAI API key to start generating mandalas.")

# Footer
st.markdown("---")
st.caption("Created with Streamlit and OpenAI DALL-E 3. This app transforms your inspiration into black and white mandala art.")
