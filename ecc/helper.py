from unittest import TestSuite, TextTestRunner
import hashlib

from ecc.field_element import S256Field
from ecc.point import S256Point

A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
P = 2**256 - 2**32 - 977
G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

def hash256(s):
    # two rounds of sha256
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    print(num)
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def hash160(s):
    """sha256 followed by ripemd160"""
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def parse_sec(self, sec_bin):
    """return a Point object from an SEC binary (not hex)"""
    prefix = sec_bin[0]
    if prefix == 4:
        x = int.from_bytes(sec_bin[1:33], 'big')
        y = int.from_bytes(sec_bin[33:65], 'big')
        return S256Point(x, y)
    is_even = prefix == 2
    x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
    alpha = x ** 3 + S256Field(B)
    beta = alpha.sqrt()
    if beta.num % 2 == 0:
        even_beta = beta
        odd_beta = S256Field(P - beta.num)
    else:
        even_beta = S256Field(P - beta.num)
        odd_beta = beta
    if is_even:
        return S256Point(x, even_beta)
    else:
        return S256Point(x, odd_beta)
