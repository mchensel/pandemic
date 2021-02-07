import unittest
from pandemic import *
from Cities import *


def init():
    for color_city in CITIES.values():
        for l_city in color_city:
            l_city.reset()


def init_standard_setting():
    """
    1*TRIPOLIS, CHICAGO
    2*NY
    3*LAGOS
    4*KAIRO
    :return:
    """
    init()
    add_city(TRIPOLIS)
    add_city(NEW_YORK)
    add_city(NEW_YORK)
    add_city(LAGOS)
    add_city(LAGOS)
    add_city(LAGOS)
    add_city(CHICAGO)
    add_city(KAIRO)
    add_city(KAIRO)
    add_city(KAIRO)
    add_city(KAIRO)


def init_complicated_setting():
    init_standard_setting()
    epidemie(ISTANBUL)
    add_city(LAGOS)
    add_city(LAGOS)
    add_city(KAIRO)
    epidemie(NEW_YORK)
    add_city(NEW_YORK)
    add_city(LAGOS)


class TestPandemic(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPandemic, self).__init__(*args, **kwargs)
        init()

    def test_add_city(self):
        add_city(ISTANBUL)
        self.assertEqual(ISTANBUL.phase, [3, 1])

    def test_epidemie_generell(self):
        init_standard_setting()
        epidemie(ISTANBUL)
        self.assertEqual([3, 1, 0], ISTANBUL.phase)
        self.assertEqual([0, 4, 0], KAIRO.phase)

    def test_epidemie_2te(self):
        init_standard_setting()
        epidemie(ISTANBUL)
        epidemie(LAGOS)
        self.assertEqual([3, 1, 0, 0], ISTANBUL.phase)
        self.assertEqual([0, 3, 1, 0], LAGOS.phase)

    def test_add_city_nach_epidemie(self):
        init_standard_setting()
        epidemie(ISTANBUL)
        add_city(ISTANBUL)
        self.assertEqual([3, 0, 1], ISTANBUL.phase)

    def test_next_2_infekts_1epi(self):
        init_standard_setting()
        epidemie(ISTANBUL)
        self.assertEqual(1, next_x_infects(2, ISTANBUL))
        self.assertEqual(3, next_x_infects(2, LAGOS))

    def test_next_2_infekts_2epi(self):
        init_complicated_setting()
        self.assertEqual(0, next_x_infects(2, ISTANBUL))
        self.assertEqual(1, next_x_infects(2, LAGOS))
        self.assertEqual(0, next_x_infects(2, NEW_YORK))

    def test_next_6_infekts_2epi(self):
        init_complicated_setting()
        self.assertEqual(1, next_x_infects(6, ISTANBUL))
        self.assertEqual(2, next_x_infects(6, LAGOS))
        self.assertEqual(4, next_x_infects(6, KAIRO))


if __name__ == '__main__':
    unittest.main()
