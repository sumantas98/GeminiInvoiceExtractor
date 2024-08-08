from dotenv import load_dotenv
import streamlit as st

load_dotenv()
from PIL import Image
import google.generativeai as genai
import os
import PyPDF2 as pdf

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')


def get_response_from_images(inputs, images, prompt):
    response = ''
    if inputs != '':
        response = model.generate_content([inputs, images[0], prompt])
    else:
        response = model.generate_content(images)
    return response.text


def image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_info = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_info
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


image = ''
st.set_page_config(page_title='MultiLanguage Invoice Extractor')
st.header('MultiLanguage Invoice Extractor')
inputs_ = st.text_input('Please Ask Your Queries ...')
upload_files = st.file_uploader('Choose the Invoice...', type=['jpg', 'jpeg'])

if upload_files is not None:
    image = Image.open(upload_files)
    st.image(image, caption='Upload Image', use_column_width=True)

submit = st.button('Click Me !')

input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice and you will tell all
information about the invoice.
"""

if submit:
    image_data = image_setup(upload_files)
    response = get_response_from_images(input_prompt, image_data, inputs_)
    st.subheader('The Response is')
    st.write(response)
