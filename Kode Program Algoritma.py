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
# FUNGSI UTILITAS
# ======================================================
def key_to_number(key):
    return sum(ALPHABET.index(k) + 1 for k in key)

def caesar_shift(text, shift):
    return "".join(
        ALPHABET[(ALPHABET.index(c) + shift) % 26] for c in text
    )

def caesar_unshift(text, shift):
    return "".join(
        ALPHABET[(ALPHABET.index(c) - shift) % 26] for c in text
    )

def extract_block(item_id):
    suffix = item_id[-2:]
    middle = item_id[-4:-2]
    return suffix + middle

# ======================================================
# INVERSE MAPPING (REVISI PENTING)
# ======================================================
BLOCK_TO_CHAR = {
    extract_block(item_id): char
    for char, item_id in ITEM_ID_MAP.items()
}

# ======================================================
# STREAMLIT UI
# ======================================================
st.title("🔐 Skyrim Cryptography Demo")
st.caption("Enkripsi & Dekripsi menggunakan Item ID Skyrim")

mode = st.radio("Mode Operasi", ["Enkripsi", "Dekripsi"])
key = st.text_input("Masukkan Key", "").upper()

# ======================================================
# ENKRIPSI
# ======================================================
if mode == "Enkripsi":
    plaintext = st.text_input("Masukkan Plaintext", "").upper()

    if st.button("Encrypt"):
        if not plaintext or not key:
            st.warning("Plaintext dan Key wajib diisi!")
            st.stop()

        total_key = key_to_number(key)
        shift = (total_key + len(plaintext) + len(key)) % CATEGORY_COUNT

        st.subheader("🔢 Perhitungan Shift")
        st.write("Total nilai key:", total_key)
        st.write("Nilai shift:", shift)

        shifted = caesar_shift(plaintext, shift)
        st.subheader("🔁 Caesar Shift Result")
        st.code(shifted)

        blocks = []
        st.subheader("🗃️ Mapping Item ID")
        for char in shifted:
            item_id = ITEM_ID_MAP[char]
            block = extract_block(item_id)
            blocks.append(block)
            st.write(f"{char} → {item_id} → {block}")

        st.subheader("🔐 Ciphertext Akhir")
        st.code(" ".join(blocks))

# ======================================================
# DEKRIPSI
# ======================================================
else:
    ciphertext = st.text_area("Masukkan Ciphertext (pisahkan dengan spasi)")

    if st.button("Decrypt"):
        if not ciphertext or not key:
            st.warning("Ciphertext dan Key wajib diisi!")
            st.stop()

        blocks = ciphertext.strip().split()

        total_key = key_to_number(key)
        shift = (total_key + len(blocks) + len(key)) % CATEGORY_COUNT

        st.subheader("🔢 Perhitungan Shift")
        st.write("Nilai shift:", shift)

        shifted_text = ""
        st.subheader("🧩 Inverse Mapping Ciphertext")

        for block in blocks:
            char = BLOCK_TO_CHAR.get(block)
            if char is None:
                st.error(f"Ciphertext tidak valid: {block}")
                st.stop()
            shifted_text += char
            st.write(f"{block} → {char}")

        plaintext = caesar_unshift(shifted_text, shift)

        st.subheader("🔓 Plaintext Hasil Dekripsi")
        st.code(plaintext)
