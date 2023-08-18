from lib.extractor.mata_kuliah_extractor import MataKuliahExtractor
from lib.parser.parser import HTMLParser


class FakultasParser(HTMLParser):
    def __init__(self, tahun: int, semester: int) -> None:
        super().__init__("fakultas")

        self.extractor = MataKuliahExtractor()
        self.extractor.set_config(tahun=tahun, semester=semester)


    def parse(self) -> None:
        soup = self.extractor.get_soup()
        self.data = [option.text.strip() for option in soup.find('select', {'id': 'fakultas'}).find_all('option')][1:]
