from lib.extractor.mata_kuliah_extractor import MataKuliahExtractor
from lib.parser.parser import HTMLParser
from lib.parser.fakultas_parser import FakultasParser


class ProdiParser(HTMLParser):
    def __init__(self, tahun: int, semester: int) -> None:
        super().__init__("program_studi")

        self.tahun = tahun
        self.semester = semester

        self.extractor = MataKuliahExtractor()
        self.extractor.set_config(tahun=tahun, semester=semester)


    def parse(self) -> None:
        list_fakultas = FakultasParser(tahun=self.tahun, semester=self.semester).get()

        self.data = []
        for fakultas in list_fakultas:
            print(f"Scraping Program Studi Fakultas {fakultas}")

            self.extractor.set_config(fakultas=fakultas)
            soup = self.extractor.get_soup()

            list_prodi = [data.text.strip() for data in soup.find('select', {'id': 'prodi'}).find_all('option')][1:]
            
            for prodi in list_prodi:
                self.data += [{
                    'kode': prodi.split('-')[0].strip(),
                    'nama': prodi.split('-')[1].strip(),
                    'fakultas': fakultas
                }]
            
            break
        
        print(self.data)
