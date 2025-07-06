from ecc import FieldElement
from ecc import Point
from ecc import ECCTest
from ecc.helper import run

a = FieldElement(5, 13)
b = FieldElement(12, 13)
c = FieldElement(5, 17)
d = FieldElement(7, 13)
e = FieldElement(8, 13)
print(d ** -3 == e)
print(a == b)
print(a == a)
print(a + b)
print(a - b)
print(a / b)

p1 = Point(2, 5, 5, 7)
p2 = Point(-1, -1, 5, 7)
p3 = p1 + p2
p4 = p2 + p2
print(p3.x, p3.y)
print(p4.x, p4.y)

a = FieldElement(0, 223)
b = FieldElement(7,223)
x1 = FieldElement(192,223)
y1 = FieldElement(105,223)
x2 = FieldElement(17, 223)
y2 = FieldElement(56, 223)
p1 = Point(x1, y1, a, b)
p2 = Point(x2, y2, a, b)
p3 = p1 + p2
print(p3.x, p3.y)
run(ECCTest('test_on_curve'))
run(ECCTest('test_add'))

gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
p = 2**256 - 2**32 - 977
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
x = FieldElement(gx, p)
y = FieldElement(gy, p)
seven = FieldElement(7, p)
zero = FieldElement(0, p)

G = Point(x, y, zero, seven)
print(G)
nG = n * G
print(nG.x, nG.y)



