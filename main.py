"""
Amazon Sales Analysis Dashboard
Converted from Jupyter notebook analysis into an interactive Streamlit app.

Run with:
    streamlit run amazon_sales_dashboard.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Amazon Sales Analysis Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CUSTOM STYLING
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main { background-color: #f7f8fa; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetricLabel"] { font-weight: 600; color: #555; }
    h1, h2, h3 { color: #232f3e; }
    .block-container { padding-top: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# DATA PATH — update this to point to your local amazon.csv
# ----------------------------------------------------------------------------
CSV_PATH = "Data/amazon.csv"  # e.g. "D:/Anaconda/Project/Amazone-Sales-Analysis-Dashbaord/Data/amazon.csv"

# ----------------------------------------------------------------------------
# DATA LOADING + CLEANING (same logic as the original notebook)
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file)

    df["discounted_price"] = (
        df["discounted_price"].astype(str).str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )
    df["actual_price"] = (
        df["actual_price"].astype(str).str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["rating_count"] = (
        df["rating_count"].astype(str).str.replace(",", "", regex=False)
    )
    df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    df["discount_percentage"] = (
        df["discount_percentage"].astype(str).str.replace("%", "", regex=False)
    )
    df["discount_percentage"] = pd.to_numeric(df["discount_percentage"], errors="coerce")

    df = df.dropna(subset=["rating", "rating_count", "discount_percentage",
                            "discounted_price", "actual_price"])

    # Performance score, same formula as notebook
    df["performance_score"] = df["rating"] * np.log1p(df["rating_count"])

    # Top-level category (category column is often a ">" separated path)
    if "category" in df.columns:
        df["category_top"] = df["category"].astype(str).str.split("\\|").str[0].str.split(">").str[0]

    return df


st.sidebar.title("📦 Amazon Sales Dashboard")
st.sidebar.markdown(f"Loading data from:\n`{CSV_PATH}`")

try:
    df = load_data(CSV_PATH)
except FileNotFoundError:
    st.title("📦 Amazon Sales Analysis Dashboard")
    st.error(
        f"❌ Could not find the data file at **`{CSV_PATH}`**.\n\n"
        "Update the `CSV_PATH` variable near the top of this script to point "
        "to your actual `amazon.csv` location."
    )
    st.stop()

# ----------------------------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

cat_col = "category_top" if "category_top" in df.columns else "category"
all_categories = sorted(df[cat_col].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Category", options=all_categories, default=[]
)

rating_range = st.sidebar.slider(
    "Rating range", float(df["rating"].min()), float(df["rating"].max()),
    (float(df["rating"].min()), float(df["rating"].max())), step=0.1,
)

price_min, price_max = float(df["actual_price"].min()), float(df["actual_price"].max())
price_range = st.sidebar.slider(
    "Actual price range (₹)", price_min, price_max, (price_min, price_max)
)

filtered_df = df[
    (df["rating"].between(*rating_range))
    & (df["actual_price"].between(*price_range))
]
if selected_categories:
    filtered_df = filtered_df[filtered_df[cat_col].isin(selected_categories)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered_df):,}** of {len(df):,} products")

# ----------------------------------------------------------------------------
# HEADER + KPIs
# ----------------------------------------------------------------------------
st.title("📦 Amazon Sales Analysis Dashboard")
st.caption("Interactive view of product pricing, ratings, and category performance")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Products", f"{filtered_df['product_id'].nunique():,}")
k2.metric("Avg. Discount", f"{filtered_df['discount_percentage'].mean():.1f}%")
k3.metric("Avg. Rating", f"{filtered_df['rating'].mean():.2f} ⭐")
k4.metric("Total Reviews", f"{int(filtered_df['rating_count'].sum()):,}")
corr = filtered_df["rating"].corr(filtered_df["discount_percentage"])
k5.metric("Rating ↔ Discount Corr.", f"{corr:.2f}")

st.markdown("---")

# ----------------------------------------------------------------------------
# ROW 1: Top reviewed products | Category-wise avg rating
# ----------------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("🔥 Top 10 Most Reviewed Products")
    top_reviewed = (
        filtered_df[["product_name", "rating_count"]]
        .sort_values("rating_count", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top_reviewed, x="rating_count", y="product_name", orientation="h",
        labels={"rating_count": "Review Count", "product_name": ""},
        color="rating_count", color_continuous_scale="Oranges",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, height=420)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("⭐ Category-wise Average Rating (Top 10)")
    category_rating = (
        filtered_df.groupby(cat_col)["rating"].mean()
        .sort_values(ascending=False).head(10).reset_index()
    )
    fig = px.bar(
        category_rating, x="rating", y=cat_col, orientation="h",
        labels={"rating": "Avg Rating", cat_col: ""},
        color="rating", color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, height=420)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 2: Category-wise avg discount | Category distribution
# ----------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("💸 Category-wise Average Discount (Top 10)")
    category_discount = (
        filtered_df.groupby(cat_col)["discount_percentage"].mean()
        .sort_values(ascending=False).head(10).reset_index()
    )
    fig = px.bar(
        category_discount, x="discount_percentage", y=cat_col, orientation="h",
        labels={"discount_percentage": "Avg Discount %", cat_col: ""},
        color="discount_percentage", color_continuous_scale="Greens",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, height=420)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("📊 Product Count by Category (Top 10)")
    category_count = filtered_df[cat_col].value_counts().head(10).reset_index()
    category_count.columns = [cat_col, "count"]
    fig = px.pie(
        category_count, names=cat_col, values="count", hole=0.45,
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 3: Rating distribution | Rating vs Discount scatter
# ----------------------------------------------------------------------------
c5, c6 = st.columns(2)

with c5:
    st.subheader("📈 Rating Distribution")
    fig = px.histogram(filtered_df, x="rating", nbins=10, color_discrete_sequence=["#ff9900"])
    fig.update_layout(xaxis_title="Rating", yaxis_title="Count", height=400)
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.subheader("🔍 Rating vs Discount Percentage")
    fig = px.scatter(
        filtered_df, x="discount_percentage", y="rating",
        opacity=0.6, color="rating", color_continuous_scale="Viridis",
        labels={"discount_percentage": "Discount %", "rating": "Rating"},
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Correlation coefficient: **{corr:.2f}**")

st.markdown("---")

# ----------------------------------------------------------------------------
# ROW 4: Performance score leaders
# ----------------------------------------------------------------------------
st.subheader("🏆 Top 10 Products by Performance Score")
st.caption("Performance Score = Rating × log(1 + Review Count)")
top_perf = (
    filtered_df[["product_name", "performance_score", "rating", "rating_count"]]
    .sort_values("performance_score", ascending=False).head(10)
)
fig = px.bar(
    top_perf, x="performance_score", y="product_name", orientation="h",
    labels={"performance_score": "Performance Score", "product_name": ""},
    color="performance_score", color_continuous_scale="Purples",
)
fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, height=420)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 5: Most expensive / cheapest tables
# ----------------------------------------------------------------------------
t1, t2 = st.columns(2)

with t1:
    st.subheader("💎 Most Expensive Products")
    expensive = (
        filtered_df[["product_name", "actual_price"]]
        .sort_values("actual_price", ascending=False).head(10)
        .reset_index(drop=True)
    )
    st.dataframe(expensive, use_container_width=True, hide_index=True)

with t2:
    st.subheader("🪙 Cheapest Products (After Discount)")
    cheap = (
        filtered_df[["product_name", "discounted_price"]]
        .sort_values("discounted_price", ascending=True).head(10)
        .reset_index(drop=True)
    )
    st.dataframe(cheap, use_container_width=True, hide_index=True)

# ----------------------------------------------------------------------------
# RAW DATA EXPANDER
# ----------------------------------------------------------------------------
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit • Data: Amazon Sales Dataset")
