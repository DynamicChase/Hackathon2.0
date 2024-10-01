import socket
import logging
from key_manager import KeyManager
from file_handler import FileHandler

# Configure logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_server():
    # Import Encryption here to avoid circular dependency issues
    from encryption import Encryption
    
    # Initialize KeyManager and Encryption classes with AES algorithm (change to 'fernet' for Fernet)
    key_manager = KeyManager()
    encryption = Encryption(key_manager.key, algorithm='aes')  # Change to 'fernet' for Fernet

    # Setup socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(1)  # Listen for incoming connections

    logging.info("Waiting for connection...")
    
    conn, addr = server_socket.accept()  # Accept a connection
    logging.info(f"Connection established with {addr}")

    while True:
        try:
            # Receive data
            encrypted_data = conn.recv(1024)  # Receive up to 1024 bytes of encrypted data

            if not encrypted_data:
                logging.info("No data received; closing connection.")
                break

            # Decrypt received data
            decrypted_data = encryption.decrypt_data(encrypted_data)

            # Save the decrypted data to a file (consider naming convention based on timestamp or sender)
            FileHandler.write_file("received_file.json", decrypted_data)

            logging.info("File received and decrypted successfully.")

            # Encrypt response and send back acknowledgment
            response = "Acknowledged".encode()  
            encrypted_response = encryption.encrypt_data(response)
            conn.sendall(encrypted_response)

        except Exception as e:
            logging.error(f"Error: {e}")
            break

    conn.close()  # Close the connection when done
    logging.info("Connection closed.")

if __name__ == "__main__":
    start_server()  # Start the server when the script is run

