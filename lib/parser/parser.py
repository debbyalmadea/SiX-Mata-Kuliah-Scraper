from abc import ABC, abstractmethod


import lib.util.io_handler as IO


class HTMLParser(ABC):
    def __init__(self, filename) -> None:
        self.filename = filename
        self.data = None
        self.tahun = 2023
        self.semester = 1

    def get(self, force_extract: bool = False) -> list:
        if force_extract:
            self.parse()
        else:
            self.data = self.read()

            if self.data is None:
                self.parse()

        return self.data

    def read(self):
        json_object = IO.read_json(self.filename)

        if json_object is None:
            return None

        return json_object['data']

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        if self.data is None:
            self.parse()

        IO.save_json({"data": self.data}, name=filename)

    @abstractmethod
    def parse(self):
        pass
