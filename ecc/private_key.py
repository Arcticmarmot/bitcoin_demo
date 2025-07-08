from random import randint

from point import S256Point
from helper import encode_base58_checksum
from signature import Signature
from params import N, Gx, Gy

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret # secret is a num
        self.point = secret * S256Point(Gx, Gy) # public key

    def sign(self, z):
        k = randint(0, N)
        r = (k * S256Point(Gx, Gy)).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

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