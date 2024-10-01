import socket
import os
from cryptography.fernet import Fernet

def load_key():
    return open("Secret.key", "rb").read()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def send_file(client_socket, filename, key):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            file_data = f.read()
            encrypted_file_data = encrypt_data(file_data, key)  # Encrypt the file data
            
            # Send encrypted file data to server
            client_socket.sendall(encrypted_file_data)
            print(f"Sent {filename} successfully.")
    
            # Receive acknowledgment from server
            encrypted_response = client_socket.recv(1024)
            decrypted_response = Fernet(key).decrypt(encrypted_response)
            print("Server Response:", decrypted_response.decode())
    else:
        print(f"File '{filename}' not found.")

def main():
    key = load_key()  # Load the key
    
    # Setup socket connection to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    while True:
        filename = input("Enter the full path of the file to send (or type 'exit' to quit): ")
        if filename.lower() == 'exit':
            break
        send_file(client_socket, filename, key)

    client_socket.close()

if __name__ == "__main__":
    main()
