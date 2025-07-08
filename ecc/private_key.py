from random import randint

from ecc.helper import N, G, encode_base58_checksum
from ecc.signature import Signature

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret # secret is a num
        self.__point__ = secret * G # public key

    def sign(self, z):
        k = randint(0, N)
        r = (k * G).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

    def get_public_key(self):
        return self.__point__

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def wif(self, compressed=True, testnet=False):
        """
        Return the wif format of the secret
        """
        secret_bytes = self.secret.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)