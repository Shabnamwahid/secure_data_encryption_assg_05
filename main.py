
import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# ✅ Page config
st.set_page_config(page_title="Secure Encryptor", layout="centered")

# ✅ CSS Styling
st.markdown("""
    <style>
    html, body, .stApp {
        background-image: url("https://wallpaperbat.com/img/319559-cyber-security.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-heading {
        font-size: 48px;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 5px black;
        text-align: center;
        padding-top: 30px;
    }
    .custom-button {
        display: block;
        margin: 30px auto;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: 0.3s ease;
    }
    .custom-button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Fixed key for encryption
KEY = b'n0P_zF-KfHX-DmNoV_E3_YX2gTBDpDnCCkSDdL6iMLU='
cipher = Fernet(KEY)

# ✅ Session state initialization
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# ✅ Hashing function
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# ✅ Encrypt
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# ✅ Decrypt
def decrypt_data(encrypted_text, passkey):
    hashed = hash_passkey(passkey)
    for record in st.session_state.stored_data.values():
        if record["encrypted_text"] == encrypted_text and record["passkey"] == hashed:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    st.session_state.failed_attempts += 1
    return None

# 🎯 Main Heading
st.markdown('<div class="main-heading">🔐 Secure Data Encryption System</div>', unsafe_allow_html=True)
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigate", menu)

# 🏠 Home Page
if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("Store and retrieve **encrypted** data using your secret passkey.")

# 📝 Store Data
elif choice == "Store Data":
    st.subheader("📥 Store Your Data")
    user_data = st.text_area("Enter data to encrypt:")
    passkey = st.text_input("Choose your passkey:", type="password")

    if st.button("Encrypt and Save"):
        if user_data and passkey:
            hashed = hash_passkey(passkey)
            encrypted = encrypt_data(user_data)
            st.session_state.stored_data[encrypted] = {
                "encrypted_text": encrypted,
                "passkey": hashed
            }
            st.success("✅ Data encrypted and saved!")
            st.code(encrypted)
        else:
            st.error("⚠️ Please fill both fields.")

# 🔓 Retrieve Data
elif choice == "Retrieve Data":
    st.subheader("🔎 Retrieve Your Data")
    encrypted_input = st.text_area("Paste Encrypted Text:")
    passkey = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey:
            result = decrypt_data(encrypted_input, passkey)
            if result:
                st.success("✅ Decrypted Data:")
                st.code(result)
            else:
                st.error(f"❌ Incorrect passkey! Attempts left: {3 - st.session_state.failed_attempts}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many wrong attempts. Login required.")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Provide both fields.")

# 🔐 Login Page
elif choice == "Login":
    st.subheader("🔐 Admin Login")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":
            st.session_state.failed_attempts = 0
            st.success("✅ Login successful. Try decryption again.")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect admin password.")
            
st.write(" Build with ❤️ by Shabnam Wahid")