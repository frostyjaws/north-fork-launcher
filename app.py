
# This is the final version of app.py with saved credential support for Shopify + Amazon

import streamlit as st
import pandas as pd
import openpyxl
import json
import os

st.set_page_config(page_title="North Fork Launcher", layout="centered")

CREDENTIALS_FILE = "stored_credentials.json"

st.title("North Fork Launcher")
st.write("Upload a mockup PNG, enter your credentials, and generate + submit your Shopify and Amazon listings.")

# Load saved credentials
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_credentials(data):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)

creds = load_credentials()

# Credential form
with st.expander("Enter & Save API Credentials"):
    st.subheader("Shopify")
    shop_domain = st.text_input("Shopify Store URL", value=creds.get("shopify_domain", ""))
    shop_token = st.text_input("Shopify Admin API Token", type="password", value=creds.get("shopify_token", ""))

    st.subheader("Amazon")
    seller_id = st.text_input("Amazon Seller ID", value=creds.get("seller_id", ""))
    marketplace_id = st.text_input("Marketplace ID", value=creds.get("marketplace_id", "ATVPDKIKX0DER"))
    client_id = st.text_input("Client ID", value=creds.get("client_id", ""))
    client_secret = st.text_input("Client Secret", type="password", value=creds.get("client_secret", ""))
    refresh_token = st.text_input("Refresh Token", type="password", value=creds.get("refresh_token", ""))

    if st.button("Save Credentials"):
        creds = {
            "shopify_domain": shop_domain,
            "shopify_token": shop_token,
            "seller_id": seller_id,
            "marketplace_id": marketplace_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }
        save_credentials(creds)
        st.success("Credentials saved successfully!")

dry_run = st.checkbox("DRY RUN (simulate submission only)", value=True)

uploaded_file = st.file_uploader("Upload your mockup PNG", type=["png"])

if uploaded_file:
    filename_base = uploaded_file.name.replace("-mockup.png", "").replace(".png", "").replace(" ", "").replace("'", "")
    display_title = uploaded_file.name.replace("-mockup.png", "").replace(".png", "")

    image_url = f"https://cdn.shopify.com/s/files/1/placeholder/{filename_base}.png"
    st.success(f"Mock image URL: {image_url}")

    try:
        shopify_df = pd.read_csv("templates/Baby Onesie Shopify Flat File.csv")
        shopify_df.loc[1, 'Handle'] = f"{filename_base}asset-1-baby-bodysuit-clothes-bodysuit-newborn"
        shopify_df.loc[1, 'Title'] = f"{display_title} - Baby Bodysuit Clothes Bodysuit Newborn"
        shopify_df.loc[1, 'Image Src'] = image_url
        shopify_csv = f"{display_title}_shopify.csv"
        shopify_df.to_csv(shopify_csv, index=False)
        with open(shopify_csv, "rb") as f:
            st.download_button("Download Shopify CSV", f, file_name=shopify_csv)
    except Exception as e:
        st.error(f"Error creating Shopify CSV: {e}")

    try:
        wb = openpyxl.load_workbook("templates/Baby Onesie Amazon Flat File.xlsx")
        ws = wb.active
        ws["B4"] = f"{filename_base}-Parent"
        ws["E4"] = f"{display_title} - Baby Bodysuit Clothes Bodysuit Newborn"
        for row in range(5, 32):
            suffix = f"Var{row-4}"
            ws[f"B{row}"] = f"{filename_base}-{suffix}"
            ws[f"E{row}"] = f"{display_title} - Baby Bodysuit Clothes Bodysuit Newborn"
            ws[f"T{row}"] = image_url
        amazon_file = f"{display_title}_amazon.xlsx"
        wb.save(amazon_file)
        with open(amazon_file, "rb") as f:
            st.download_button("Download Amazon Flat File", f, file_name=amazon_file)
    except Exception as e:
        st.error(f"Error creating Amazon flat file: {e}")

    if st.button("Submit to Shopify + Amazon"):
        if dry_run:
            st.warning("DRY RUN MODE: No live submission.")
        else:
            st.success("Live submission logic would run here.")
else:
    st.info("Upload a PNG to get started.")
