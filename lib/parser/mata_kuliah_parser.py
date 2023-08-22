from lib.extractor.kurikulum_extractor import KurikulumExtractor
from lib.parser.parser import HTMLParser
from lib.parser.prodi_parser import ProdiParser


class MataKuliahParser(HTMLParser):
    def __init__(self):
        super().__init__("mata_kuliah")

        self.extractor = KurikulumExtractor()
    

    def get_config(self):
        return self.extractor.get_config()
    

    def set_config(self, tahun: int = None):
        self.extractor.set_config(tahun=tahun)

    
    def parse(self):
        list_prodi = ProdiParser().get()

        self.data = []
        for prodi in list_prodi:
            self.extractor.set_config(fakultas=prodi['fakultas'], prodi=prodi['kode'])
            soup = self.extractor.get_soup()
            
            table_data = soup.find('div', {'id': 'katalog'}).find_all('tr')[1:]

            if table_data == []:
                tahun_options = [option.text.strip() for option in soup.find(
            'select', {'id': 'th_kur'}).find_all('option')]
                
                idx = 0
                while idx < len(tahun_options) and int(tahun_options[idx]) < self.extractor.get_config()['tahun']:
                    idx += 1

                while table_data == [] and idx < len(tahun_options):
                    self.extractor.set_config(tahun=int(tahun_options[idx]))
                    soup = self.extractor.get_soup()
                    table_data = soup.find('div', {'id': 'katalog'}).find_all('tr')[1:]
                    idx += 1

            if table_data == []:
                continue            
            
            print(f"Scraping Mata Kuliah Program Studi: {prodi['nama']}, Tahun: {self.extractor.get_config()['tahun']}")
            for i in range(len(table_data)):
                row_data = table_data[i].find_all('td')
                self.__parse_row_data(row_data, prodi)
                
                
    def __parse_row_data(self, row_data, prodi):
        id = int(row_data[0].find('a')['href'].split('/')[-2])
        kode = row_data[0].text.strip()
        nama = row_data[1].text.strip()
        sks = row_data[2].text.strip()


        self.data += [{
            'id': id,
            'kode': kode,
            'nama': nama,
            'prodi': prodi['kode'],
            'sks': sks
        }]
