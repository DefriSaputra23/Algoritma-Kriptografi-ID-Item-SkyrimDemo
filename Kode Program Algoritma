import streamlit as st
import string

# =========================
# DATASET SEDERHANA
# =========================
ALPHABET = string.ascii_uppercase

ITEM_ID_MAP = {
    'A': '0001398A',
    'B': '0003EAE2',
    'C': '0001398D',
    'D': '000A4848',
    'E': '00013955',
    'F': '0003EADE',
    'G': '0001396B',
    'H': '0004E4EE',
    'I': '00043E28',
    'J': '0003EAF2',
    'K': '0001397A',
    'L': '0003EA12',
    'M': '000139AA',
    'N': '0003EB22',
    'O': '000139BB',
    'P': '0003EC12',
    'Q': '000139CC',
    'R': '0003ED12',
    'S': '000139DD',
    'T': '0003EE12',
    'U': '000139EE',
    'V': '0003EF12',
    'W': '000139FF',
    'X': '0003F012',
    'Y': '000139AB',
    'Z': '0003F112'
}

CATEGORY_COUNT = 5

# =========================
# FUNGSI
# =========================
def key_to_number(key):
    return sum(ALPHABET.index(k) + 1 for k in key)

def caesar_shift(text, shift):
    result = ""
    for char in text:
        idx = ALPHABET.index(char)
        result += ALPHABET[(idx + shift) % 26]
    return result

def extract_suffix_middle(item_id):
    suffix = item_id[-2:]
    middle = item_id[-4:-2]
    return suffix + middle

# =========================
# STREAMLIT UI
# =========================
st.title("🔐 Skyrim Cryptography Demo")
st.caption("Algoritma Kriptografi berbasis Item ID Skyrim")

plaintext = st.text_input("Masukkan Plaintext", "").upper()
key = st.text_input("Masukkan Key", "").upper()

if st.button("Encrypt"):
    if plaintext and key:
        total_key = key_to_number(key)
        shift = (total_key + len(plaintext) + len(key)) % CATEGORY_COUNT

        st.subheader("🔢 Detail Perhitungan")
        st.write("Total nilai key:", total_key)
        st.write("Nilai shift:", shift)

        shifted_text = caesar_shift(plaintext, shift)
        st.subheader("🔁 Caesar Shift Result")
        st.code(shifted_text)

        cipher_blocks = []
        st.subheader("🗃️ Mapping Item ID")
        for char in shifted_text:
            item_id = ITEM_ID_MAP[char]
            block = extract_suffix_middle(item_id)
            cipher_blocks.append(block)
            st.write(f"{char} → {item_id} → {block}")

        st.subheader("🔐 Ciphertext Akhir")
        st.code(" ".join(cipher_blocks))
    else:
        st.warning("Plaintext dan Key tidak boleh kosong!")
