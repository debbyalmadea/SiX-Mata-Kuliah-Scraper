from datetime import datetime

from lib.soup import Soup
from lib.mata_kuliah import MataKuliah
from lib.kelas_mata_kuliah import KelasMataKuliah
from lib.jadwal_mata_kuliah import JadwalMataKuliah
import lib.prodi_parser as ProdiParser
import lib.output as Output
import lib.input as Input


def get_kelas_mata_kuliah_by_prodi(kode_prodi, tahun=2023, semester=1):
    soup = Soup(prodi=kode_prodi, tahun=tahun, semester=semester).soup
    mata_kuliah_list, dosen_list = __parse_soup__(
        soup, kode_prodi, tahun, semester)
    return mata_kuliah_list, dosen_list


def get_all_mata_kuliah(tahun=2023, semester=1):
    prodi_list = ProdiParser.get_all_kode_prodi(ProdiParser.read_prodi())
    mata_kuliah_list = []
    dosen_list = []
    for prodi in prodi_list:
        print('Scraping mata kuliah prodi', prodi)
        mata_kuliah_prodi_list, dosen_prodi_list = get_kelas_mata_kuliah_by_prodi(
            prodi, tahun, semester)
        dosen_list += dosen_prodi_list
        mata_kuliah_list += mata_kuliah_prodi_list
        print()

    __save_mata_kuliah__(mata_kuliah_list, f"mata_kuliah_{tahun}-{semester}")
    Output.save_json({'data': dosen_list}, f'dosen_{tahun}-{semester}')


def read_mata_kuliah(tahun=2023, semester=1):
    return Input.read_json(f'mata_kuliah_{tahun}-{semester}')['data']


def __is_mata_kuliah_exists__(kode_matkul, mata_kuliah_list):
    for matkul in mata_kuliah_list:
        if matkul.kode == kode_matkul:
            return True

    return False


def __is_jadwal_mata_kuliah_exists__(jadwal_mk, jadwal_list):
    for jadwal in jadwal_list:
        if jadwal.is_equal(jadwal_mk):
            return True

    return False


def __save_mata_kuliah__(mata_kuliah_list, name='mata_kuliah'):
    dict = {
        'data': []
    }

    for mk in mata_kuliah_list:
        dict['data'].append(mk.to_dict())

    Output.save_json(dict, name)


def __parse_soup__(soup, kode_prodi, tahun, semester):
    mata_kuliah_list = []
    all_dosen_list = []

    table = soup.find('table')

    if not table:
        return [], []

    table_data = table.find_all('tr')

    for row in table_data:
        kelas_mata_kuliah_list = []
        row_data = row.find_all('td')

        if (len(row_data) == 0):
            continue

        individual_row_data = [data.text.strip() for data in row_data][1:]
        kode = individual_row_data[0]
        print('Scrapping data kelas', kode)
        nama = individual_row_data[1]
        sks = int(individual_row_data[2])

        mata_kuliah = MataKuliah(kode, kode_prodi, nama, sks)

        no_kelas = int(individual_row_data[3])
        kuota = 0
        if individual_row_data[4].isnumeric():
            kuota = int(individual_row_data[4])

        list_dosen = [dosen.strip()
                      for dosen in individual_row_data[5].split('\n')]

        for dosen in list_dosen:
            if dosen not in all_dosen_list:
                all_dosen_list.append(dosen)

        keterangan_batasan = row_data[-2].find_all('p')
        kelas_mata_kuliah = KelasMataKuliah(
            no_kelas, kuota, list_dosen, tahun, semester)

        for item in keterangan_batasan:
            if "Batasan" in item.text:
                list_batasan = item.text
                if "Kampus" in item.text:
                    list_batasan = item.text.split("Kampus")
                    list_batasan[-1] = list_batasan[-1].replace(
                        '\n', '').strip()
                    list_batasan = 'Kampus '.join(list_batasan)

                list_batasan = [batasan.strip()
                                for batasan in list_batasan.split('\n')[2:]]
                kelas_mata_kuliah.list_batasan = list_batasan
            else:
                kelas_mata_kuliah.keterangan = item.text.strip().replace('  ', '').replace('\n', ' ')

        schedules = row_data[-1].find_all('li')
        list_jadwal = []

        for schedule in schedules:
            schedule = schedule.text.strip().split('/')
            if (len(schedule) < 3):
                break

            hari = schedule[0].strip()
            waktu = schedule[2].strip().replace(
                " ", "").replace("\n", "").split('-')
            waktu_mulai = datetime.strptime(waktu[0], '%H.%M').time()
            waktu_akhir = datetime.strptime(waktu[1], '%H.%M').time()
            ruangan = schedule[3].strip().replace(" ", "").replace("\n", " ")

            jadwal = JadwalMataKuliah(hari, waktu_mulai, waktu_akhir, ruangan)
            if not __is_jadwal_mata_kuliah_exists__(jadwal, list_jadwal):
                list_jadwal.append(jadwal)
            else:
                break

        kelas_mata_kuliah.list_jadwal = list_jadwal
        kelas_mata_kuliah_list.append(kelas_mata_kuliah)

        mata_kuliah.list_kelas = kelas_mata_kuliah_list
        if not __is_mata_kuliah_exists__(kode, mata_kuliah_list):
            mata_kuliah_list.append(mata_kuliah)

    return mata_kuliah_list, all_dosen_list
