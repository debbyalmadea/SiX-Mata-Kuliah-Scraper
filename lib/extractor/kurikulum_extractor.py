import config
import requests


from lib.extractor.extractor import HTMLExtractor


class KurikulumExtractor(HTMLExtractor):
    def __init__(self) -> None:
        self.fakultas = None
        self.prodi = None
        self.tahun = None
        self.soup = None

    
    def get_config(self) -> dict:
        return {
            'fakultas': self.fakultas,
            'prodi': self.prodi,
            'tahun': self.tahun
        }
    

    def set_config(self, fakultas: str = None, prodi: int = None, tahun: int = None) -> None:
        if fakultas != None:
            self.fakultas = fakultas
        
        if prodi != None:
            self.prodi = prodi

        if tahun != None:
            self.tahun = tahun

    
    def get_response(self) -> requests.models.Response:
        BASE_URL = f'https://akademik.itb.ac.id/app/mahasiswa:{config.NIM}/kurikulum/struktur?fakultas={self.fakultas}&prodi={self.prodi}&th_kur={self.tahun}'

        response = requests.get(
            BASE_URL,
            cookies=config.COOKIES,
            headers=config.HEADERS,
        )

        return response
