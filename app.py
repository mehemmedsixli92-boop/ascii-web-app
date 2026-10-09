import streamlit as st
from PIL import Image

# ASCII simvolları (parlaqlığa görə sıralanıb)
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

# Streamlit Veb Arayüzü
st.title("ASCII Art Çevirici")

uploaded_file = st.file_uploader("Şəkil yükləyin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklənən Şəkil", use_column_width=True)
    
    # Emal etmək
    new_width = st.slider("Genişlik (Simvol sayı):", 20, 200, 100)
    
    resized_img = resize_image(image, new_width)
    gray_img = grayify(resized_img)
    ascii_str = pixels_to_ascii(gray_img)
    
    # Sətirlərə bölmək
    pixel_count = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:(index + new_width)] for index in range(0, pixel_count, new_width)])
    
    # Nəticəni göstərmək
    st.text_area("ASCII Nəticəsi:", ascii_img, height=400)
