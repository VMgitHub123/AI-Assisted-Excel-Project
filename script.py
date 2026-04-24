import pandas as pd

# Load data
df = pd.read_csv("amazon.csv")

# Preview columns
print("Original columns:")
print(df.columns)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")

print("\nCleaned columns:")
print(df.columns)

# Keep only columns useful for analysis
keep_cols = [
    "product_id",
    "product_name",
    "category",
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count"
]

df = df[keep_cols]

# Remove duplicates
df = df.drop_duplicates()

# Clean price columns (remove currency symbols/commas if needed)
for col in ["discounted_price", "actual_price"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Clean discount percentage
df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)
df["discount_percentage"] = pd.to_numeric(df["discount_percentage"], errors="coerce")

# Clean rating
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Clean rating_count
df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

# Drop rows missing important values
df = df.dropna(subset=["category", "discounted_price", "actual_price", "discount_percentage", "rating"])

# Create calculated columns
df["price_difference"] = df["actual_price"] - df["discounted_price"]

# Optional: simplify category to first main category if categories are long
df["main_category"] = df["category"].astype(str).str.split("|").str[0].str.strip()

# Save cleaned file
df.to_csv("cleaned_data.csv", index=False)

print("\nCleaned data saved as cleaned_data.csv")
print(df.head())
print("\nShape:", df.shape)