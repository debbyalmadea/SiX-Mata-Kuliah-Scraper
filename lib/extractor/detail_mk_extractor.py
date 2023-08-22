import config
import requests


from lib.extractor.extractor import HTMLExtractor


class DetailMataKuliahExtractor(HTMLExtractor):
    def __init__(self) -> None:
        self.id = None
        self.soup = None

    
    def get_config(self) -> dict:
        return {
            'id': self.id
        }
    

    def set_config(self, id: int = None) -> None:
        if id != None:
            self.id = id
    

    def get_response(self) -> requests.models.Response:
        BASE_URL = f'https://akademik.itb.ac.id/app/mahasiswa:{config.NIM}/kurikulum/silabus/{self.id}/view'

        response = requests.get(
            BASE_URL,
            cookies=config.COOKIES,
            headers=config.HEADERS,
        )

        return response