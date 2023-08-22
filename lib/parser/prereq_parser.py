from lib.extractor.detail_mk_extractor import DetailMataKuliahExtractor
from lib.parser.parser import HTMLParser
from lib.parser.mata_kuliah_parser import MataKuliahParser


class PrereqParser(HTMLParser):
    def __init__(self, id) -> None:
        super().__init__(f"prereq-{id}")

        self.extractor = DetailMataKuliahExtractor()
        self.extractor.set_config(id=id)


    def get_config(self) -> dict:
        return self.extractor.get_config()
    

    def set_config(self, id: int = None) -> None:
        self.extractor.set_config(id=id)


    def parse(self) -> None:
        soup = self.extractor.get_soup()

        prereq_data = soup.find_all('tr')[7].text.replace("  ", "").split('\n')[1:]

        self.data = []
        for i in range(0, len(prereq_data), 2):
            kode = prereq_data[i].split(' ')[0]
            matkul = self.__find_matkul_by_kode(kode)

            if matkul:
                self.data += [matkul]
    

    def __find_matkul_by_kode(self, kode: str) -> dict:
        data = MataKuliahParser().get()

        for matkul in data:
            if matkul['kode'] == kode:
                return matkul
