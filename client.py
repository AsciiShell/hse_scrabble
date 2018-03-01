import time
from threading import Thread

from scrabblelib import *


class GameClientPrepare:
    """Класс подключения клиента к игре"""

    def _listener_daemon(self):
        """Асинхронный метод для ожидания информации"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 8384))
        while self.prepare:
            data, address = sock.recvfrom(1024)
            data = convert_type(data)
            for i in self.servers:
                if i["id"] == data["id"]:
                    i["queue"] = data["queue"]
                    i["game"] = data["game"]
                    self.callback()
                    break
            else:
                self.servers.append(data)
                self.servers[-1]["ip"] = address[0]
                self.callback()
            print(data)
        sock.close()

    def _fetch_daemon(self):
        while self.prepare:
            send_broadcast({'action': 'getStatus'}, 8383)
            time.sleep(1)

    def connect_server(self, rid):
        for i in self.servers:
            if i["id"] == rid:
                send_broadcast({'action': 'connectGame', 'rid': self.client_id, 'name': rand(2) + '_BOSS'}, 8383,
                               i["ip"])
                return Message(True)
        return Message(False, "Сервер не найден")

    def __init__(self):
        self.prepare = True
        self.servers = []
        self.client_id = rand(8)
        self.callback = lambda *args: None
        self.listenThread = Thread(target=self._listener_daemon)
        self.listenThread.start()
        self.fetchThread = Thread(target=self._fetch_daemon)
        self.fetchThread.start()
