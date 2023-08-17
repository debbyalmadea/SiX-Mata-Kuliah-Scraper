from lib.soup import Soup
import lib.output as output
import lib.input as Input


def get_fakultas():
    soup = Soup().soup

    fakultas = __parse_soup__(soup)
    __save_json__(fakultas)

    return fakultas


def read_fakultas():
    fakultas = Input.read_json('fakultas')['data']
    return fakultas


def __save_json__(fakultas):
    fakultas_dict = {
        "data": fakultas
    }

    output.save_json(fakultas_dict, 'fakultas')


def __parse_soup__(soup):
    fakultas_select = soup.find('select', {'id': 'fakultas'})
    fakultas = [data.text.strip()
                for data in fakultas_select.find_all('option')]

    return fakultas[1:]
