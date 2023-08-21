from lib.extractor.jadwal_kuliah_extractor import JadwalKuliahExtractor
from lib.parser.parser import HTMLParser


class FakultasParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__("fakultas")

        self.extractor = JadwalKuliahExtractor()

    
    def get_config(self) -> dict:
        return self.extractor.get_config()


    def set_config(self, tahun: int = None, semester: int = None) -> None:
        if tahun != None:
            self.extractor.set_config(tahun=tahun)

        if semester != None:
            self.extractor.set_config(semester=semester)


    def parse(self) -> None:
        soup = self.extractor.get_soup()
        self.data = [option.text.strip() for option in soup.find(
            'select', {'id': 'fakultas'}).find_all('option')][1:]
