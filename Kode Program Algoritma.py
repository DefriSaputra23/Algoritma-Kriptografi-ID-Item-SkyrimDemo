import streamlit as st
import string

# =========================
# DATASET
# =========================
ALPHABET = string.ascii_uppercase

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

# Reverse lookup untuk dekripsi
REVERSE_ITEM_MAP = {v: k for k, v in ITEM_ID_MAP.items()}

CATEGORY_COUNT = 5

# =========================
# FUNGSI UTILITAS
# =========================
def key_to_number(key):
    return sum(ALPHABET.index(k) + 1 for k in key)

def caesar_shift(text, shift):
    result = ""
    for char in text:
        idx = ALPHABET.index(char)
        result += ALPHABET[(idx + shift) % 26]
    return result

def caesar_unshift(text, shift):
    result = ""
    for char in text:
        idx = ALPHABET.index(char)
        result += ALPHABET[(idx - shift) % 26]
    return result

def extract_suffix_middle(item_id):
    suffix = item_id[-2:]
    middle = item_id[-4:-2]
    return suffix + middle

def rebuild_item_id(block):
    suffix = block[:2]
    middle = block[2:]
    return "0001" + middle + suffix

# =========================
# STREAMLIT UI
# =========================
st.title("🔐 Skyrim Cryptography Demo")
st.caption("Enkripsi & Dekripsi berbasis Item ID Skyrim")

mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

key = st.text_input("Masukkan Key", "").upper()

# =========================
# ENKRIPSI
# =========================
if mode == "Enkripsi":
    plaintext = st.text_input("Masukkan Plaintext", "").upper()

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

# =========================
# DEKRIPSI
# =========================
else:
    ciphertext = st.text_area("Masukkan Ciphertext (pisahkan dengan spasi)")

    if st.button("Decrypt"):
        if ciphertext and key:
            blocks = ciphertext.split()

            total_key = key_to_number(key)
            shift = (total_key + len(blocks) + len(key)) % CATEGORY_COUNT

            st.subheader("🔢 Detail Perhitungan")
            st.write("Nilai shift:", shift)

            shifted_text = ""
            st.subheader("🧩 Rekonstruksi Item ID")
            for block in blocks:
                item_id = rebuild_item_id(block)
                char = REVERSE_ITEM_MAP.get(item_id, "?")
                shifted_text += char
                st.write(f"{block} → {item_id} → {char}")

            st.subheader("🔁 Caesar Shift Balik")
            plaintext = caesar_unshift(shifted_text, shift)
            st.code(plaintext)
        else:
            st.warning("Ciphertext dan Key tidak boleh kosong!")
