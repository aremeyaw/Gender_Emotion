import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Set page title and favicon (MUST BE FIRST)
st.set_page_config(page_title="Facial Analysis Hub", page_icon="🎭")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .stProgress>div>div>div>div {
        background-color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to analyze image
def analyze_image(img_array):
    try:
        analysis = DeepFace.analyze(img_array, actions=['gender', 'emotion'], enforce_detection=False)
        return analysis[0]
    except Exception as e:
        return {"error": str(e)}

# Title and description
st.markdown("<p class='big-font'>Facial Analysis Hub 🎭</p>", unsafe_allow_html=True)
st.markdown("""
    Upload an image, and this app will analyze the gender and emotions of the faces in the image using **DeepFace**.
    """)

# Sidebar for additional information
with st.sidebar:
    st.header("About")
    st.markdown("""
        This app uses the **DeepFace** library to analyze:
        - **Gender**: Male or Female
        - **Emotion**: Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral
        """)
    st.markdown("---")
    st.markdown("Built with ❤️ by [Your Name]")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

if uploaded_file is not None:
    # Read and display the image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    st.image(img, caption="Uploaded Image.", use_container_width=True)

    # Analyze button
    if st.button('Analyze Image 🚀'):
        with st.spinner("Analyzing the image... Please wait."):
            analysis_result = analyze_image(img)

        if "error" in analysis_result:
            st.error(f"Error: {analysis_result['error']}")
        else:
            # Display results in columns
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"<p style='color:green; font-size: 20px;'><b>Gender:</b> {analysis_result['gender'].capitalize()} </p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:blue; font-size: 20px;'><b>Dominant Emotion:</b> {analysis_result['dominant_emotion'].capitalize()} </p>", unsafe_allow_html=True)

            with col2:
                # Plot emotion probabilities as an interactive bar chart
                st.write("**Emotion Probabilities:**")
                emotions = list(analysis_result["emotion"].keys())
                probabilities = list(analysis_result["emotion"].values())

                fig = go.Figure(data=[go.Bar(x=emotions, y=probabilities, marker_color='skyblue')])
                fig.update_layout(xaxis_title="Emotion", yaxis_title="Probability")
                st.plotly_chart(fig, use_container_width=True)

            # Display raw emotion probabilities with progress bars
            st.markdown("**Detailed Emotion Probabilities:**")
            for emotion, probability in analysis_result["emotion"].items():
                st.write(f"- {emotion.capitalize()}: {probability:.2f}%")
                st.progress(probability / 1.0)
