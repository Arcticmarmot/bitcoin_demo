from ecc import FieldElement
from ecc import Point

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
x = FieldElement(192,223)
y = FieldElement(105,223)
p1 = Point(x, y, a, b)
print(p1.x, p1.y)