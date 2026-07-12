import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import json

st.set_page_config(page_title="AI Waste Scanner", page_icon="♻️")

@st.cache_resource
def load_scanner_model():
    model = tf.keras.models.load_model("model_sampah.h5")
    with open("labels.json", "r") as f:
        labels = json.load(f)
    return model, labels

try:
    model, labels = load_scanner_model()
except Exception:
    st.error("File model atau labels belum lengkap di folder.")
    st.stop()

st.title("♻️ AI Scanning & Pemilah Sampah")
st.write("Gunakan kamera laptop atau unggah foto untuk mendeteksi kategori sampah secara instan.")

metode = st.radio("Metode Scan:", ("Gunakan Kamera", "Unggah File Foto"))

foto_user = None
if metode == "Gunakan Kamera":
    foto_user = st.camera_input("Arahkan sampah ke webcam")
else:
    foto_user = st.file_uploader("Pilih gambar dari laptop...", type=["jpg", "jpeg", "png"])

if foto_user is not None:
    image = Image.open(foto_user).convert("RGB")
    st.image(image, caption="Gambar yang masuk ke sistem", use_container_width=True)
    st.write("🔍 Sedang menganalisis...")
    
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.asarray(image)
    img_reshape = img_array[np.newaxis, ...] 
    img_normalized = img_reshape / 255.0     
    
    prediksi = model.predict(img_normalized)
    indeks_tertinggi = np.argmax(prediksi)
    nama_sampah = labels[str(indeks_tertinggi)]
    akurasi = prediksi[indeks_tertinggi] * 100
    
    st.metric(label="Jenis Sampah Terdeteksi:", value=nama_sampah.upper())
    st.info(f"Tingkat Keyakinan AI: *{akurasi:.2f}%*")
    
    nama_sampah_lowercase = nama_sampah.lower()
    if nama_sampah_lowercase in ['plastik', 'logam', 'kertas', 'kardus', 'kaca']:
        st.success("💡 *Saran:* Buang ke tempat sampah *ANORGANIK / DAUR ULANG*.")
    elif nama_sampah_lowercase == 'residu':
        st.error("💡 *Saran:* Buang ke tempat sampah *RESIDU / KHUSUS*.")
    else:
        st.warning("💡 *Saran:* Buang ke tempat sampah *ORGANIK*.")