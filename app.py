
import streamlit as st
import pandas as pd
import openpyxl
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="North Fork Launcher", layout="centered")

st.title("North Fork Launcher")
st.write("Upload a mockup PNG, enter your credentials, and generate + submit your Shopify and Amazon listings.")

# Session state for credentials
if 'shopify_token' not in st.session_state:
    st.session_state.shopify_token = ""
if 'shopify_domain' not in st.session_state:
    st.session_state.shopify_domain = ""
if 'amazon_credentials' not in st.session_state:
    st.session_state.amazon_credentials = {}

with st.expander("Enter API Credentials"):
    st.subheader("Shopify")
    st.session_state.shopify_domain = st.text_input("Shopify Store URL (e.g. ablessingindesign.myshopify.com)", value=st.session_state.shopify_domain)
    st.session_state.shopify_token = st.text_input("Shopify Admin API Token", type="password", value=st.session_state.shopify_token)

    st.subheader("Amazon SP-API")
    st.session_state.amazon_credentials['seller_id'] = st.text_input("Seller ID", value=st.session_state.amazon_credentials.get('seller_id', ''))
    st.session_state.amazon_credentials['marketplace_id'] = st.text_input("Marketplace ID", value=st.session_state.amazon_credentials.get('marketplace_id', ''))
    st.session_state.amazon_credentials['refresh_token'] = st.text_input("Refresh Token", value=st.session_state.amazon_credentials.get('refresh_token', ''))
    st.session_state.amazon_credentials['client_id'] = st.text_input("Client ID", value=st.session_state.amazon_credentials.get('client_id', ''))
    st.session_state.amazon_credentials['client_secret'] = st.text_input("Client Secret", type="password", value=st.session_state.amazon_credentials.get('client_secret', ''))

dry_run = st.checkbox("DRY RUN (simulate everything, no live submission)", value=True)

uploaded_file = st.file_uploader("Upload your mockup PNG", type=["png"])

if uploaded_file:
    st.image(uploaded_file, caption="Mockup Preview", use_column_width=True)
    filename_base = uploaded_file.name.replace("-mockup.png", "").replace(".png", "").replace(" ", "").replace("'", "")
    display_title = uploaded_file.name.replace("-mockup.png", "").replace(".png", "")

    # Simulate Shopify image upload
    st.info("Uploading image to Shopify...")
    image_url = f"https://cdn.shopify.com/s/files/1/placeholder/{filename_base}.png"
    st.success(f"Mock image uploaded! URL: {image_url}")

    # Generate Shopify CSV
    try:
        shopify_df = pd.read_csv("templates/Baby Onesie Shopify Flat File.csv")
        shopify_df.loc[1, 'Handle'] = f"{filename_base}asset-1-baby-bodysuit-clothes-bodysuit-newborn"
        shopify_df.loc[1, 'Title'] = f"{display_title} - Baby Bodysuit Clothes Bodysuit Newborn"
        shopify_df.loc[1, 'Image Src'] = image_url
        shopify_csv = f"{display_title}_shopify.csv"
        shopify_df.to_csv(shopify_csv, index=False)
        st.success("Shopify CSV generated.")
        with open(shopify_csv, "rb") as f:
            st.download_button("Download Shopify CSV", f, file_name=shopify_csv)
    except Exception as e:
        st.error(f"Error generating Shopify CSV: {e}")

    # Generate Amazon flat file
    try:
        wb = openpyxl.load_workbook("templates/Baby Onesie Amazon Flat File.xlsx")
        ws = wb.active
        ws["B4"] = f"{filename_base}-Parent"
        ws["E4"] = f"{display_title} - Baby Bodysuit Clothes Bodysuit Newborn"
        for row in range(5, 32):
            variation_suffix = f"Var{row-4}"
            ws[f"B{row}"] = f"{filename_base}-{variation_suffix}"
            ws[f"E{row}"] = f"{display_title} - Baby Bodysuit Clothes Bodysuit Newborn"
            ws[f"T{row}"] = image_url
        amazon_file = f"{display_title}_amazon.xlsx"
        wb.save(amazon_file)
        st.success("Amazon Flat File generated.")
        with open(amazon_file, "rb") as f:
            st.download_button("Download Amazon Flat File", f, file_name=amazon_file)
    except Exception as e:
        st.error(f"Error generating Amazon flat file: {e}")

    # Simulate or submit to platforms
    if st.button("Submit to Shopify + Amazon"):
        if dry_run:
            st.warning("DRY RUN mode is ON. No real submissions were made.")
        else:
            st.success("Live submission would happen here with provided credentials.")

else:
    st.info("Upload a PNG mockup to begin.")
