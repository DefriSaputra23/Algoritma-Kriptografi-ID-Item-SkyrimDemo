import streamlit as st
import string

# ======================================================
# DATASET
# ======================================================
ALPHABET = string.ascii_uppercase
CATEGORY_COUNT = 5

ITEM_ID_MAP = {
    'A': '00012EB7',
    'B': '00013989',
    'C': '0001398A',
    'D': '0001398B',
    'E': '0001398C',
    'F': '0001398D',
    'G': '00012E49',
    'H': '00013952',
    'I': '00013953',
    'J': '00013954',
    'K': '00013955',
    'L': '00013956',
    'M': '0003EADD',
    'N': '0003EAE2',
    'O': '0003EAE3',
    'P': '0003EADE',
    'Q': '0003EADF',
    'R': '0003EAEO',
    'S': '000A44',
    'T': '000A45',
    'U': '000A46',
    'V': '000A47',
    'W': '000A48',
    'X': '000A49',
    'Y': '000A26',
    'Z': '000A27'
}

# ======================================================
# UTILITAS
# ======================================================
def key_to_number(key):
    return sum(ALPHABET.index(k) + 1 for k in key if k in ALPHABET)

def caesar_shift(text, shift):
    result = ""
    for c in text:
        if c in ALPHABET:
            result += ALPHABET[(ALPHABET.index(c) + shift) % 26]
        else:
            result += c
    return result

def caesar_unshift(text, shift):
    result = ""
    for c in text:
        if c in ALPHABET:
            result += ALPHABET[(ALPHABET.index(c) - shift) % 26]
        else:
            result += c
    return result

def extract_block(item_id):
    return item_id[-2:] + item_id[-4:-2]

# ======================================================
# INVERSE MAPPING
# ======================================================
BLOCK_TO_CHAR = {
    extract_block(item_id): char
    for char, item_id in ITEM_ID_MAP.items()
}

# ======================================================
# LOGGING
# ======================================================
def add_log(msg):
    if "encrypt_log" not in st.session_state:
        st.session_state.encrypt_log = []
    st.session_state.encrypt_log.append(msg)

# ======================================================
# STREAMLIT UI
# ======================================================
st.title("🔐 Skyrim Cryptography Demo")
st.caption("Enkripsi & Dekripsi berbasis Item ID Skyrim")

st.markdown("### 📂 Dokumentasi & Dataset")
st.markdown(
    "[🔗 Lihat Dataset & Dokumentasi](https://drive.google.com/drive/folders/1CqIbSM2IWldEGEs19m1jf85rn9GWHttZ?usp=sharing)",
    unsafe_allow_html=True
)

mode = st.radio("Mode Operasi", ["Enkripsi", "Dekripsi"])
key = st.text_input("Masukkan Key").upper()

# ======================================================
# ENKRIPSI
# ======================================================
if mode == "Enkripsi":
    plaintext = st.text_area("Masukkan Plaintext").upper()

    if st.button("Encrypt"):
        if not plaintext or not key:
            st.warning("Plaintext dan Key wajib diisi!")
            st.stop()

        st.session_state.encrypt_log = []

        add_log(f"Plaintext awal: {plaintext}")
        add_log(f"Key digunakan: {key}")

        total_key = key_to_number(key)
        huruf_count = sum(1 for c in plaintext if c in ALPHABET)
        shift = (total_key + huruf_count + len(key)) % CATEGORY_COUNT

        add_log(f"Total nilai key: {total_key}")
        add_log(f"Jumlah huruf alfabet: {huruf_count}")
        add_log(f"Panjang key: {len(key)}")
        add_log(f"Shift akhir: {shift}")

        shifted = caesar_shift(plaintext, shift)
        add_log(f"Hasil Caesar Shift: {shifted}")

        blocks = []
        add_log("Mapping karakter ke Item ID:")

        for c in shifted:
            if c in ALPHABET:
                block = extract_block(ITEM_ID_MAP[c])
                blocks.append(block)
                add_log(f"{c} → {block}")
            else:
                blocks.append(c)
                add_log("Spasi dipertahankan")

        ciphertext = " ".join(blocks)
        add_log(f"Ciphertext akhir: {ciphertext}")

        st.subheader("🔐 Ciphertext Akhir")
        st.code(ciphertext)

        with st.expander("📜 Encryption Log (Detail Proses)"):
            for log in st.session_state.encrypt_log:
                st.write(log)

# ======================================================
# DEKRIPSI
# ======================================================
else:
    ciphertext = st.text_area("Masukkan Ciphertext")

    if st.button("Decrypt"):
        if not ciphertext or not key:
            st.warning("Ciphertext dan Key wajib diisi!")
            st.stop()

        tokens = ciphertext.split(" ")

        total_key = key_to_number(key)
        huruf_count = sum(1 for t in tokens if t in BLOCK_TO_CHAR)
        shift = (total_key + huruf_count + len(key)) % CATEGORY_COUNT

        shifted_text = ""
        for t in tokens:
            if t in BLOCK_TO_CHAR:
                shifted_text += BLOCK_TO_CHAR[t]
            else:
                shifted_text += " "

        plaintext = caesar_unshift(shifted_text, shift)

        st.subheader("🔓 Plaintext Hasil Dekripsi")
        st.code(plaintext)
