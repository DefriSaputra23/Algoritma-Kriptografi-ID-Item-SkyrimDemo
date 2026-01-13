import streamlit as st
import string

# ======================================================
# DATASET
# ======================================================
ALPHABET = string.ascii_uppercase
CATEGORY_COUNT = 5

ITEM_ID_MAP = {
    'A': '0001398A', 'B': '0003EAE2', 'C': '0001398D', 'D': '000A4848',
    'E': '00013955', 'F': '0003EADE', 'G': '0001396B', 'H': '0004E4EE',
    'I': '00043E28', 'J': '0003EAF2', 'K': '0001397A', 'L': '0003EA12',
    'M': '000139AA', 'N': '0003EB22', 'O': '000139BB', 'P': '0003EC12',
    'Q': '000139CC', 'R': '0003ED12', 'S': '000139DD', 'T': '0003EE12',
    'U': '000139EE', 'V': '0003EF12', 'W': '000139FF', 'X': '0003F012',
    'Y': '000139AB', 'Z': '0003F112'
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
