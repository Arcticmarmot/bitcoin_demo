from field_element import S256Field
from helper import hash160, encode_base58_checksum
from params import N, A, B, Gx, Gy

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
        """
        Add two points on the elliptic curve defined by y^2 = x^3 + a*x + b.

        :param other: second point

        :return: the result of self + other
        """
        # Ensure both points share the same curve parameters
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format(self, other))

        # Handle the point at infinity(identity element)
        if self.x is None:
            return other
        if other.x is None:
            return self

        # Opposite points have same x, negated y
        if self.x == other.x and self.y == -1 * other.y:
            return self.__class__(None, None, self.a, self.b)

        # Compute slope(s)
        if self == other:
            s = (3 * self.x ** 2 + self.a) / (2 * self.y)
        else:
            s = (other.y - self.y) / (other.x - self.x)
        # Compute resulting coordinates
        x = s ** 2 - self.x - other.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)

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

    def sec(self, compressed=True):
        """
        :return: the binary version of the SEC(Standard for Efficient Cryptograpy) format
        """
        if compressed:
            if self.y.num % 2:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

    def address(self, compressed=True, testnet=False):
        """
        :return: the address string
        """
        h160 = hash160(self.sec(compressed))
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)

    def verify(self, z, sig):
        """
        Verify that the given signature is valid for this public key and message hash

        :param z: Integer hash of the message being verified
        :param sig: Signature(r,s)

        :return: boolean
        """
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        R = u * S256Point(Gx, Gy) + v * self
        return R.x.num == sig.r

    def parse(self, sec_bin):
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