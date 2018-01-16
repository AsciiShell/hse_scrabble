import unittest
from server import GameDictionary
from os import remove


class TestGameDictionary(unittest.TestCase):
    test_path = "test_dict"

    @classmethod
    def setUpClass(cls):
        with open(cls.test_path, "w", encoding="utf-8") as f:
            f.write("""биосфера
блюз
дворянство
домолачивание
заковывание
изъян
киноведение
колеровщик
координированность
митраизм
налавливание
неминуемость
одухотворенность
окраина
плавсостав
поборник
подхват
приматывание
пролысина
сипловатость
солододробилка
топаз
трином
трехсотлетие
умывание
хранилище
централизация
шейх""")

    @classmethod
    def tearDownClass(cls):
        remove(cls.test_path)

    def test_dict(self):
        GameDictionary.filename = self.test_path
        a = GameDictionary()
        self.assertTrue(len(a.prepare("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")) == 28)


if __name__ == '__main__':
    unittest.main()
