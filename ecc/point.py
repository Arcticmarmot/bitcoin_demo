from random import randint
from ecc.field_element import S256Field
from ecc.helper import little_endian_to_int
from helper import hash160, encode_base58_checksum

class Point:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None or self.y is None:
            return
        if self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError('({}, {}) is not on the curve'.format(x, y))

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        if self == other:
            if self.y == 0 * self.x:
                return self.__class__(None, None, self.a, self.b)
            s = (3 * self.x ** 2 + self.a) / (2 * self.y)
        else:
            s = (other.y - self.y) / (other.x - self.x)
        x3 = s ** 2 - self.x - other.x
        y3 = s * (self.x - x3) - self.y
        return self.__class__(x3, y3, self.a, self.b)

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
P = 2**256 - 2**32 - 977

class S256Point(Point):
    def  __init__(self, x, y, a = None, b = None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x = S256Field(x), y = S256Field(y), a = a, b = b)
        else:
            super().__init__(x = x, y = y, a = a, b = b)

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        """returns the address string"""
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)

    def sec(self, compressed=True):
        """return the binary version of the SEC format"""
        if compressed:
            if self.y.num % 2:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

    def parse(self, sec_bin):
        """return a Point object from an SEC binary (not hex)"""
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x, y)
        is_even = sec_bin[0] == 2
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

    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u * G + v * self
        return total.x.num == sig.r

G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def der(self):
        rbin = self.r.to_bytes(32, byteorder='big')
        rbin = rbin.lstrip(b'\x00')
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, byteorder='big')
        sbin = sbin.lstrip(b'\x00')
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result

    def __repr__(self):
        return 'Signature({:x},{:x})'.format(self.r, self.s)

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, N)
        r = (k * G).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def wif(self, compressed=True, testnet=False):
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


# key = PrivateKey(5001)
# print(key.point.sec().hex())
# key = PrivateKey(2018 ** 2)
# print(key.point.sec().hex())
# key = PrivateKey(0xdeadbeef1)
# print(key.point)
# print(key.point.sec().hex())
# print(key.point.parse(key.point.sec()))
# # key = PrivateKey(int.from_bytes(hash256(b'my secret'), 'big'))
# # z = int.from_bytes(hash256(b'hello world'), 'big')
# # sign = key.sign(z)
# # sign.s += 0
# # print(sign)
# # print(key.point.verify(z, sign))
# r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
# s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
# sig = Signature(r,s)
# print(sig.der().hex())
# key = PrivateKey(5002)
# print(key.point.address(compressed=False, testnet=True))
# key = PrivateKey(5003)
# print(key.wif(compressed=True, testnet=True))

my_key = PrivateKey(little_endian_to_int(b"hello friend"))
print(my_key.secret, 'secret')
print(my_key.wif(testnet=True), 'wif')
print(my_key.point.address(testnet=True))
