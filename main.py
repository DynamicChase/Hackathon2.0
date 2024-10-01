import streamlit as st
from cryptography.fernet import Fernet

# Function to generate a key and create a Fernet cipher
def generate_key():
    return Fernet.generate_key()

# Function to encrypt data
def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted

# Function to decrypt data
def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    return decrypted

# Streamlit UI
st.title("Universal Switch Set with Data Encryption and Decryption")

# Initialize session state for key if it doesn't exist
if 'key' not in st.session_state:
    st.session_state.key = generate_key()
    st.success("Encryption key generated.")

# Display current encryption key
st.write(f"Current Encryption Key: {st.session_state.key.decode()}")

# Input for sensitive data
st.subheader("Data Input")
data_input = st.text_area("Enter sensitive data:")

# Buttons for encryption and decryption
if st.button("Encrypt Data"):
    if data_input:
        encrypted_data = encrypt_data(st.session_state.key, data_input)
        st.success(f"Encrypted Data: {encrypted_data.decode()}")
    else:
        st.warning("Please enter some data to encrypt.")

if st.button("Decrypt Data"):
    if 'encrypted_data' in locals():
        decrypted_data = decrypt_data(st.session_state.key, encrypted_data)
        st.success(f"Decrypted Data: {decrypted_data}")
    else:
        st.warning("No encrypted data available to decrypt.")

# Optionally, allow users to download the key (for demonstration purposes)
if st.button("Download Key"):
    key_file = "key.txt"
    with open(key_file, "w") as f:
        f.write(st.session_state.key.decode())
    st.success(f"Key downloaded as {key_file}.")

