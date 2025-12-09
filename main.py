import streamlit as st
from io import BytesIO
import qrcode
from PIL import Image
import re
from typing import Tuple

st.set_page_config(page_title="QR Code Generator", layout="wide")

# Hide default streamlit elements
st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5189735719754116"
     crossorigin="anonymous"></script>
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stDecoration"] {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Session state
if "url_input" not in st.session_state:
    st.session_state.url_input = ""
if "qr_generated" not in st.session_state:
    st.session_state.qr_generated = False
if "qr_data" not in st.session_state:
    st.session_state.qr_data = None

def is_valid_url(url: str) -> bool:
    """Simple URL validation."""
    if not url:
        return False
    regex = re.compile(
        r'^(https?://)?'
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'
        r'(/\S*)?$'
    )
    return re.match(regex, url) is not None

def normalize_url(url: str) -> str:
    """Add http:// if missing."""
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

def generate_qr(url: str) -> bytes:
    """Generate QR code as PNG bytes."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    png_bytes = BytesIO()
    img.save(png_bytes, format="PNG")
    png_bytes.seek(0)
    return png_bytes.getvalue()

# Updated Ad render function with your ad code
def render_ad(ad_width: int = 320, ad_height: int = 50):
    """Render the actual ad from highperformanceformat.com"""
    ad_html = f"""
    <div style="display:flex; justify-content:center; align-items:center; padding:10px;">
        <script type="text/javascript">
          atOptions = {{
            'key' : 'b8f4a9d246eaa202e442df7f246bf92f',
            'format' : 'iframe',
            'height' : {ad_height},
            'width' : {ad_width},
            'params' : {{}}
          }};
        </script>
        <script type="text/javascript" src="//www.highperformanceformat.com/b8f4a9d246eaa202e442df7f246bf92f/invoke.js"></script>
    </div>
    """
    st.components.v1.html(ad_html, height=ad_height + 30)

# Title
st.markdown("<h1 style='text-align: center;'>Free QR Code Generator</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>No BS. Free for life time. Enjoy :)</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Main layout: Left Ad | Center (Input + Arrow + QR) | Right Ad
left_ad, center, right_ad = st.columns([1, 3, 1], gap="large")

with left_ad:
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    # Vertical ad for sidebar
    render_ad(ad_width=320, ad_height=250)

with center:
    # Input section
    
    # URL input + Validation badge on same row
    url_col, input_col, validation_col = st.columns([1, 6, 1])
    
    with url_col:
        st.markdown("<p style='text-align: center; padding-top: 8px;'>URL:</p>", unsafe_allow_html=True)

    with input_col:
        url_input = st.text_input("", placeholder="https://example.com", label_visibility="collapsed")
    
    with validation_col:
        if url_input:
            normalized = normalize_url(url_input)
            is_valid = is_valid_url(normalized)
            validation_icon = "✅" if is_valid else "❌"
            validation_color = "green" if is_valid else "red"
            st.markdown(f"<p style='color: {validation_color}; text-align: center; padding-top: 8px; font-size: 20px;'>{validation_icon}</p>", unsafe_allow_html=True)
    
    # Convert button
    st.markdown("<br>", unsafe_allow_html=True)
    convert_btn = st.button("➜ Convert", use_container_width=True, key="convert_btn")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if convert_btn and url_input:
        normalized = normalize_url(url_input)
        if is_valid_url(normalized):
            qr_data = generate_qr(normalized)
            st.session_state.qr_generated = True
            st.session_state.qr_data = qr_data
            st.session_state.url_for_qr = normalized
        else:
            st.error("Please enter a valid URL")

    # QR Code centered
    qr_col1, qr_col2, qr_col3 = st.columns([1, 1, 1])
    
    with qr_col2:
        if st.session_state.qr_generated and st.session_state.qr_data:
            st.image(st.session_state.qr_data, width=250)
        else:
            st.markdown("""
            <div style='width:250px; height:250px; background:#f0f0f0; border:2px dashed #ccc; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#999; font-size:14px;'>
                QR Code Preview
            </div>
            """, unsafe_allow_html=True)
        
        # Download buttons (small, below QR)
        if st.session_state.qr_generated and st.session_state.qr_data:
            st.markdown("<br>", unsafe_allow_html=True)
            
            d_col1, d_col2, d_col3 = st.columns(3, gap="small")
            
            with d_col1:
                st.download_button(
                    label="PNG",
                    data=st.session_state.qr_data,
                    file_name="qr_code.png",
                    mime="image/png",
                    use_container_width=True,
                    key="png_btn"
                )
            
            with d_col2:
                # SVG download
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
                qr.add_data(st.session_state.url_for_qr)
                qr.make(fit=True)
                matrix = qr.get_matrix()
                block = 10
                w = len(matrix)
                svg_size = w * block
                svg_parts = []
                svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_size}" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}">')
                svg_parts.append(f'<rect width="100%" height="100%" fill="white"/>')
                for y in range(w):
                    for x in range(w):
                        if matrix[y][x]:
                            svg_parts.append(f'<rect x="{x*block}" y="{y*block}" width="{block}" height="{block}" fill="black"/>')
                svg_parts.append('</svg>')
                svg_str = "".join(svg_parts)
                
                st.download_button(
                    label="SVG",
                    data=svg_str.encode("utf-8"),
                    file_name="qr_code.svg",
                    mime="image/svg+xml",
                    use_container_width=True,
                    key="svg_btn"
                )
            
            with d_col3:
                if st.button("Reset", use_container_width=True, key="reset_btn"):
                    st.session_state.qr_generated = False
                    st.session_state.qr_data = None
                    st.session_state.url_input = ""
                    st.rerun()

with right_ad:
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    # Vertical ad for sidebar
    render_ad(ad_width=320, ad_height=250)

# Bottom Ad (horizontal banner)
st.markdown("---")
_, bottom_ad, _ = st.columns([1, 2, 1])
with bottom_ad:
    # Horizontal banner ad at bottom
    render_ad(ad_width=728, ad_height=90)
