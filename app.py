import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt

# Function to analyze image
def analyze_image(img_array):
    try:
        analysis = DeepFace.analyze(img_array, actions=['gender', 'emotion'], enforce_detection=False)
        return analysis[0]
    except Exception as e:
        return {"error": str(e)}

# Set page title and favicon
st.set_page_config(page_title="Gender & Emotion Recognition", page_icon="😊", layout="centered")

# Custom styling
st.markdown("""
    <style>
        .stTitle {
            text-align: center;
        }
        .stMarkdown {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎭 Gender & Emotion Recognition")
st.markdown("""
    Upload an image, and this AI-powered app will analyze the **gender** and **emotions** of the faces using **DeepFace**.
    """)

# Sidebar for additional information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **This app analyzes:**
    - 👨‍💼 **Gender**: Male or Female
    - 😃 **Emotion**: Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral
    
    Built with ❤️ using **Streamlit** & **DeepFace**
    """)
    st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "png"])

if uploaded_file is not None:
    # Read and display the image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    st.image(img, caption="📷 Uploaded Image", use_container_width=True)

    # Analyze button
    if st.button('🚀 Analyze Image'):
        with st.spinner("🔍 Analyzing the image... Please wait."):
            analysis_result = analyze_image(img)

        if "error" in analysis_result:
            st.error(f"❌ Error: {analysis_result['error']}")
        else:
            # Display results in columns
            col1, col2 = st.columns(2)

            with col1:
                st.success(f"**🧑 Gender:** {analysis_result['gender']}")
                st.success(f"**😊 Dominant Emotion:** {analysis_result['dominant_emotion']}")

            with col2:
                # Plot emotion probabilities as a bar chart
                st.write("**📊 Emotion Probabilities:**")
                emotions = list(analysis_result["emotion"].keys())
                probabilities = list(analysis_result["emotion"].values())

                fig, ax = plt.subplots()
                ax.barh(emotions, probabilities, color='skyblue')
                ax.set_xlabel('Probability')
                ax.set_title('Emotion Distribution')
                st.pyplot(fig)

            # Display raw emotion probabilities
            st.markdown("### 📝 Detailed Emotion Probabilities:")
            for emotion, probability in analysis_result["emotion"].items():
                st.write(f"- {emotion.capitalize()}: {probability:.2f}%")
