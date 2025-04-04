
# ✅ REAL app.py with visual Shopify + Amazon sections

import streamlit as st
import pandas as pd
import openpyxl
import os
import json
import requests
import re

st.set_page_config(page_title="North Fork Launcher", layout="centered")
st.title("North Fork Launcher")

CREDENTIALS_FILE = "stored_credentials.json"

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_credentials(data):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)

creds = load_credentials()

with st.expander("Enter & Save API Credentials"):
    st.subheader("Shopify")
    shop_domain = st.text_input("Shopify Store URL", value=creds.get("shopify_domain", ""))
    shop_token = st.text_input("Shopify Admin API Token", type="password", value=creds.get("shopify_token", ""))

    st.subheader("Amazon")
    seller_id = st.text_input("Amazon Seller ID", value=creds.get("seller_id", ""))
    marketplace_id = st.text_input("Marketplace ID", value=creds.get("marketplace_id", "ATVPDKIKX0DER"))
    client_id = st.text_input("Amazon LWA Client ID", value=creds.get("client_id", ""))
    client_secret = st.text_input("Amazon LWA Client Secret", type="password", value=creds.get("client_secret", ""))
    refresh_token = st.text_input("Amazon Refresh Token", type="password", value=creds.get("refresh_token", ""))

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

with st.expander("Test API Credentials"):
    if st.button("Test Shopify"):
        if shop_domain and shop_token:
            url = f"https://{shop_domain}/admin/api/2023-07/shop.json"
            headers = {"X-Shopify-Access-Token": shop_token}
            try:
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    st.success("✅ Shopify credentials are valid!")
                else:
                    st.error(f"❌ Shopify error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Test Amazon"):
        if client_id and client_secret and refresh_token:
            try:
                res = requests.post("https://api.amazon.com/auth/o2/token", data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": client_id,
                    "client_secret": client_secret
                })
                if res.status_code == 200:
                    st.success("✅ Amazon credentials are valid!")
                else:
                    st.error(f"❌ Amazon error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")

dry_run = st.checkbox("DRY RUN (no live upload)", value=True)
uploaded_file = st.file_uploader("Upload your mockup PNG", type=["png"])

if uploaded_file:
    filename_raw = uploaded_file.name.replace(".png", "").replace("-mockup", "").strip()
    filename_base = filename_raw.replace(" ", "").lower()
    formatted_title = filename_raw.replace("-", " ").title()
    handle = f"{filename_base}baby-bodysuit-clothes-bodysuit-newborn"
    product_title = f"{formatted_title} - Baby Bodysuit Clothes Bodysuit Newborn"
    image_url = f"https://cdn.shopify.com/s/files/1/placeholder/{filename_base}.png"

    st.subheader("✅ Shopify Spreadsheet")
    try:
        shopify_path = "templates/Baby Onesie Shopify Flat File.csv"
        df = pd.read_csv(shopify_path)
        df.loc[1, 'Handle'] = handle
        df.loc[1, 'Title'] = product_title
        df.loc[1, 'Image Src'] = image_url
        output_csv = f"{filename_base}_Shopify.csv"
        df.to_csv(output_csv, index=False)
        st.success("✅ Shopify spreadsheet generated!")
        with open(output_csv, "rb") as f:
            st.download_button("Download Shopify CSV", f, file_name=output_csv)
    except Exception as e:
        st.error(f"Shopify file error: {e}")

    st.subheader("✅ Amazon Spreadsheet")
    try:
        amazon_path = "templates/Baby Onesie Amazon Flat File.xlsm"
        wb = openpyxl.load_workbook(amazon_path)
        ws = wb.active
        parent_sku = f"{filename_base}-Parent"

        for row in range(4, 32):
            ws[f"A{row}"] = "leotard"
            if row == 4:
                ws[f"B{row}"] = parent_sku
                ws[f"AE{row}"] = ""
            else:
                ws[f"B{row}"] = f"{filename_base}-Var{row-4}"
                ws[f"AE{row}"] = parent_sku
            ws[f"E{row}"] = product_title
            ws[f"T{row}"] = image_url

        amazon_output = f"{filename_base}_Amazon.xlsm"
        wb.save(amazon_output)
        st.success("✅ Amazon spreadsheet generated!")
        with open(amazon_output, "rb") as f:
            st.download_button("Download Amazon Flat File", f, file_name=amazon_output)
    except Exception as e:
        st.error(f"Amazon file error: {e}")

    st.subheader("Submit to Shopify + Amazon")
    if st.button("Submit Live"):
        if dry_run:
            st.warning("DRY RUN is ON — no live submission.")
        else:
            st.success("Live submission would execute here.")
else:
    st.info("Upload a PNG file to begin.")
