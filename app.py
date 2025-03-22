import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size: 3rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
        background: linear-gradient(90deg, #FF7E5F, #FEB47B);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4b6cb7, #182848);
        color: white !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #FF7E5F, #FEB47B);
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #FEB47B, #FF7E5F);
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background: linear-gradient(90deg, #4b6cb7, #182848);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to analyze image
def analyze_image(img_array):
    try:
        analysis = DeepFace.analyze(img_array, actions=['gender', 'emotion'], enforce_detection=False)
        return analysis[0]
    except Exception as e:
        return {"error": str(e)}

# Set page title and favicon
st.set_page_config(page_title="Gender & Emotion Recognition", page_icon="😊")

# Title with gradient background
st.markdown('<div class="title">🎭 Gender and Emotion Recognition</div>', unsafe_allow_html=True)
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
                st.metric(label="**🧑 Gender**", value=analysis_result['gender'])
                st.metric(label="**😊 Dominant Emotion**", value=analysis_result['dominant_emotion'])

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

# Footer
st.markdown('<div class="footer">© 2023 Gender & Emotion Recognition App</div>', unsafe_allow_html=True)
