from otp_system.utils.cryptography import EncryptDecryptMixin
from otp_system.utils.randnum import RandomNumberMixin


class OTPManager(EncryptDecryptMixin, RandomNumberMixin):

    def __init__(self, secret_key):
        super().__init__(secret_key)

    def generate_otp(self, data):
        encrypted_otp = self.encrypt(data)
        return encrypted_otp

    def validate_otp(self, submitted_otp, generated_otp):
        decrypted_otp = self.decrypt(generated_otp)
        return decrypted_otp == submitted_otp
