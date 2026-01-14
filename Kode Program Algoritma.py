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
    return "".join(
        ALPHABET[(ALPHABET.index(c) + shift) % 26] if c in ALPHABET else c
        for c in text
    )

def caesar_unshift(text, shift):
    return "".join(
        ALPHABET[(ALPHABET.index(c) - shift) % 26] if c in ALPHABET else c
        for c in text
    )

def extract_block(item_id):
    return item_id[-2:] + item_id[-4:-2]

BLOCK_TO_CHAR = {
    extract_block(item_id): char
    for char, item_id in ITEM_ID_MAP.items()
}

# ======================================================
# ENCRYPTION CORE (WITH SILENT LOG)
# ======================================================
def encrypt(plaintext, key):
    log = []

    log.append(f"Plaintext: {plaintext}")
    log.append(f"Key: {key}")

    total_key = key_to_number(key)
    huruf_count = sum(1 for c in plaintext if c in ALPHABET)
    shift = (total_key + huruf_count + len(key)) % CATEGORY_COUNT

    log.append(f"Total key value: {total_key}")
    log.append(f"Alphabet count: {huruf_count}")
    log.append(f"Final shift: {shift}")

    shifted = caesar_shift(plaintext, shift)
    log.append(f"Caesar result: {shifted}")

    blocks = []
    for c in shifted:
        if c in ALPHABET:
            block = extract_block(ITEM_ID_MAP[c])
            blocks.append(block)
            log.append(f"{c} -> {block}")
        else:
            blocks.append(c)
            log.append("Space preserved")

    ciphertext = " ".join(blocks)
    log.append(f"Ciphertext: {ciphertext}")

    return ciphertext, log

# ======================================================
# STREAMLIT UI
# ======================================================
st.title("🔐 Skyrim Cryptography Demo")
st.caption("Clean UI dengan Logging Proses Enkripsi")

mode = st.radio("Mode Operasi", ["Enkripsi", "Dekripsi"])
key = st.text_input("Masukkan Key").upper()

# ======================================================
# ENKRIPSI UI (BERSIH)
# ======================================================
if mode == "Enkripsi":
    plaintext = st.text_area("Masukkan Plaintext").upper()

    if st.button("Encrypt"):
        if not plaintext or not key:
            st.warning("Plaintext dan Key wajib diisi!")
            st.stop()

        ciphertext, log = encrypt(plaintext, key)

        st.subheader("🔐 Ciphertext")
        st.code(ciphertext)

        with st.expander("📜 Lihat Log Proses Enkripsi"):
            for line in log:
                st.write(line)

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

        shifted_text = "".join(
            BLOCK_TO_CHAR[t] if t in BLOCK_TO_CHAR else " "
            for t in tokens
        )

        plaintext = caesar_unshift(shifted_text, shift)

        st.subheader("🔓 Plaintext")
        st.code(plaintext)
