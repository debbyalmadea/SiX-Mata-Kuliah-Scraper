import os
from dotenv import load_dotenv

load_dotenv()

COOKIES_KHONGGUAN = os.getenv('COOKIES_KHONGGUAN')
NIM = os.getenv('NIM')

COOKIES = {
    'khongguan': COOKIES_KHONGGUAN
}

HEADERS = {
    'authority': 'akademik.itb.ac.id',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
