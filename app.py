import streamlit as st
import torch
from model.model import load_resources, translate

# Page configuration
st.set_page_config(
    page_title="Arabic to English Translator",
    page_icon="🌍",
    layout="centered"
)

# Simplified Clean CSS
st.markdown("""
<style>
    /* Modern and clean styling */
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    .main-header {
        color: #1E3A8A;
        margin-bottom: 25px;
        text-align: center;
    }
    .translator-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .output-container {
        background-color: #F9FAFB;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.2);
    }
    
    /* Language indicators */
    .language-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
        gap: 10px;
    }
    .language-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .ar-badge {
        background-color: #E5E7EB;
        color: #374151;
    }
    .en-badge {
        background-color: #3B82F6;
        color: white;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 40px;
        padding: 15px;
        text-align: center;
        font-size: 0.9rem;
        color: #6B7280;
        background-color: #F9FAFB;
        border-radius: 10px;
    }
    .contributor {
        display: inline-block;
        margin: 5px 15px;
        text-align: center;
    }
    .linkedin-link {
        color: #3B82F6;
        text-decoration: none;
        font-weight: 500;
        display: block;
        margin-top: 3px;
    }
    .linkedin-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-header'>🌍 Arabic to English Translator</h1>", unsafe_allow_html=True)

# Language indicator
st.markdown("""
<div class="language-indicator">
    <span class="language-badge ar-badge">Arabic</span>
    <span>➡️</span>
    <span class="language-badge en-badge">English</span>
</div>
""", unsafe_allow_html=True)

# Load the model and resources (cached to prevent reloading)
@st.cache_resource
def load_translation_resources():
    with st.spinner("Loading translation model..."):
        try:
            return load_resources()
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return None

# Main translator container
st.markdown("<div class='translator-container'>", unsafe_allow_html=True)

# Simple instructions
st.markdown("#### How to use")
st.markdown("Type or paste Arabic text in the box below and click 'Translate'")

# Load resources
resources = load_translation_resources()

if resources:
    model, src_tokenizer, tgt_tokenizer, device = resources
    
    # Input text area for Arabic text
    arabic_text = st.text_area(
        "Enter Arabic text:",
        placeholder="اكتب النص العربي هنا...", 
        height=120
    )
    
    # Buttons in a more compact layout
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        translate_button = st.button("Translate")
    with col2:
        clear_button = st.button("Clear")
    
    if clear_button:
        st.session_state.arabic_text = ""
        st.session_state.translation = None
        st.rerun()
    
    if translate_button and arabic_text:
        with st.spinner("Translating..."):
            try:
                english_translation = translate(model, arabic_text, src_tokenizer, tgt_tokenizer, device)
                st.session_state.translation = english_translation
            except Exception as e:
                st.error(f"Translation error: {str(e)}")
    
    # Display translation result
    if 'translation' in st.session_state and st.session_state.translation:
        st.markdown("<div class='output-container'>", unsafe_allow_html=True)
        st.markdown("#### Translation Result:")
        st.write(st.session_state.translation)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Failed to load translation model. Please check the console for errors.")

st.markdown("</div>", unsafe_allow_html=True)

# Simplified sidebar
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This app translates Arabic text to English using a Transformer neural network model.
    
    **Model Details:**
    - Transformer architecture
    - 4 encoder/decoder layers
    - 8 attention heads
    - 512 model dimension
    """)

# Updated footer with new contributors
st.markdown("""
<div class="footer">
    <h4>Contributors</h4>
    <div>
        <div class="contributor">
            <strong>M Husnain</strong>
            <a href="https://www.linkedin.com/in/m-husnain-6b94b6279/" class="linkedin-link" target="_blank">LinkedIn Profile</a>
        </div>
        <div class="contributor">
            <strong>Marwa Shahid</strong>
            <a href="https://www.linkedin.com/in/marwashahid/" class="linkedin-link" target="_blank">LinkedIn Profile</a>
        </div>
    </div>
    <p style="margin-top: 15px;">© 2025 Arabic-English Neural Machine Translation</p>
</div>
""", unsafe_allow_html=True)