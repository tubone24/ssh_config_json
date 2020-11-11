import base64
import hashlib
import string
import os
from random import SystemRandom
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding


class AESCipher(object):
    def __init__(self, key=None, key_num=32):
        if key is not None:
            self.key = (hashlib.shake_128(key.encode("utf-8")).hexdigest(16)).encode(
                "utf-8"
            )
        else:
            self.raw_key = self._create_key(key_num)
            print(f"Encrypt key: {self.raw_key}")
            self.key = (
                hashlib.shake_128(self.raw_key.encode("utf-8")).hexdigest(16)
            ).encode("utf-8")

    @staticmethod
    def _create_key(key_num=32):
        return "".join(
            [
                SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(key_num)
            ]
        )

    def encrypt(self, raw_text):
        initialization_vector = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_EAX, initialization_vector)
        data = Padding.pad(raw_text.encode("utf-8"), AES.block_size, "pkcs7")
        return base64.b64encode(initialization_vector + cipher.encrypt(data))

    def decrypt(self, encrypted):
        encrypted = base64.b64decode(encrypted)
        iv = encrypted[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_EAX, iv)
        data = Padding.unpad(
            cipher.decrypt(encrypted[AES.block_size :]), AES.block_size, "pkcs7"
        )
        return data.decode("utf-8")

    def encrypt_file(self, path, delete_raw_file=False):
        with open(path, "r") as f1, open(path + ".enc", "wb") as f2:
            f2.write(self.encrypt(f1.read()))
        if delete_raw_file:
            os.remove(path)
        print(f"Encrypted file: {path}.enc")

    def decrypt_file(self, path, delete_raw_file=False):
        with open(path, "rb") as f1, open(path.replace(".enc", ""), "w") as f2:
            f2.write(self.decrypt(f1.read()))
        if delete_raw_file:
            os.remove(path)
