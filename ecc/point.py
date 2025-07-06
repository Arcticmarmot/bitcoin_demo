from ecc.field_element import S256Field

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
        # coef = coefficient
        # current = self
        # result = self.__class__(None, None, self.a, self.b)
        # while coef:
        #     if coef & 1:
        #         result += current
        #     current += current
        #     coef >>= 1
        # return result
        result = self.__class__(None, None, self.a, self.b)
        for _ in range(coefficient):
            result += self
            print(_, result)
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
class S256Point(Point):
    def __init__(self, x, y, a = None, b = None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x = S256Field(x), y = S256Field(y), a = a, b = b)
        else:
            super().__init__(x = x, y = y, a = a, b = b)

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
print((N - 3) * G)