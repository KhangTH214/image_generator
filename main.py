from monsterapi import client
import cv2
import urllib
import numpy as np
import streamlit as st
import base64

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImQ5OWFkMmY0MDE0YjIxNGUzMmNkYzRlNzc2NDc2YTM3IiwiY3JlYXRlZF9hdCI6IjIwMjQtMDktMDNUMDM6Mzg6MjcuNTU1NzkyIn0.Xo9vcDRzG4Md8YgqwETvEkcz5dokHzJYLyYv-T33cIA"
# Get api key: https://monsterapi.ai/

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

def set_logo(logo_path):
    with open(logo_path, "rb") as logo_file:
        encoded_logo = base64.b64encode(logo_file.read()).decode()
    logo_style = f"""
    <style>
    .logo {{
        position: absolute;
        top: 20px;
        left: -300px; 
        width: 150px; 
        height: auto;
        z-index: 999;
    }}
    </style>
    <img class="logo" src="data:image/png;base64,{encoded_logo}" alt="Logo">
    """
    st.markdown(logo_style, unsafe_allow_html=True)

def generate(prompt, api_key):
    monster_client = client(api_key)

    model = 'sdxl-base'
    input_data = {
    'prompt': prompt,
    'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly',
    'samples': 2,
    'enhance': True,
    'optimize': True,
    'safe_filter': True,
    'steps': 50,
    'aspect_ratio': 'square',
    'guidance_scale': 7.5,
    'seed': 2414,
    }
    result = monster_client.generate(model, input_data)
    images = result['output']
    image = urllib.request.urlopen(images[0])
    arr = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    return img

set_background('images/background.jpg')
set_logo('images/WHITE.png')

st.title('Generate Image')
prompt = st.text_input(label="Type something creative...")
if st.button("Generate"):
    if prompt is not None:
        image = generate(prompt=prompt, api_key=api_key)
        st.image(image, caption="Generated Image ")
    else:
        st.write('Please write a prompt.')