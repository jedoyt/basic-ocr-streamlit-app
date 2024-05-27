# Library for Web App UI
import streamlit as st
# Main library for OCR
import pytesseract
# Libraries for reading/displaying images
from PIL import Image
import cv2
import matplotlib.pyplot as plt
# Library for converting pages of a pdf file into images
import pdf2image

import tempfile
import pyperclip


### WEB APP USER-INTERFACE SECTION ###
### TITLE
st.title("Basic OCR App")
### SOME CONTENT
st.write("A simple web app for reading scanned documents in pdf or in image format simply drag a file on the upload section for the app to return an output")
st.write("OCR - Optical Character Recognition")
### FILE UPLOAD
uploaded_file  = st.file_uploader("Choose a file that contains scanned image(s) with texts", type=['jpg', 'png', 'pdf'])
output_str = ""
text_box_label = "Output textbox"
image_object = ""
slider_max_page_val = 10

if uploaded_file is not None:
    text_box_label = f"File found: {uploaded_file.name}."

    if uploaded_file.name[-3:] == 'pdf':
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(uploaded_file.read())
            temp_pdf_path = temp_pdf.name
        # output_str = "Output is expected here!"
        pages = pdf2image.convert_from_path(temp_pdf_path)
        slider_max_page_val = len(pages)
        page_no = st.slider("Toggle pages",value=0, max_value=slider_max_page_val)
        st.write(f"Page Index: {page_no}")
        output_str = pytesseract.image_to_string(pages[page_no])
        st.image(pages[page_no])
    else:
        img = Image.open(uploaded_file)
        image_object = img
        output_str = pytesseract.image_to_string(img)
        st.image(image_object)
else:
    output_str = "No file uploaded."

### BUTTON1
button1 = st.button("Copy Output Text")
if button1:
    pyperclip.copy(output_str)

### OUTPUT TEXTBOX
text_box = st.text_area(text_box_label, output_str, height=720)