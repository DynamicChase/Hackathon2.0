import socket
import os
import logging
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    filename='client.log',  # Log file name
    level=logging.INFO,      # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

def load_key():
    return open("Secret.key", "rb").read()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def send_file(client_socket, filename, key):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            file_data = f.read()
            encrypted_file_data = encrypt_data(file_data, key)  # Pass the key here
            
            # Send encrypted file data to server
            client_socket.sendall(encrypted_file_data)
            logging.info(f"Sent {filename} successfully.")
    
            # Receive acknowledgment from server
            encrypted_response = client_socket.recv(1024)
            decrypted_response = Fernet(key).decrypt(encrypted_response)
            logging.info("Server Response: %s", decrypted_response.decode())
    else:
        logging.error(f"File '{filename}' not found.")

def main():
    key = load_key()  # Load the key
    
    # Setup socket connection to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    while True:
        filename = input("Enter the full path of the file to send (or type 'exit' to quit): ")
        if filename.lower() == 'exit':
            logging.info("Client exited.")
            break
        send_file(client_socket, filename, key)

    client_socket.close()
    logging.info("Connection closed.")

if __name__ == "__main__":
    main()
