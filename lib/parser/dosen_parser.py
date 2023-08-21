from lib.extractor.jadwal_kuliah_extractor import JadwalKuliahExtractor
from lib.parser.parser import HTMLParser
from lib.parser.jadwal_kuliah_parser import JadwalKuliahParser


class DosenParser(HTMLParser):
    def __init__(self, tahun: int, semester: int) -> None:
        super().__init__(f"dosen_{tahun}-{semester}")

        self.tahun = tahun
        self.semester = semester

        self.extractor = JadwalKuliahExtractor()
        self.extractor.set_config(tahun=tahun, semester=semester)

    def parse(self) -> None:
        list_jadwal_mk = JadwalKuliahParser(
            tahun=self.tahun, semester=self.semester).save()

        self.data = []
        for jadwal_mk in list_jadwal_mk:
            for kelas_mk in jadwal_mk['list_kelas']:
                for dosen in kelas_mk['list_dosen']:
                    if dosen not in self.data:
                        self.data += [dosen]
