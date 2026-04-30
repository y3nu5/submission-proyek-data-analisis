import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.title("📊 Dashboard Analisis E-Commerce")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    order_reviews = pd.read_csv(os.path.join(base_dir, "order_reviews.csv"))
    product_sales = pd.read_csv(os.path.join(base_dir, "product_sales.csv"))
    return order_reviews, product_sales

order_reviews, product_sales = load_data()

# ===============================
# PREPROCESSING
# ===============================
order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
product_sales['order_purchase_timestamp'] = pd.to_datetime(product_sales['order_purchase_timestamp'])

# ===============================
# 🔹 PERTANYAAN 1
# ===============================
st.header("⭐ Distribusi Review Score")

min_date_r = order_reviews['review_creation_date'].min().date()
max_date_r = order_reviews['review_creation_date'].max().date()

date_range_r = st.date_input(
    "📅 Filter Rentang Tanggal Review",
    value=[pd.to_datetime("2018-06-01").date(), pd.to_datetime("2018-08-31").date()],  
    min_value=min_date_r,
    max_value=max_date_r,
    key="filter_review"
)

if len(date_range_r) == 2:
    filtered_reviews = order_reviews[
        (order_reviews['review_creation_date'] >= pd.to_datetime(date_range_r[0])) &
        (order_reviews['review_creation_date'] <= pd.to_datetime(date_range_r[1]))
    ]

    fig1, ax1 = plt.subplots()
    sns.countplot(x='review_score', data=filtered_reviews, ax=ax1)
    ax1.set_title("Distribusi Review Score 3 Bulan Terakhir")
    ax1.set_ylabel("Jumlah Customer")
    ax1.set_xlabel("Review Score")
    st.pyplot(fig1)

# ===============================
# 🔹 PERTANYAAN 2
# ===============================
st.header("🏆 Kategori Produk Terlaris")

min_date_s = product_sales['order_purchase_timestamp'].min().date()
max_date_s = product_sales['order_purchase_timestamp'].max().date()

date_range_s = st.date_input(
    "📅 Filter Rentang Tanggal Penjualan",
    value=[pd.to_datetime("2017-01-01").date(), pd.to_datetime("2018-09-01").date()],  # ← default Q2
    min_value=min_date_s,
    max_value=max_date_s,
    key="filter_sales"
)

if len(date_range_s) == 2:
    filtered_sales = product_sales[
        (product_sales['order_purchase_timestamp'] >= pd.to_datetime(date_range_s[0])) &
        (product_sales['order_purchase_timestamp'] <= pd.to_datetime(date_range_s[1]))
    ]

    top_category = filtered_sales['product_category_name_english'].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_category.values, y=top_category.index, ax=ax2)
    ax2.set_title("Top 10 Kategori Produk Terlaris 2017-2018")
    ax2.set_xlabel("Jumlah Transaksi")
    ax2.set_ylabel("Kategori Produk")
    st.pyplot(fig2)

