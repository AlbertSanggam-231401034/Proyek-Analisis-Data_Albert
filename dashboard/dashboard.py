import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Set Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Mengatur tema seaborn
sns.set_theme(style="ticks", palette="pastel")

# ==============================
# 1. Helper Functions & Data Loading
# ==============================

@st.cache_data
def load_data():
    # Load dataset
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Cleaning: Ubah tipe data dteday ke datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping label musim dan cuaca
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_mapping = {1: 'Clear/Partly Cloudy', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
    
    day_df['season_label'] = day_df['season'].map(season_mapping)
    day_df['weather_label'] = day_df['weathersit'].map(weather_mapping)
    
    hour_df['season_label'] = hour_df['season'].map(season_mapping)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_mapping)
    
    # Menambahkan label tipe hari (Workingday vs Holiday) pada hour_df
    hour_df['day_type'] = hour_df['workingday'].map({1: 'Hari Kerja (Working Day)', 0: 'Akhir Pekan / Libur'})
    
    # Membuat kategori waktu (Binning) untuk jam
    def categorize_time_of_day(hour):
        if 5 <= hour <= 11:
            return 'Pagi (05-11)'
        elif 12 <= hour <= 16:
            return 'Siang (12-16)'
        elif 17 <= hour <= 20:
            return 'Sore (17-20)'
        else:
            return 'Malam (21-04)'
            
    hour_df['time_group'] = hour_df['hr'].apply(categorize_time_of_day)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# ==============================
# 2. Sidebar - Input User (Filter)
# ==============================
st.sidebar.title("🚲 Filter Data")
st.sidebar.markdown("Silakan atur filter di bawah ini:")

# Input: Filter Rentang Tanggal
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

try:
    start_date, end_date = st.sidebar.date_input(
        label="Pilih Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
except ValueError:
    st.error("Harap pilih tanggal awal dan akhir dengan benar.")
    st.stop()

# Input: Filter Musim (Multiselect)
seasons_list = day_df['season_label'].unique().tolist()
selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim",
    options=seasons_list,
    default=seasons_list
)

# Menerapkan filter pada dataset
main_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                     (day_df['dteday'] <= pd.to_datetime(end_date)) &
                     (day_df['season_label'].isin(selected_seasons))]

main_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & 
                       (hour_df['dteday'] <= pd.to_datetime(end_date)) &
                       (hour_df['season_label'].isin(selected_seasons))]

# ==============================
# 3. Main Dashboard Content
# ==============================
st.title("🚴‍♂️ Bike Sharing Data Analytics Dashboard")
st.markdown("Dashboard interaktif ini menyajikan ringkasan dan analisis pola penyewaan sepeda berdasarkan *dataset* historis.")

# --- Metrik Utama ---
st.subheader("📌 Ringkasan Metrik (Berdasarkan Filter)")
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_day_df['cnt'].sum()
    st.metric(label="Total Penyewaan (Semua)", value=f"{total_rentals:,.0f}")

with col2:
    total_registered = main_day_df['registered'].sum()
    st.metric(label="Total Pengguna Registered", value=f"{total_registered:,.0f}")

with col3:
    total_casual = main_day_df['casual'].sum()
    st.metric(label="Total Pengguna Casual", value=f"{total_casual:,.0f}")

st.markdown("---")

# --- Visualisasi 1: Pengaruh Musim dan Cuaca ---
st.subheader("1. Pengaruh Cuaca dan Musim Terhadap Penyewaan")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='season_label', 
    y='cnt', 
    hue='weather_label', 
    data=main_day_df, 
    errorbar=None, 
    palette='muted',
    ax=ax1
)
ax1.set_title("Rata-rata Penyewaan Harian: Musim vs Cuaca", fontsize=14)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan (cnt)")
ax1.legend(title="Kondisi Cuaca", bbox_to_anchor=(1.05, 1), loc='upper left')
sns.despine()
st.pyplot(fig1)

with st.expander("Lihat Penjelasan (Insight)"):
    st.write(
        "Grafik di atas menunjukkan bahwa cuaca cerah/berawan (Clear/Partly Cloudy) secara konsisten "
        "mendominasi angka penyewaan di setiap musim. Cuaca buruk (seperti hujan lebat atau badai) "
        "hampir sepenuhnya menghentikan aktivitas penyewaan."
    )

st.markdown("---")

# --- Visualisasi 2: Pola per Jam ---
st.subheader("2. Pola Penyewaan per Jam: Hari Kerja vs Libur")
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(
    x='hr', 
    y='cnt', 
    hue='day_type', 
    data=main_hour_df, 
    marker='o', 
    errorbar=None,
    linewidth=2,
    ax=ax2
)
ax2.set_title("Rata-rata Penyewaan per Jam", fontsize=14)
ax2.set_xlabel("Jam dalam Sehari (0 - 23)")
ax2.set_ylabel("Rata-rata Penyewaan (cnt)")
ax2.set_xticks(np.arange(0, 24, 1))
ax2.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine()
st.pyplot(fig2)

with st.expander("Lihat Penjelasan (Insight)"):
    st.write(
        "Pada **hari kerja**, terlihat dua puncak tajam (bimodal) pada pukul 08:00 pagi dan 17:00-18:00 sore, "
        "menandakan bahwa sepeda digunakan oleh para pekerja/komuter. "
        "Sebaliknya, pada **akhir pekan/libur**, kurva membentuk pola lonceng yang landai di siang hari, "
        "mengindikasikan penggunaan sepeda untuk rekreasi atau aktivitas santai."
    )

st.markdown("---")

# --- Visualisasi 3: Analisis Lanjutan (Clustering Waktu) ---
st.subheader("3. Perbandingan Tipe Pengguna Berdasarkan Kelompok Waktu")

# Menghitung agregasi berdasarkan time_group
time_clustering = main_hour_df.groupby('time_group')[['casual', 'registered']].mean().reset_index()
time_clustering_melted = time_clustering.melt(id_vars='time_group', var_name='User Type', value_name='Average Rentals')

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='time_group', 
    y='Average Rentals', 
    hue='User Type', 
    data=time_clustering_melted, 
    palette='viridis',
    ax=ax3,
    order=["Pagi (05-11)", "Siang (12-16)", "Sore (17-20)", "Malam (21-04)"]
)
ax3.set_title("Rata-rata Pengguna Casual vs Registered Berdasarkan Waktu", fontsize=14)
ax3.set_xlabel("Kelompok Waktu")
ax3.set_ylabel("Rata-rata Penyewaan")
sns.despine()
st.pyplot(fig3)

with st.expander("Lihat Penjelasan (Insight)"):
    st.write(
        "Hasil *binning* manual waktu menunjukkan dominasi ekstrem dari pengguna **Registered** "
        "pada rentang waktu **Sore** dan **Pagi** (jam pulang dan pergi kerja). Di sisi lain, "
        "jumlah pengguna **Casual** mengalami peningkatan signifikan di waktu **Siang**."
    )

st.caption("Copyright © Albert Sanggam Nalom Sinurat 2024")