import streamlit as st
from PIL import Image
import cv2
import tempfile

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def image_to_color_ascii(image, new_width=80):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5) # Yükseklik oranını düzenle
    
    # Resmi yeniden boyutlandır
    img_resized = image.resize((new_width, new_height))
    img_rgb = img_resized.convert("RGB")
    
    # HTML stil yapısı oluştur
    html_output = '<div style="font-family: monospace; font-size: 8px; line-height: 7px; background-color: black; letter-spacing: 1px; white-space: pre; word-wrap: break-word;">'
    
    for y in range(new_height):
        for x in range(new_width):
            r, g, b = img_rgb.getpixel((x, y))
            # Parlaklığa göre karakter seçimi
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            char_index = brightness // 25
            if char_index >= len(ASCII_CHARS):
                char_index = len(ASCII_CHARS) - 1
            char = ASCII_CHARS[char_index]
            
            # Boşluk karakterlerini düzgün göstermek için
            if char == " ":
                char = "&nbsp;"
                
            html_output += f'<span style="color: rgb({r},{g},{b});">{char}</span>'
        html_output += "<br>"
        
    html_output += "</div>"
    return html_output

st.set_page_config(layout="wide")
st.title("Renkli ASCII Art Çevirici 🎨")

option = st.radio("Dosya türünü seçin:", ("Fotoğraf", "Video"))

if option == "Fotoğraf":
    uploaded_file = st.file_uploader("Fotoğraf yükleyin...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Orijinal Fotoğraf", use_column_width=True)
            
        new_width = st.slider("Genişlik (Karakter Sayısı):", 30, 150, 80)
        
        with col2:
            st.write("ASCII Sonucu:")
            ascii_html = image_to_color_ascii(image, new_width)
            st.markdown(ascii_html, unsafe_allow_html=True)

elif option == "Video":
    uploaded_video = st.file_uploader("Video yükleyin...", type=["mp4", "mov", "avi"])
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        
        cap = cv2.VideoCapture(tfile.name)
        new_width = st.slider("Genişlik (Karakter Sayısı):", 20, 80, 50)
        
        frame_window = st.empty()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # OpenCV BGR -> PIL RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            ascii_html = image_to_color_ascii(pil_image, new_width)
            frame_window.markdown(ascii_html, unsafe_allow_html=True)
            
        cap.release()
