from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class HTMLExtractor:
    @abstractmethod
    def getResponse(self):
        pass


    def getSoup(self, sendRequest: bool = True) -> BeautifulSoup:
        if sendRequest or self.soup == None:
            response = self.getResponse()
            self.soup = BeautifulSoup(response.text, 'html.parser')
        
        return self.soup
