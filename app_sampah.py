import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import json
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA MODERN
# ==========================================
st.set_page_config(
    page_title="EcoScans - Cerdas Pilah Sampah",
    page_icon="🗑️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk tampilan Dashboard yang bersih dan modern
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stFileUploader {
        border: 2px dashed #2E7D32 !important;
        border-radius: 15px;
        background-color: #ffffff;
        padding: 20px;
    }
    .prediction-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.1);
        border-left: 5px solid #2E7D32;
        margin-top: 20px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SISTEM DATABASE SEMENTARA (SESSION STATE)
# ==========================================
# Inisialisasi data counter jika pertama kali website dibuka
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = {
        "Organik": 12,    # Data simulasi awal agar grafik langsung muncul
        "Anorganik": 18,
        "B3 / Berbahaya": 5
    }

# ==========================================
# 3. HEADER WEBSITE (LOGO ECOSCANS)
# ==========================================
try:
    logo = Image.open('logo.png')
    st.image(logo, use_container_width=True)
except FileNotFoundError:
    st.title("🌱 ECOSCANS")
    st.subheader("Cerdas Pilah Sampah, Jaga Bumi")

st.markdown("---")

# ==========================================
# 4. LOAD MODEL & LABELS AI
# ==========================================
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model_sampah.h5')

model = load_my_model()

with open('labels.json', 'r') as f:
    labels = json.load(f)

# ==========================================
# 5. KONTEN UTAMA: FITUR SCANNING AI
# ==========================================
st.write("### 📸 Ambil atau Unggah Foto Sampah")
st.caption("Sistem AI akan menganalisis foto dan memasukkannya ke dalam statistik kontribusi bumi.")

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.write("#### 🖼️ Pratinjau Gambar")
        st.image(image, use_container_width=True, channels="RGB")
        
    with col2:
        st.write("#### 🤖 Analisis AI EcoScans")
        with st.spinner("Sedang memproses gambar..."):
            size = (224, 224) 
            image_resized = ImageOps.fit(image, size)
            img_array = np.asarray(image_resized)
            img_normalized = img_array.astype(np.float32) / 255.0
            data = np.expand_dims(img_normalized, axis=0)

            # Eksekusi Prediksi
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = labels[str(index)]
            confidence_score = prediction[index]

            # UPDATE STATISTIK: Menambah hitungan tipe sampah yang terdeteksi
            if class_name in st.session_state.scan_history:
                st.session_state.scan_history[class_name] += 1

        # Tampilan Hasil Prediksi Elegan
        st.markdown(f"""
            <div class="prediction-card">
                <span style="color: #666; font-size: 14px; font-weight: bold; text-transform: uppercase;">Kategori Terdeteksi</span>
                <h2 style="color: #2E7D32; margin: 5px 0 15px 0; font-size: 32px;">🟢 {class_name}</h2>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 10px 0;">
                <span style="color: #666; font-size: 14px;">Tingkat Akurasi AI</span>
                <h4 style="color: #333; margin: 5px 0 0 0;">{confidence_score * 100:.2f}%</h4>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 6. PANEL DASHBOARD & GRAFIK STATISTIK (KEKINIAN)
# ==========================================
st.write("### 📊 Dashboard Dampak Lingkungan Kita")
st.caption("Akumulasi jumlah sampah yang berhasil dipilah dan didata oleh pengguna EcoScans hari ini.")

import streamlit as st  # <-- SEBELUMNYA SALAH KETIK 'as tf', SEKARANG SUDAH BENAR 'as st'
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import json
import pandas as pd

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA MODERN
# ==========================================
st.set_page_config(
    page_title="EcoScans - Cerdas Pilah Sampah",
    page_icon="🗑️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk tampilan Dashboard yang bersih dan modern
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stFileUploader {
        border: 2px dashed #2E7D32 !important;
        border-radius: 15px;
        background-color: #ffffff;
        padding: 20px;
    }
    .prediction-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.1);
        border-left: 5px solid #2E7D32;
        margin-top: 20px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SISTEM DATABASE SEMENTARA (SESSION STATE)
# ==========================================
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = {
        "Organik": 12,    
        "Anorganik": 18,
        "B3 / Berbahaya": 5
    }

# ==========================================
# 3. HEADER WEBSITE (LOGO ECOSCANS)
# ==========================================
try:
    logo = Image.open('logo.png')
    st.image(logo, use_container_width=True)
except FileNotFoundError:
    st.title("🌱 ECOSCANS")
    st.subheader("Cerdas Pilah Sampah, Jaga Bumi")

st.markdown("---")

# ==========================================
# 4. LOAD MODEL & LABELS AI
# ==========================================
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model_sampah.h5')

model = load_my_model()

with open('labels.json', 'r') as f:
    labels = json.load(f)

# ==========================================
# 5. KONTEN UTAMA: FITUR SCANNING AI
# ==========================================
st.write("### 📸 Ambil atau Unggah Foto Sampah")
st.caption("Sistem AI akan menganalisis foto dan memasukkannya ke dalam statistik kontribusi bumi.")

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.write("#### 🖼️ Pratinjau Gambar")
        st.image(image, use_container_width=True, channels="RGB")
        
    with col2:
        st.write("#### 🤖 Analisis AI EcoScans")
        with st.spinner("Sedang memproses gambar..."):
            size = (224, 224) 
            image_resized = ImageOps.fit(image, size)
            img_array = np.asarray(image_resized)
            img_normalized = img_array.astype(np.float32) / 255.0
            data = np.expand_dims(img_normalized, axis=0)

            # Eksekusi Prediksi
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = labels[str(index)]
            confidence_score = prediction[index]

            # Update Statistik
            if class_name in st.session_state.scan_history:
                st.session_state.scan_history[class_name] += 1

        # Tampilan Hasil Prediksi Elegan
        st.markdown(f"""
            <div class="prediction-card">
                <span style="color: #666; font-size: 14px; font-weight: bold; text-transform: uppercase;">Kategori Terdeteksi</span>
                <h2 style="color: #2E7D32; margin: 5px 0 15px 0; font-size: 32px;">🟢 {class_name}</h2>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 10px 0;">
                <span style="color: #666; font-size: 14px;">Tingkat Akurasi AI</span>
                <h4 style="color: #333; margin: 5px 0 0 0;">{confidence_score * 100:.2f}%</h4>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 6. PANEL DASHBOARD & GRAFIK STATISTIK
# ==========================================
st.write("### 📊 Dashboard Dampak Lingkungan Kita")
st.caption("Akumulasi jumlah sampah yang berhasil dipilah dan didata oleh pengguna EcoScans hari ini.")

# Mengonversi database sementara ke Pandas DataFrame untuk grafik
df_stats = pd.DataFrame(
    list(st.session_state.scan_history.items()), 
    columns=["Kategori Sampah", "Jumlah (Unit)"]
)

# Tampilan Metrics Angka Ringkasan
total_sampah = df_stats["Jumlah (Unit)"].sum()
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(label="Total Sampah Dipilah", value=f"{total_sampah} Unit", delta="Hari Ini")
with metric_col2:
    st.metric(label="♻️ Organik & Anorganik", value=st.session_state.scan_history["Organik"] + st.session_state.scan_history["Anorganik"])
with metric_col3:
    st.metric(label="⚠️ Aman Terkendali (B3)", value=st.session_state.scan_history["B3 / Berbahaya"])

st.write("") 

# Tampilan Grafik Batang Horisontal yang Clean & Modern
st.write("#### 📈 Proporsi Jenis Sampah")
st.bar_chart(data=df_stats, x="Kategori Sampah", y="Jumlah (Unit)", use_container_width=True)
