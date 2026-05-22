import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Page Config
st.set_page_config(
    page_title="MediScan",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 MediScan - Medical Report Reader")
st.markdown("Upload PDF, JPG, JPEG or PNG medical reports.")

uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf", "jpg", "jpeg", "png"]
)

def generate_summary(text):

    summary = []

    keywords = [
        "hemoglobin",
        "glucose",
        "sugar",
        "cholesterol",
        "platelet",
        "wbc",
        "rbc",
        "vitamin",
        "thyroid",
        "creatinine",
        "bilirubin"
    ]

    for item in keywords:
        if item.lower() in text.lower():
            summary.append(item.title())

    if summary:
        return "Detected Parameters: " + ", ".join(summary)
    else:
        return "No major parameters automatically detected."

if uploaded_file:

    extracted_text = ""

    # PDF Processing
    if uploaded_file.type == "application/pdf":

        with st.spinner("Reading PDF..."):

            pages = convert_from_bytes(uploaded_file.read())

            for page in pages:
                text = pytesseract.image_to_string(page)
                extracted_text += text + "\n"

    # Image Processing
    else:

        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Uploaded Report")

        extracted_text = pytesseract.image_to_string(image)

    st.success("Report Processed Successfully")

    st.subheader("📄 Extracted Text")

    st.text_area(
        "Report Content",
        extracted_text,
        height=400
    )

    st.subheader("🩺 Quick Summary")

    st.info(generate_summary(extracted_text))

    st.download_button(
        label="Download Extracted Text",
        data=extracted_text,
        file_name="report_text.txt",
        mime="text/plain"
    )