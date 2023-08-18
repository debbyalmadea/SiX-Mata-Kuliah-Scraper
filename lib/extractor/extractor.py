from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class HTMLExtractor(ABC):
    @abstractmethod
    def get_response(self):
        pass


    def get_soup(self, send_request: bool = True) -> BeautifulSoup:
        if send_request or self.soup == None:
            response = self.getResponse()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        
        return self.soup
