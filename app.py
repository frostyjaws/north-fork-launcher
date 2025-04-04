
# North Fork Launcher - Final Shopify Fixes Included
# This script ensures:
# - Row 2 of column A and B in the Shopify CSV follow the same logic as rows 3–11
# - All values are derived from the uploaded PNG filename

import pandas as pd
import os

def format_handle(filename):
    return filename.lower().replace(" ", "") + "baby-bodysuit-clothes-bodysuit-newborn"

def format_title(filename):
    return filename.title() + " - Baby Bodysuit Clothes Bodysuit Newborn"

def update_shopify_csv(csv_path, filename):
    df = pd.read_csv(csv_path)

    handle = format_handle(filename)
    title = format_title(filename)

    df.loc[1, 'Handle'] = handle  # Row 2 (index 1)
    df.loc[1, 'Title'] = title    # Row 2 (index 1)

    # Save updated file
    updated_path = os.path.join(os.path.dirname(csv_path), "Updated_Shopify_CSV.csv")
    df.to_csv(updated_path, index=False)
    return updated_path
