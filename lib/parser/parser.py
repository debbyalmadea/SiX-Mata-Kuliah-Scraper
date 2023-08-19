from abc import ABC, abstractmethod


import lib.util.io_handler as IO


class HTMLParser(ABC):
    def __init__(self, filename) -> None:
        self.filename = filename
        self.data = None

    def get(self) -> list:
        self.data = self.read()
        if self.data is None:
            self.parse()

        self.save()
        return self.data

    def read(self):
        json_object = IO.read_json(self.filename)
        if json_object is None:
            return None
        return json_object['data']

    def save(self):
        self.data = self.read()
        if self.data is None:
            self.parse()

        IO.save_json({"data": self.data}, name=self.filename)

    @abstractmethod
    def parse(self):
        pass
