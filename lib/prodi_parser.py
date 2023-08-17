from lib.soup import Soup
import lib.output as Output
import lib.input as Input
import lib.fakultas_parser as FakultasParser


def get_prodi_by_fakultas(fakultas):
    soup = Soup(fakultas=fakultas).soup

    return __parse_soup__(soup, fakultas)


def get_kode_prodi_by_fakultas(prodi_arr):
    kode_prodi = []
    for prodi in prodi_arr:
        kode_prodi.append(prodi['kode'])

    return kode_prodi


def get_all_prodi():
    all_prodi_dict = {}
    all_prodi_dict['data'] = []

    fakultas = FakultasParser.get_fakultas()

    for item in fakultas:
        print('Scrapping Program Studi', item)
        all_prodi_dict['data'].append(get_prodi_by_fakultas(item))

    Output.save_json(all_prodi_dict, 'program_studi')
    return all_prodi_dict


def get_all_kode_prodi(all_prodi_arr):
    kode_prodi = []
    for prodi_fakultas in all_prodi_arr:
        kode_prodi += get_kode_prodi_by_fakultas(
            prodi_fakultas['program_studi'])

    return kode_prodi


def read_prodi():
    prodi = Input.read_json('program_studi')['data']

    return prodi


def __parse_soup__(soup, fakultas):
    prodi_dict = {'fakultas': fakultas}

    prodi_select = soup.find('select', {'id': 'prodi'})

    prodi_options = prodi_select.find_all('option')
    prodi_list = [data.text.strip() for data in prodi_options]
    prodi_dict['program_studi'] = []

    for prodi in prodi_list:
        if prodi == '':
            continue
        dict = {
            'kode': prodi.split('-')[0].strip(),
            'nama': prodi.split('-')[1].strip()
        }

        prodi_dict['program_studi'].append(dict)

    return prodi_dict
