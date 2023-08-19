import config
import requests


from lib.extractor.extractor import HTMLExtractor


class JadwalKuliahExtractor(HTMLExtractor):
    def __init__(self) -> None:
        self.tahun = None
        self.semester = None
        self.fakultas = None
        self.prodi = None
        self.soup = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(JadwalKuliahExtractor, cls).__new__(cls)
        return cls.instance

    def set_config(self, tahun: int = None, semester: int = None, fakultas: str = None, prodi: str = None) -> None:
        if tahun != None:
            self.tahun = tahun

        if semester != None:
            self.semester = semester

        if fakultas != None:
            self.fakultas = fakultas

        if prodi != None:
            self.prodi = prodi

    def get_config(self) -> dict:
        return {
            'tahun': self.tahun,
            'semester': self.semester,
            'fakultas': self.fakultas,
            'prodi': self.prodi
        }

    def get_response(self) -> requests.models.Response:
        if config.NIM == None:
            raise Exception('NIM belum di set')

        if self.tahun == None:
            raise Exception('Tahun belum di set')

        if self.semester == None:
            raise Exception('Semester belum di set')

        BASE_URL = f'https://akademik.itb.ac.id/app/K/mahasiswa:{config.NIM}+{self.tahun}-{self.semester}/kelas/jadwal/kuliah?fakultas={self.fakultas}&prodi={self.prodi}'

        response = requests.get(
            BASE_URL,
            cookies=config.COOKIES,
            headers=config.HEADERS,
        )

        return response
