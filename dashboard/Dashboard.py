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
    # Gunakan path relatif terhadap lokasi script ini
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    order_reviews_path = os.path.join(base_dir, "order_reviews.csv")
    product_sales_path = os.path.join(base_dir, "product_sales.csv")
    
    order_reviews = pd.read_csv(order_reviews_path)
    product_sales = pd.read_csv(product_sales_path)
    
    return order_reviews, product_sales

try:
    order_reviews, product_sales = load_data()
except FileNotFoundError as e:
    st.error(f"❌ File tidak ditemukan: {e}")
    st.stop()

# ===============================
# VISUALISASI 1
# ===============================
st.header("⭐ Distribusi Review Score")

fig1, ax1 = plt.subplots()
sns.countplot(x='review_score', data=order_reviews, ax=ax1)
ax1.set_title("Distribusi Review Score")
ax1.set_xlabel("Review Score")
ax1.set_ylabel("Jumlah")
st.pyplot(fig1)
plt.close(fig1)  # Bebaskan memori

st.markdown("""
Mayoritas pelanggan memberikan rating tinggi (4–5), menunjukkan kepuasan yang baik.
""")

# ===============================
# VISUALISASI 2
# ===============================
st.header("🏆 Top 10 Kategori Produk Terlaris")

if 'product_category_name_english' not in product_sales.columns:
    st.warning("⚠️ Kolom 'product_category_name_english' tidak ditemukan. Kolom yang tersedia: " + 
               str(product_sales.columns.tolist()))
else:
    top_category = product_sales['product_category_name_english'].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_category.values, y=top_category.index, ax=ax2)
    ax2.set_title("Top 10 Kategori Produk Terlaris")
    ax2.set_xlabel("Jumlah Penjualan")
    ax2.set_ylabel("Kategori")
    st.pyplot(fig2)
    plt.close(fig2)  # Bebaskan memori

st.markdown("""
Kategori tertentu mendominasi penjualan dan berpotensi menjadi fokus bisnis utama.
""")

# ===============================
# KESIMPULAN
# ===============================
st.header("📌 Kesimpulan")
st.write("""
1. Berdasarkan analisis distribusi review_score, mayoritas pelanggan memberikan rating tinggi (4 dan 5). Hal ini menunjukkan bahwa secara umum tingkat kepuasan pelanggan terhadap layanan dan produk tergolong baik.
   Namun, masih terdapat sebagian pelanggan yang memberikan rating rendah, yang mengindikasikan adanya pengalaman negatif pada sebagian transaksi.
2. Kategori penjualan produk tertinggi berada di kategori produk bed_bath_table, diikuti oleh kategori produk health_beauty dan sports_leisure. Hal ini menunjukkan bahwa kategori-kategori tersebut memiliki permintaan yang tinggi di pasar dan berpotensi menjadi fokus bisnis utama untuk meningkatkan penjualan.
""")

# ===============================
# REKOMENDASI
# ===============================
st.header("🚀 Rekomendasi")
st.write("""
- Fokus pada kategori produk terlaris
- Optimalkan promosi (diskon, program loyalitas custoer, dll,)
- Walaupun rating sudah tinggi, pertahankan kualitas produk dan layanan
- Untuk rating 1 & 2 dianalisis lebih lanjut apa permasalahan utamanya.
""")