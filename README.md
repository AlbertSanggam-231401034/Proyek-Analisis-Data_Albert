# 🚲 Bike Sharing Data Analysis Dashboard

## 📌 Project Overview
Proyek ini merupakan tugas akhir dari kelas **Belajar Analisis Data dengan Python** di Dicoding. Proyek ini berfokus pada analisis *Bike Sharing Dataset* untuk menggali *insight* bisnis yang bermanfaat. 

Melalui proses *data wrangling*, *exploratory data analysis* (EDA), dan visualisasi data, dashboard ini dirancang untuk menjawab dua pertanyaan bisnis utama:
1. Bagaimana pengaruh kondisi cuaca dan musim terhadap total penyewaan sepeda (*casual* dan *registered*)?
2. Bagaimana pola penyewaan sepeda berdasarkan jam dalam sehari (0-23) jika dibandingkan antara hari kerja (*workingday*) dan hari libur/akhir pekan?

## 📂 Directory Structure
```text
.
├── dashboard
│   └── dashboard.py
│   └── main_data.csv
├── data
│   ├── day.csv
│   └── hour.csv
├── Proyek_Analisis_Data_Albert_Sanggam_Nalom_Sinurat.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## 🚀 Setup & Deployment

### 1. Clone Repository
Langkah pertama adalah mengunduh salinan repositori ini ke komputer Anda. Buka terminal atau command prompt, lalu jalankan perintah berikut:
```bash
git clone https://github.com/AlbertSanggam-231401034/proyek-analisis-data_albert.git
cd proyek-analisis-data_albert
```

### 2. Setup Environment
Menggunakan Shell/Terminal:
```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App (Lokal)
Setelah proses instalasi selesai, Anda dapat menjalankan dan menguji dashboard secara lokal dengan perintah berikut:
```bash
streamlit run dashboard/dashboard.py
```
Dashboard akan otomatis terbuka di browser default Anda.

### 4. Deploy to Streamlit Cloud
Proyek ini sudah dikonfigurasi agar siap di-deploy ke Streamlit Cloud. Ikuti langkah-langkah ini untuk meng-online-kan dashboard Anda:
  - Pastikan seluruh perubahan kode (termasuk requirements.txt, dashboard.py, dan dataset) sudah di-push ke repositori GitHub Anda.
  - Buka situs [Streamlit Share](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
  - Klik tombol "New app".
  - Isi formulir konfigurasi (pilih repository, branch main, dan file path `dashboard/dashboard.py`).
  - Klik "Deploy!" dan tunggu beberapa saat hingga proses instalasi dependensi di server selesai.
  - Selesai! Dashboard Anda kini sudah online dan tautannya bisa langsung dibagikan.
