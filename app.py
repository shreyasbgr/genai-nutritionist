from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import os
import io
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
from PIL import Image
import warnings
warnings.filterwarnings("ignore", message="ALTS: Platforms other than Linux and Windows are not supported")

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_prompt, image])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(bytes_data))
        # st.image(image, caption='Uploaded Image', use_column_width=True)
        
        image_part = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit app
st.set_page_config(page_title="Gemini Nutritionist App")
st.header("Gemini GenAI Nutritionist App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image_part = input_image_setup(uploaded_file)
    
    # Convert image part to PIL image and display it
    if image_part['mime_type'] in ['image/jpeg', 'image/png']:
        image = Image.open(io.BytesIO(image_part['data']))
        st.image(image, caption='Processed Image', use_column_width=True)
else:
    st.write("Please upload an image file.")

submit = st.button("Tell me the nutrition information in the image")

input_prompt = """
You are an expert nutritionist. You need to see food items from the image and calculate
the total calories, and also provide the details of every food items with calorie intake in
the following format:

1. Item1 - No. of calories
2. Item2 - No. of calories
..
..
..

Finally you can also mention whether the food is health or not and
also mention the percentage split of the carbohydrates, fats, fibres, sugar, 
and other important things required in the diet.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("The response is:")
    st.write(response)