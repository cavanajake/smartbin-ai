import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from transformers import pipeline
import openai

# Set your OpenAI API key
openai.api_key = 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

# Load a pre-trained image classification model
classifier = pipeline("image-classification", model="microsoft/resnet-50")

# Title
st.title("♻️ SmartBin - AI Waste Classifier")
st.write("Upload a photo of an item to find out if it's recyclable, compostable, or landfill!")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")

    # Run image classification
    results = classifier(image)
    top_label = results[0]['label']
    st.write(f"**Predicted item:** {top_label}")

    # Use OpenAI to decide bin category
    prompt = f"Determine whether a '{top_label}' should go in the recycling bin, compost bin, or trash. Respond with just one word: 'Recycle', 'Compost', or 'Landfill'."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    bin_type = response["choices"][0]["message"]["content"]

    st.subheader(f"🗑 Suggested Bin: {bin_type}")

    # Explanation prompt
    explain_prompt = f"Explain why a '{top_label}' should be disposed of in the {bin_type} bin. Keep it concise."
    explanation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": explain_prompt}
        ]
    )
    st.info(explanation["choices"][0]["message"]["content"])

    # Waste saved counter (static for prototype)
    st.metric(label="🌍 Waste Diverted", value="2.5 lbs")

st.markdown("---")
st.caption("Built with Hugging Face + OpenAI + Streamlit | Cavana AI 2025")
