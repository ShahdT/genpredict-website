import streamlit as st
from PIL import Image
import base64

# ------------------ Page Configuration ------------------
st.set_page_config(page_title="GenPredict", layout="wide")

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
        font-size: 50px;
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

# ------------------ Banner ------------------
banner = Image.open(banner_path)

# ------------------ Text under banner ------------------
st.markdown(
    """
    <style>
    .bottom-text {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color:#555
        margin-top: 30px;
    }
    .team-container {
        text-align: center;
        margin-top: 40px;
    }
    .member {
        font-size: 18px;
        margin: 10px 0;
        color: #064635
    }
    .member a {
        text-decoration: none;
        color:#064635;
        font-weight: bold;
        margin-left: 8px;
    }
    .member a:hover {
        color:#555
    }
    </style>

    <div class="bottom-text"> Our Team 💚</div>

    <div class="team-container">
        <div class="member"> <b>Shahad Alhamam</b>
            <a href="https://www.linkedin.com/in/shahad-alhamam" target="_blank">LinkedIn</a>
        </div>
        <div class="member"> <b>Bashyer Alsulami</b>
            <a href="https://www.linkedin.com/in/bashyer-alsulami" target="_blank">LinkedIn</a>
        </div>
        <div class="member"> <b>Shahd Altalhi</b>
            <a href="https://www.linkedin.com/in/altalhishahd" target="_blank">LinkedIn</a>
        </div>
        <div class="member"> <b>Shahad Alfahmi</b>
            <a href="http://linkedin.com/in/shahad-alfahmi-390729312" target="_blank">LinkedIn</a>
        </div>
    </div>

    <div style="text-align:center; margin-top:30px; font-size:16px; color:#064635;">
        Thank you 🧬
    </div>
    """,
    unsafe_allow_html=True
)
