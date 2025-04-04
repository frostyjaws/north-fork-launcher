import streamlit as st
import pandas as pd
import openpyxl
import xlwings as xw
from openpyxl import load_workbook
import os

# Constants
SHOPIFY_TEMPLATE_PATH = "templates/Baby Onesie Shopify Flat File.csv"
AMAZON_TEMPLATE_PATH = "templates/Baby Onesie Amazon Flat File.xlsm"
SHOPIFY_OUTPUT_PATH = "shopify_csvs/output_shopify.csv"
AMAZON_OUTPUT_PATH = "amazon_flatfiles/output_amazon.xlsm"

# Helper function to get filename
def extract_filename_no_ext(filename):
    return Path(filename).stem.replace(" ", "").replace(".", "")

# Generate Shopify spreadsheet
def generate_shopify(filename, image_url):
    df = pd.read_csv(SHOPIFY_TEMPLATE_PATH)
    handle = extract_filename_no_ext(filename).lower() + "-baby-bodysuit-clothes-bodysuit-newborn"
    title = Path(filename).stem + " - Baby Bodysuit Clothes Bodysuit Newborn"

    df.at[1, "Handle"] = handle
    df.at[1, "Title"] = title
    df.at[1, "Image Src"] = image_url

    # Clear all rows from 3 downward for columns A and B
    df.loc[2:, "Handle"] = ""
    df.loc[2:, "Title"] = ""

    df.to_csv(SHOPIFY_OUTPUT_PATH, index=False)

# Generate Amazon spreadsheet
def generate_amazon(filename, image_url):
    wb = load_workbook(AMAZON_TEMPLATE_PATH, keep_vba=True)
    ws = wb.active

    parent_sku = extract_filename_no_ext(filename) + "-Parent"
    base_sku = extract_filename_no_ext(filename)
    title = Path(filename).stem + " - Baby Bodysuit Clothes Bodysuit Newborn"

    # Row 4 is parent
    ws["A4"].value = "leotard"
    ws["B4"].value = parent_sku
    ws["E4"].value = title
    ws["T4"].value = image_url
    ws["AE4"].value = ""

    # Rows 5–31 are variations
    for row in range(5, 32):
        variation = ws[f"B{row}"].value
        if variation:
            ws[f"A{row}"].value = "leotard"
            ws[f"B{row}"].value = f"{base_sku}{variation}"
            ws[f"E{row}"].value = title
            ws[f"T{row}"].value = image_url
            ws[f"AE{row}"].value = parent_sku

    wb.save(AMAZON_OUTPUT_PATH)

# Streamlit UI
st.title("North Fork Launcher")

with st.expander("Enter & Save API Credentials"):
    st.text_input("Shopify API Key")
    st.text_input("Amazon LWA Client ID")
    st.text_input("Amazon LWA Client Secret")
    st.button("Save Credentials")

st.button("Test API Credentials")
dry_run = st.checkbox("DRY RUN (no live upload)", value=True)

uploaded_file = st.file_uploader("Upload your mockup PNG", type="png")

if uploaded_file:
    st.success("Mockup uploaded: " + uploaded_file.name)
    mockup_url = f"https://cdn.mockcdn.com/{uploaded_file.name}"  # fake placeholder

    # Process files
    generate_shopify(uploaded_file.name, mockup_url)
    st.success("Shopify spreadsheet generated")
    with open(SHOPIFY_OUTPUT_PATH, "rb") as f:
        st.download_button("Download Shopify CSV", f, file_name="shopify.csv")

    generate_amazon(uploaded_file.name, mockup_url)
    st.success("Amazon spreadsheet generated")
    with open(AMAZON_OUTPUT_PATH, "rb") as f:
        st.download_button("Download Amazon XLSM", f, file_name="amazon.xlsm")
