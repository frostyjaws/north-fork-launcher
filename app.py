
# North Fork Launcher - Final Version with Amazon + Shopify Fixes

import streamlit as st
import pandas as pd
import os

# Utility to format handle and title from filename
def format_handle_and_title(filename):
    base = filename.replace(".png", "").replace(" ", "")
    title = filename.replace(".png", "").replace("-", " ").title()
    handle = f"{base.lower()}baby-bodysuit-clothes-bodysuit-newborn"
    title_fmt = f"{title} - Baby Bodysuit Clothes Bodysuit Newborn"
    return handle, title_fmt

# Load templates
SHOPIFY_TEMPLATE = "/mnt/data/Baby Onesie Shopify Flat File.csv"
AMAZON_TEMPLATE = "/mnt/data/Baby Onesie Amazon Flat File.xlsx"

# File uploader
uploaded_file = st.file_uploader("Upload your mockup PNG", type=["png"])
if uploaded_file:
    file_name = uploaded_file.name
    handle, title = format_handle_and_title(file_name)

    # --- SHOPIFY CSV ---
    df = pd.read_csv(SHOPIFY_TEMPLATE)

    # Update rows 2–9 only
    for i in range(1, 10):  # Rows 2–10 in Excel
        if i == 1:
            df.iloc[i, 0] = handle  # Column A
            df.iloc[i, 1] = title   # Column B
        elif i > 1 and i < 9:
            df.iloc[i, 0] = handle
            df.iloc[i, 1] = title

    shopify_output = f"/mnt/data/{file_name.replace('.png', '')}_Shopify.csv"
    df.to_csv(shopify_output, index=False)
    st.success("Shopify CSV generated")
    st.download_button("Download Shopify CSV", data=open(shopify_output, "rb"), file_name="shopify.csv")

    # --- AMAZON FLAT FILE ---
    try:
        amazon_df = pd.read_excel(AMAZON_TEMPLATE, sheet_name=0)

        parent_sku = f"{file_name.replace('.png', '')}-Parent"
        variation_base = file_name.replace(".png", "").replace(" ", "")

        for i in range(27):
            row_idx = i + 4  # Rows 5–31
            size = amazon_df.at[row_idx, "size_name"]
            color = amazon_df.at[row_idx, "color_name"]
            sleeve = amazon_df.at[row_idx, "sleeve_type"]
            sku = f"{variation_base}{size}{color}{sleeve}"
            amazon_df.at[row_idx, "item_sku"] = sku
            amazon_df.at[row_idx, "item_name"] = title
            amazon_df.at[row_idx, "main_image_url"] = "https://cdn.shopify.com/s/yourmockupurl.png"

        amazon_df.at[3, "item_sku"] = parent_sku
        amazon_df.at[3, "item_name"] = title
        amazon_df.at[3, "main_image_url"] = "https://cdn.shopify.com/s/yourmockupurl.png"

        amazon_output = f"/mnt/data/{file_name.replace('.png', '')}_Amazon.xlsx"
        amazon_df.to_excel(amazon_output, index=False)
        st.success("Amazon Flat File generated")
        st.download_button("Download Amazon Flat File", data=open(amazon_output, "rb"), file_name="amazon.xlsx")
    except Exception as e:
        st.error(f"Amazon file generation failed: {e}")
