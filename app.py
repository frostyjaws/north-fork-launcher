
import streamlit as st
import os

st.set_page_config(page_title="North Fork Launcher", layout="centered")

st.title("North Fork Launcher")
st.write("Drag and drop a mockup PNG to begin.")

uploaded_file = st.file_uploader("Upload mockup", type=["png"])

if uploaded_file:
    filename = uploaded_file.name
    st.success(f"Uploaded: {filename}")
    st.write("Here is where the Shopify + Amazon generation and submission would happen.")
