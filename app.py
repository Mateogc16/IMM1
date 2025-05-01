import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Estilo medieval oscuro con CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');

        html, body, [class*="css"] {
            background-color: #1e1b1b;
            color: #f8f4e3;
            font-family: 'UnifrakturCook', cursive;
        }

        h1, h2, h3, .css-10trblm, .css-hxt7ib {
            color: #d4af37;
            text-shadow: 2px 2px 4px #000000;
        }

        .stTextArea textarea {
            background-color: #2c2626;
            color: #f8f4e3;
            border: 1px solid #444;
        }

        .stButton>button {
            background-color: #3a2f2f;
            color: #f8f4e3;
            border-radius: 8px;
            border: 2px solid #d4af37;
            font-weight: bold;
        }

        .stSelectbox div {
            background-color: #2c2626;
            color: #f8f4e3;
        }

        .sidebar .sidebar-content {
            background-color: #2a2222;
            color: #f8f4e3;
        }

        .css-1aumxhk {
            background-color: #2a2222 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título e imagen decorativa
st.title("📜 Conversión de Texto a Voz - Grimorio Parlante")
image = Image.open('DRAGÓN BACANO.jpg')  # Puedes reemplazar esto por una imagen más acorde, como un grimorio
st.image(image, width=350)

with st.sidebar:
    st.subheader("✍️ Ingresa un hechizo... o una fábula para ser recitada.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("🛡️ La Balada del Caballero Sombrío")
st.write(
    "En los confines del Bosque de las Cenizas, cabalgaba el caballero Elandor, cuya armadura estaba forjada con la ira de un dios olvidado. "
    "Durante lunas incontables, buscó a la bestia que redujo su reino a cenizas. Y al fin, bajo una luna sangrante, lo halló: "
    "el dragón Malrog, con ojos como brasas y escamas negras como la noche eterna.\n\n"
    "El combate fue un poema de acero y fuego. Las llamas lamieron el escudo del caballero, y su espada cantó contra los colmillos del horror alado. "
    "Con un rugido final, Elandor hundió su hoja maldita en el corazón de la criatura. El dragón cayó... pero también el caballero, "
    "pues ningún hombre toca la sangre de Malrog y vive para contarlo.\n\n"
    "_Así terminó la última luz del reino perdido._"
)


st.markdown("🗣️ ¿Quieres escucharlo? Copia el texto:")
text = st.text_area("📖 Texto a convertir:")

option_lang = st.selectbox("🌍 Lengua del conjuro", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    file_name = text[:20] if len(text) > 0 else "audio"
    tts.save(f"temp/{file_name}.mp3")
    return file_name

if st.button("🔊 Convertir a Voz"):
    result = text_to_speech(text, 'com', lg)
    audio_path = f"temp/{result}.mp3"
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    
    st.markdown("🎧 Tu encantamiento grabado:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(audio_path, "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='Archivo'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">⬇️ Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html(audio_path, file_label="Hechizo Sonoro"), unsafe_allow_html=True)

# Limpieza de archivos viejos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

