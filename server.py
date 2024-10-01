import socket
import logging
from cryptography.fernet import Fernet, InvalidToken

# Configure logging
logging.basicConfig(
    filename='server.log',  # Log file name
    level=logging.INFO,      # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

class UniversalSwitchSet:
    def __init__(self):
        self.key = self.load_key()  # Load pre-generated key

    def load_key(self):
        return open("Secret.key", "rb").read()  # Load the encryption key from a file

    def encrypt_data(self, data):
        f = Fernet(self.key)
        return f.encrypt(data)  # Encrypt data using the loaded key

    def decrypt_data(self, encrypted_data):
        f = Fernet(self.key)
        return f.decrypt(encrypted_data)  # Decrypt data using the loaded key

def start_server():
    switch_set = UniversalSwitchSet()
    
    # Setup socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(1)  # Listen for incoming connections
    print('Server Started')
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
            decrypted_data = switch_set.decrypt_data(encrypted_data)

            # Log the content of the decrypted data (assuming it's in JSON format)
            logging.info(f"Received file content: {decrypted_data.decode()}")  # Log decrypted content
            
            # Save the decrypted data to a file
            with open("received_file.json", "wb") as f:
                f.write(decrypted_data)
            
            logging.info("File received and decrypted successfully.")
            
            # Encrypt response
            response = "Acknowledged".encode()
            encrypted_response = switch_set.encrypt_data(response)
            
            # Send encrypted response back
            conn.sendall(encrypted_response)

        except InvalidToken:
            logging.error("Invalid token! The received data may be corrupted or use a different key.")
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            break

    conn.close()  # Close the connection when done
    logging.info("Connection closed.")

if __name__ == "__main__":
    start_server()  # Start the server when the script is run
