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
            result += c   # spasi / simbol dibiarkan
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
key = st.text_input("Masukkan Key", "").upper()


# ======================================================
# ENKRIPSI
# ======================================================
if mode == "Enkripsi":
    plaintext = st.text_area("Masukkan Plaintext").upper()

    if st.button("Encrypt"):
        if not plaintext or not key:
            st.warning("Plaintext dan Key wajib diisi!")
            st.stop()

        total_key = key_to_number(key)
        huruf_count = sum(1 for c in plaintext if c in ALPHABET)
        shift = (total_key + huruf_count + len(key)) % CATEGORY_COUNT

        st.subheader("🔢 Perhitungan Shift")
        st.write("Total nilai key:", total_key)
        st.write("Jumlah huruf alfabet:", huruf_count)
        st.write("Nilai shift:", shift)

        shifted = caesar_shift(plaintext, shift)
        st.subheader("🔁 Caesar Shift Result")
        st.code(shifted)

        blocks = []
        st.subheader("🗃️ Mapping Item ID")

        for c in shifted:
            if c in ALPHABET:
                block = extract_block(ITEM_ID_MAP[c])
                blocks.append(block)
                st.write(f"{c} → {block}")
            else:
                blocks.append(c)  # spasi tetap

        st.subheader("🔐 Ciphertext Akhir")
        st.code(" ".join(blocks))

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

        st.subheader("🔢 Perhitungan Shift")
        st.write("Nilai shift:", shift)

        shifted_text = ""

        for t in tokens:
            if t in BLOCK_TO_CHAR:
                shifted_text += BLOCK_TO_CHAR[t]
            else:
                shifted_text += " "

        plaintext = caesar_unshift(shifted_text, shift)

        st.subheader("🔓 Plaintext Hasil Dekripsi")
        st.code(plaintext)
