from lib.extractor.jadwal_kuliah_extractor import JadwalKuliahExtractor
from lib.parser.parser import HTMLParser
from lib.parser.fakultas_parser import FakultasParser


class ProdiParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__("program_studi")

        self.extractor = JadwalKuliahExtractor()


    def get_config(self) -> dict:
        return self.extractor.get_config()
    

    def set_config(self, tahun: int = None, semester: int = None) -> None:
        if tahun != None:
            self.extractor.set_config(tahun=tahun)
        
        if semester != None:
            self.extractor.set_config(semester=semester)


    def parse(self) -> None:
        fakultas_parser = FakultasParser()

        fakultas_parser.set_config(tahun=2023, semester=1)
        list_fakultas = fakultas_parser.get()

        self.data = []
        for fakultas in list_fakultas:
            print(f"Scraping Program Studi Fakultas {fakultas}")

            self.extractor.set_config(fakultas=fakultas)
            soup = self.extractor.get_soup()

            list_prodi = [data.text.strip() for data in soup.find(
                'select', {'id': 'prodi'}).find_all('option')][1:]

            for prodi in list_prodi:
                self.data += [{
                    'kode': prodi.split('-')[0].strip(),
                    'nama': prodi.split('-')[1].strip(),
                    'fakultas': fakultas
                }]
