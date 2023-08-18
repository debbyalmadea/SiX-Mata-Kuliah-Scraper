from abc import ABC, abstractmethod


import lib.util.io_handler as IO


class HTMLParser(ABC):
    def __init__(self, filename) -> None:
        self.filename = filename
        self.data = None


    def get(self) -> list:
        if self.data is None:
            self.parse()
        
        return self.data
    

    def read(self):
        return IO.read_json(self.filename)['data']


    def save(self):
        if self.data is None:
            self.parse()
        
        IO.save_json({"data": self.data}, name=self.filename)


    @abstractmethod
    def parse(self):
        pass
