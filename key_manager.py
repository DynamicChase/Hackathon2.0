import os
from cryptography.fernet import Fernet

class KeyManager:
    def __init__(self, key_file='Secret.key'):
        self.key_file = key_file
        self.key = self.load_key()

    def generate_key(self):
        """Generate a new Fernet key and save it to a file."""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        return key

    def load_key(self):
        """Load the encryption key from a file."""
        if not os.path.exists(self.key_file):
            return self.generate_key()
        
        # Load the key as bytes
        key = open(self.key_file, 'rb').read()
        
        # Check the length of the key
        if len(key) > 32:
            raise ValueError("Key must be at most 32 bytes long.")
        
        return key  # Return the key as bytes for AES compatibility

