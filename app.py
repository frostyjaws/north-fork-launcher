
import streamlit as st

st.set_page_config(page_title="North Fork Launcher", layout="centered")

st.title("North Fork Launcher")
st.write("Upload a mockup PNG and generate product files for Shopify and Amazon.")

# DRY_RUN toggle
dry_run = st.checkbox("DRY RUN (Test Mode)", value=True)

# Upload file
uploaded_file = st.file_uploader("Upload your mockup PNG", type=["png"])

if uploaded_file:
    filename = uploaded_file.name
    st.success(f"Uploaded: {filename}")
    
    # Show options
    st.write("### What would you like to do?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Shopify CSV"):
            st.info("Shopify CSV logic would run here...")

    with col2:
        if st.button("Generate Amazon Flat File"):
            st.info("Amazon Flat File logic would run here...")

    if st.button("Submit to Shopify + Amazon"):
        if dry_run:
            st.warning("DRY RUN: Submission simulated.")
        else:
            st.success("Live submission logic would trigger here.")
else:
    st.info("Drag and drop a PNG file above to get started.")
