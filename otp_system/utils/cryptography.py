from cryptography.fernet import Fernet


class EncryptDecryptMixin:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.cipher_suite = Fernet(self.secret_key)

    def encrypt(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode('utf-8')

    def decrypt(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(
            encrypted_data.encode()
        ).decode()
        return decrypted_data
