from unittest import TestCase

from ecc import FieldElement
from ecc import Point

class ECCTest(TestCase):
    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        x1 = FieldElement(192, 223)
        y1 = FieldElement(105, 223)
        x2 = FieldElement(17, 223)
        y2 = FieldElement(56, 223)

        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        p3 = p1 + p2

        x3 = FieldElement(47, 223)
        y3 = FieldElement(71, 223)
        p4 = Point(x3, y3, a, b)
        p8 = 2 * p4
        print(p8.x, p8.y)
        print(p3.x, p3.y)