import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

# ----------------------------------------
# Load Local Model (NO API)
# ----------------------------------------
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    model = AutoModelForCausalLM.from_pretrained(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    return tokenizer, model

tokenizer, model = load_model()

# ----------------------------------------
# Templates
# ----------------------------------------
TEMPLATES = {
    "Casual": "Write a casual friendly email about: {prompt}",
    "Formal": "Write a formal business email about: {prompt}",
    "Apology": "Write a sincere apology email for: {prompt}",
    "Request": "Write a polite request email regarding: {prompt}",
    "Complaint": "Write a professional complaint email about: {prompt}",
}

# ----------------------------------------
# Generate Email (Local LLM)
# ----------------------------------------
def generate_email(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=250,
        temperature=0.7,
        do_sample=True,
        top_k=50
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

# ----------------------------------------
# PDF Export
# ----------------------------------------
def download_pdf(text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = [Paragraph(text.replace("\n", "<br/>"), styles["Normal"])]
    doc.build(story)
    buffer.seek(0)
    return buffer

# ----------------------------------------
# DOCX Export
# ----------------------------------------
def download_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ----------------------------------------
# Streamlit UI
# ----------------------------------------
st.title("📧 Offline AI Email Generator (No API Needed)")
st.write("Powered by TinyLlama — fully offline, no keys, no cost.")

prompt = st.text_input("Email Purpose")
recipient = st.text_input("Recipient Name")
sender = st.text_input("Your Name")
position = st.text_input("Your Position")

template_choice = st.selectbox("Choose Email Template", list(TEMPLATES.keys()))

if st.button("Generate Email"):
    if not prompt or not recipient or not sender:
        st.error("Please fill all fields.")
    else:
        template = TEMPLATES[template_choice]
        full_prompt = template.format(prompt=prompt)

        email_body = generate_email(full_prompt)

        st.subheader("Generated Email")
        st.text_area("Email Output", value=email_body, height=300)

        col1, col2 = st.columns(2)

        with col1:
            pdf = download_pdf(email_body)
            st.download_button("Download PDF", pdf, "email.pdf")

        with col2:
            docx = download_docx(email_body)
            st.download_button("Download DOCX", docx, "email.docx")
