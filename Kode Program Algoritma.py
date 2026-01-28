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
# ENKRIPSI (DENGAN LOG LENGKAP)
# ======================================================
def encrypt(plaintext, key):
    log = []

    log.append(f"Plaintext awal: {plaintext}")
    log.append(f"Key: {key}")

    total_key = key_to_number(key)
    huruf_count = sum(1 for c in plaintext if c in ALPHABET)
    shift = (total_key + huruf_count + len(key)) % CATEGORY_COUNT

    log.append(f"Total key value: {total_key}")
    log.append(f"Alphabet count: {huruf_count}")
    log.append(f"Final shift: {shift}")

    shifted = caesar_shift(plaintext, shift)
    log.append(f"Hasil Caesar Shift: {shifted}")

    blocks = []
    log.append("Mapping karakter ke Item ID:")

    for c in shifted:
        if c in ALPHABET:
            full_id = ITEM_ID_MAP[c]
            block = extract_block(full_id)
            blocks.append(block)

            log.append(
                f"{c} → Item ID FULL: {full_id} → Block: {block}"
            )
        else:
            blocks.append(c)
            log.append("Spasi dipertahankan")

    ciphertext = " ".join(blocks)
    log.append(f"Ciphertext akhir: {ciphertext}")

    return ciphertext, log

# ======================================================
# DEKRIPSI (DENGAN LOG LENGKAP)
# ======================================================
def decrypt(ciphertext, key):
    log = []

    tokens = ciphertext.split(" ")
    log.append(f"Ciphertext: {ciphertext}")
    log.append(f"Key: {key}")

    total_key = key_to_number(key)
    huruf_count = sum(1 for t in tokens if t in BLOCK_TO_CHAR)
    shift = (total_key + huruf_count + len(key)) % CATEGORY_COUNT

    log.append(f"Final shift: {shift}")

    shifted_text = ""
    log.append("Mapping block ke karakter:")

    for t in tokens:
        if t in BLOCK_TO_CHAR:
            char = BLOCK_TO_CHAR[t]
            full_id = ITEM_ID_MAP[char]

            shifted_text += char
            log.append(
                f"Block: {t} → Item ID FULL: {full_id} → Huruf: {char}"
            )
        else:
            shifted_text += " "
            log.append("Spasi dipertahankan")

    plaintext = caesar_unshift(shifted_text, shift)
    log.append(f"Plaintext akhir: {plaintext}")

    return plaintext, log

# ======================================================
# STREAMLIT UI
# ======================================================
st.title("🔐 Skyrim Cryptography Demo")
st.caption("Kriptografi menggunakan Game Skyrim")

st.markdown("### 📂 Dokumentasi & Dataset")
st.markdown(
    "[🔗 Lihat Dataset & Dokumentasi](https://drive.google.com/drive/folders/1CqIbSM2IWldEGEs19m1jf85rn9GWHttZ?usp=sharing)",
    unsafe_allow_html=True
)
mode = st.radio("Mode Operasi", ["Enkripsi", "Dekripsi"])
key = st.text_input("Masukkan Key").upper()

# ======================================================
# ENKRIPSI UI
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

        with st.expander("📜 Log Enkripsi (Detail Lengkap)"):
            for line in log:
                st.write(line)

# ======================================================
# DEKRIPSI UI
# ======================================================
else:
    ciphertext = st.text_area("Masukkan Ciphertext")

    if st.button("Decrypt"):
        if not ciphertext or not key:
            st.warning("Ciphertext dan Key wajib diisi!")
            st.stop()

        plaintext, log = decrypt(ciphertext, key)

        st.subheader("🔓 Plaintext")
        st.code(plaintext)

        with st.expander("📜 Log Dekripsi (Detail Lengkap)"):
            for line in log:
                st.write(line)
