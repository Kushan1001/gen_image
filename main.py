import streamlit as st
import requests
import json
from io import BytesIO

# Apply custom CSS styling
st.markdown("""
    <style>
    /* Background color and general padding */
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        font-family: Arial, sans-serif;
    }

    /* Centered header styling */
    .centered-header {
        text-align: center;
        font-size: 2.5em;
        color: #1f77b4;
        margin-top: 20px;
        font-weight: bold;
    }

    /* Button styling */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 1em;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #105a8a;
        color: #e2f0fb;
    }

    /* Sidebar customization */
    .sidebar .sidebar-content {
        background-color: #2d3338;
        color: white;
        padding: 20px;
        border-radius: 10px;
    }

    /* Custom text styling */
    .custom-text {
        font-size: 1.1em;
        color: #333333;
        line-height: 1.6;
    }

    /* Input fields styling */
    .stTextInput > div, .stTextArea > div {
        border-radius: 8px;
        background-color: #e3eaf2;
        color: #333333;
        font-size: 1em;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header for the app
st.markdown('<div class="centered-header">Generate an Image</div>', unsafe_allow_html=True)

# Prompt input for the image generation
title = st.text_input("Enter your prompt to generate an image", key="prompt_input")

# Placeholder for displaying image and download button
image_placeholder = st.empty()
download_placeholder = st.empty()
generate_again_button = st.empty()

def generate_image(prompt):
    """Function to send prompt to the image generation API and display the result."""
    data = {"text": prompt}
    response = requests.post('https://image-gen-rgn0.onrender.com/generate_image', json=data)
    
    if response.status_code == 200:
        if response.text:
            try:
                json_response = json.loads(response.text)
                image_url = json_response.get("response")
                if image_url:
                    # Display the generated image
                    image_placeholder.image(image_url, caption="Generated Image", use_container_width=True)

                    # Fetch image content for download
                    image_data = requests.get(image_url).content
                    image_file = BytesIO(image_data)

                    # Provide a download button
                    download_placeholder.download_button(
                        label="Download Image",
                        data=image_file,
                        file_name="generated_image.png",
                        mime="image/png"
                    )

                    # Display "Generate Again" button
                    if generate_again_button.button("Generate Again"):
                        generate_image(prompt)
                else:
                    st.warning("Image generation failed. Please try again.")
            except json.JSONDecodeError:
                st.error("Failed to parse JSON response from the server.")
        else:
            st.warning("The server returned an empty response.")
    else:
        st.error(f"Image generation failed with status code: {response.status_code}")

# Generate Image on button click
if st.button("Generate Image"):
    if title:
        generate_image(title)
    else:
        st.warning("Please enter a prompt before generating an image.")
