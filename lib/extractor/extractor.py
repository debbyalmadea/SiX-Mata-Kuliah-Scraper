from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class HTMLExtractor(ABC):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HTMLExtractor, cls).__new__(cls)
        return cls.instance
    

    @abstractmethod
    def get_response(self):
        pass


    def get_soup(self, send_request: bool = True) -> BeautifulSoup:
        if send_request or self.soup == None:
            response = self.get_response()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        
        return self.soup
