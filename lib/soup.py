import config
from bs4 import BeautifulSoup
import requests


class Soup:
    def __init__(self, fakultas='', prodi='', tahun=2023, semester=1) -> None:
        self.tahun = tahun
        self.semester = semester
        self.fakultas = fakultas
        self.prodi = prodi

        self.soup = BeautifulSoup(
            self.__get_response__().content, 'html.parser')

    def __get_response__(self):
        BASE_URL = f'https://akademik.itb.ac.id/app/K/mahasiswa:{config.NIM}+{self.tahun}-{self.semester}/kelas/jadwal/kuliah?fakultas={self.fakultas}&prodi={self.prodi}'
        response = requests.get(
            BASE_URL,
            cookies=config.COOKIES,
            headers=config.HEADERS,
        )

        return response
