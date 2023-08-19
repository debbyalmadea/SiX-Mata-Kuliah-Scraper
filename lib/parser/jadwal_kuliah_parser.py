from datetime import datetime

from lib.extractor.jadwal_kuliah_extractor import JadwalKuliahExtractor
from lib.parser.parser import HTMLParser
from lib.parser.prodi_parser import ProdiParser

from lib.model.mata_kuliah import MataKuliah
from lib.model.kelas_mata_kuliah import KelasMataKuliah
from lib.model.jadwal_kelas import JadwalKelas


class JadwalKuliahParser(HTMLParser):
    def __init__(self, tahun: int, semester: int) -> None:
        super().__init__(f"jadwal_mata_kuliah_{tahun}-{semester}")

        self.tahun = tahun
        self.semester = semester

        self.extractor = JadwalKuliahExtractor()
        self.extractor.set_config(tahun=tahun, semester=semester)

    def parse(self) -> None:
        list_prodi = ProdiParser(
            tahun=self.tahun, semester=self.semester).get()

        self.data = []

        for prodi in list_prodi:
            table = self.extractor.find('table')

            if not table:
                return [], []

            table_data = table.find_all('tr')

            for row in table_data:
                kelas_mata_kuliah_list = []
                row_data = row.find_all('td')

                if (len(row_data) == 0):
                    continue

                individual_row_data = [data.text.strip()
                                       for data in row_data][1:]
                kode = individual_row_data[0]
                print('Scrapping data kelas', kode)
                nama = individual_row_data[1]
                sks = int(individual_row_data[2])

                mata_kuliah = MataKuliah(kode, prodi['kode'], nama, sks)

                no_kelas = int(individual_row_data[3])
                kuota = 0
                if individual_row_data[4].isnumeric():
                    kuota = int(individual_row_data[4])

                list_dosen = [dosen.strip()
                              for dosen in individual_row_data[5].split('\n')]

                keterangan_batasan = row_data[-2].find_all('p')
                kelas_mata_kuliah = KelasMataKuliah(
                    no_kelas, kuota, list_dosen, self.tahun, self.semester)

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
                    ruangan = schedule[3].strip().replace(
                        " ", "").replace("\n", " ")

                    jadwal = JadwalKelas(
                        hari, waktu_mulai, waktu_akhir, ruangan)
                    if not self.__is_jadwal_mata_kuliah_exists__(jadwal, list_jadwal):
                        list_jadwal.append(jadwal)
                    else:
                        break

                kelas_mata_kuliah.list_jadwal = list_jadwal
                kelas_mata_kuliah_list.append(kelas_mata_kuliah)

                mata_kuliah.list_kelas = kelas_mata_kuliah_list
                if not self.__is_mata_kuliah_exists__(kode):
                    self.data.append(mata_kuliah.to_dict())

    def __is_mata_kuliah_exists__(self, kode_matkul):
        for matkul in self.data:
            if matkul['kode'] == kode_matkul:
                return True

        return False

    def __is_jadwal_mata_kuliah_exists__(self, jadwal_mk, jadwal_list):
        for jadwal in jadwal_list:
            if jadwal.is_equal(jadwal_mk):
                return True

        return False