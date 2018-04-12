import unittest
import os
from time import sleep
from server_old import *


class TestGameServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(os.path.abspath(os.curdir))
        os.chdir("..")
        print(os.path.abspath(os.curdir))

    def test_1(self):
        GameConfig.startCount = 3
        test_game = GameServer([Player("BOT1", "bot")])
        test_game.matrix.Mainmap[7][7] = "П"
        test_game.matrix.Mainmap[7][8] = "Р"
        test_game.matrix.Mainmap[7][9] = "И"
        test_game.matrix.Mainmap[7][10] = "В"
        test_game.matrix.Mainmap[7][11] = "Е"
        test_time = 30
        while test_time > 0:
            self.assertTrue(test_game.playStatus)
            sleep(1)
            test_time -= 1
        for i in test_game.players:
            self.assertTrue(i.score > 0)
        del test_game


if __name__ == '__main__':
    unittest.main()
