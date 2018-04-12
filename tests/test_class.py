import unittest
from os import remove

from server_old import *


class TestGameDictionary(unittest.TestCase):
    test_path = "test_dict"
    test_dict = ['биосфера', 'блюз', 'дворянство', 'домолачивание', 'заковывание', 'изъян', 'киноведение', 'колеровщик',
                 'координированность', 'митраизм', 'налавливание', 'неминуемость', 'одухотворенность', 'окраина',
                 'плавсостав', 'поборник', 'подхват', 'приматывание', 'пролысина', 'сипловатость', 'солододробилка',
                 'топаз', 'трином', 'трехсотлетие', 'умывание', 'хранилище', 'централизация', 'шейх']

    @classmethod
    def setUpClass(cls):
        with open(cls.test_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(cls.test_dict))
        GameDictionary.filename = cls.test_path
        cls.g_dict = GameDictionary()

    @classmethod
    def tearDownClass(cls):
        remove(cls.test_path)

    def test_1(self):
        self.assertTrue(len(self.g_dict.prepare("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")) == len(self.test_dict))

    def test_2(self):
        self.assertTrue(len(self.g_dict.prepare("А")) == 0)

    def test_3(self):
        self.assertTrue(len(self.g_dict.prepare("БЛЮЗ")) == 1)

    def test_4(self):
        self.assertTrue(len(self.g_dict.prepare("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮ")) == len(self.test_dict) - 3)

    def test_star_1(self):
        self.assertTrue(len(self.g_dict.prepare("ИЗ*ЯН")) == 1)

    def test_star_2(self):
        self.assertTrue(len(self.g_dict.prepare("*****")) == 4)


class TestPoint(unittest.TestCase):
    def test_1(self):
        self.assertTrue(Point(0, 0, 'Я').get_info() == Point.info[4])

    def test_2(self):
        self.assertTrue(Point(6, 8, 'Я').get_info() == Point.info[1])

    def test_3(self):
        self.assertTrue(Point(4, 4, 'Я').get_info() == Point.info[2])

    def test_4(self):
        self.assertTrue(Point(1, 5, 'Я').get_info() == Point.info[3])

    def test_5(self):
        self.assertTrue(Point(1, 2, 'Я').get_info() == Point.info[0])


if __name__ == '__main__':
    unittest.main()
