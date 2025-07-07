from unittest import TestSuite, TextTestRunner
import hashlib

def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

def hash256(s):
    # two rounds of sha256
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
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

def little_endian_to_int(lbs):
    result = 0
    current = 1
    for i in range(0, len(lbs)):
        result += lbs[i] * current
        current *= 256
    return result

def int_to_little_endian(num):
    result = []
    while num > 0:
        num, sub_byte = divmod(num, 256)
        result.append(sub_byte)
    return bytes(result)

# b = bytes([10, 30, 30, 50, 99])
# n = 1000435345
# print(little_endian_to_int(b))
# print(int.from_bytes(b, 'little'))
# byte = int_to_little_endian(n)
# print(byte)
# print(little_endian_to_int(byte))
