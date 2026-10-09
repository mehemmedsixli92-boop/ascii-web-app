import streamlit as st
from PIL import Image
import cv2
import tempfile
import numpy as np

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def frame_to_ascii(frame, new_width=100):
    # OpenCV BGR formatını PIL RGB formatına çeviririk
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    image = image.resize((new_width, new_height)).convert("L")
    
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    pixel_count = len(characters)
    ascii_img = "\n".join([characters[i:(i + new_width)] for i in range(0, pixel_count, new_width)])
    return ascii_img

st.title("ASCII Art - Şəkil və Video Çevirici")

option = st.radio("Fayl növünü seçin:", ("Şəkil", "Video"))

if option == "Şəkil":
    uploaded_file = st.file_uploader("Şəkil yükləyin...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Yüklənən Şəkil", use_column_width=True)
        new_width = st.slider("Genişlik (Simvol sayı):", 20, 150, 80)
        
        # ASCII Çevirmə
        w, h = image.size
        resized = image.resize((new_width, int(new_width * (h / w) * 0.55))).convert("L")
        pixels = resized.getdata()
        ascii_str = "".join([ASCII_CHARS[p // 25] for p in pixels])
        ascii_img = "\n".join([ascii_str[i:(i + new_width)] for i in range(0, len(ascii_str), new_width)])
        
        st.text_area("ASCII Nəticəsi:", ascii_img, height=400)

elif option == "Video":
    uploaded_video = st.file_uploader("Video yükləyin...", type=["mp4", "mov", "avi"])
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        
        cap = cv2.VideoCapture(tfile.name)
        new_width = st.slider("Genişlik (Simvol sayı):", 20, 100, 60)
        
        st.write("Video emal olunur...")
        frame_window = st.empty()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            ascii_frame = frame_to_ascii(frame, new_width)
            frame_window.code(ascii_frame, language=None)
            
        cap.release()

