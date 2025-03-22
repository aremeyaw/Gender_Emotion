import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
import tempfile
import os

# Suppress Streamlit warnings (optional)
import logging
logging.getLogger("streamlit").setLevel(logging.ERROR)

# Set the title of the app
st.title("Gender, Facial, and Emotional Expression Recognition")

# Upload image through Streamlit
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Read the image file as bytes
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    
    # Decode the image using OpenCV
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert the image from BGR to RGB for display
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Display the uploaded image
    st.image(image_rgb, caption="Uploaded Image", use_column_width=True)

    # Save the image to a temporary file for DeepFace analysis
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(file_bytes)
        tmp_file_path = tmp_file.name

    # Analyze the image using DeepFace
    try:
        # Perform gender and emotion analysis
        result = DeepFace.analyze(img_path=tmp_file_path, actions=['gender', 'emotion'], enforce_detection=False)
        
        # Display the results
        st.subheader("Analysis Results:")
        st.write(f"**Gender:** {result[0]['dominant_gender']}")
        st.write(f"**Emotion:** {result[0]['dominant_emotion']}")
        st.write(f"**Gender Confidence:** {result[0]['gender'][result[0]['dominant_gender']]:.2f}%")
        st.write(f"**Emotion Confidence:** {result[0]['emotion'][result[0]['dominant_emotion']]:.2f}%")
    
    except Exception as e:
        st.error(f"Error during analysis: {e}")

    # Clean up the temporary file
    os.unlink(tmp_file_path)
