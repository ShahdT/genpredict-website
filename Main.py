import streamlit as st
from PIL import Image
import base64

# ------------------ Page Configuration ------------------
st.set_page_config(page_title="GenPredict1111", layout="wide")

# ------------------ Paths ------------------
logo_path = "Logo.png"
banner_path = "Banner.jpg"

# ------------------ Colors ------------------
main_bg_color = "#ECF3F0"

# ------------------ Convert image to Base64 ------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file(logo_path)
banner_base64 = get_base64_of_bin_file(banner_path)

# ------------------ CSS ------------------
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {main_bg_color};
    }}

    /* logo*/
    .logo-box {{
        position: fixed;
        top: 20px;
        left: 20px;
        width: 160px;
        height: 160px;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }}
    .logo-box img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }}

    /* Project Name*/
    .center-text {{
        text-align: center;
        font-size: 70px;
        font-weight: bold;
        margin-top: 50px;
        color: #064635;
    }}

    /* Text */
    .bottom-text {{
        text-align: center;
        font-size: 24px;
        margin-top: 20px;
        color: #064635;
    }}

    /* Banner */
  .banner-box {{
    width: 100%;
    height: 100px;
    margin: 20px auto 0 auto;
    border-radius: 10px;
    overflow: hidden;
    }}

.banner-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    }}
    </style>

<!-- Topic -->
<div class="center-text">GenPredict</div>

<!-- Logo -->
<div class="logo-box">
    <img src="data:image/png;base64,{logo_base64}">
</div>

<!-- Banner -->
<div class="banner-box">
    <img src="data:image/jpeg;base64,{banner_base64}">
</div>
""", unsafe_allow_html=True)

# ------------------ Title ------------------
# st.markdown('<div class="center-text">GenPredict</div>', unsafe_allow_html=True)

# ------------------ Banner ------------------
banner = Image.open(banner_path)
# st.image(banner, use_column_width=True, output_format="PNG", clamp=True, caption="")
# st.image(banner, use_column_width=True, output_format="PNG", clamp=True)
# st.markdown(f'<img src="{banner_path}" class="banner-img">', unsafe_allow_html=True)
# st.markdown(f'<img src="data:image/jpeg;base64,{banner_base64}" class="banner-img">', unsafe_allow_html=True)


# ------------------ Text under banner ------------------
st.markdown('<div class="bottom-text">TEXT</div>', unsafe_allow_html=True)
