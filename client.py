import socket
import logging
from key_manager import KeyManager
from file_handler import FileHandler

# Configure logging
logging.basicConfig(
    filename='client.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_file(client_socket, filename, encryption):
    """Send an encrypted file to the server."""
    try:
        file_data = FileHandler.read_file(filename)  # Read file as bytes
        
        # Encrypt the file data; ensure it's in bytes format.
        encrypted_file_data = encryption.encrypt_data(file_data)  
        
        # Send encrypted file data to server
        client_socket.sendall(encrypted_file_data)
        
        logging.info(f"Sent {filename} successfully.")

        # Receive acknowledgment from server
        encrypted_response = client_socket.recv(1024)
        
        decrypted_response = encryption.decrypt_data(encrypted_response)
        
        print("Server Response:", decrypted_response.decode())
    
    except Exception as e:
        logging.error(f"Error sending file '{filename}': {e}")
        print(e)

def main():
    # Initialize KeyManager and Encryption classes with AES algorithm (change to 'fernet' for Fernet)
    key_manager = KeyManager()
    
    # Import Encryption here to avoid circular dependency issues 
    from encryption import Encryption
    
    encryption = Encryption(key_manager.key, algorithm='aes')  # Change to 'fernet' for Fernet

    # Setup socket connection to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', 12345))
        
        logging.info("Connected to server.")

        while True:
            filename = input("Enter the full path of the file to send (or type 'exit' to quit): ")
            
            if filename.lower() == 'exit':
                break
            
            send_file(client_socket, filename, encryption)
    
    except Exception as e:
        logging.error(f"Connection error: {e}")
    
    finally:
        client_socket.close()
        
        logging.info("Connection closed.")

if __name__ == "__main__":
    main()

