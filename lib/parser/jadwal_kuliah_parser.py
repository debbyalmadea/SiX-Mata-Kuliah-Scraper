from datetime import datetime

from lib.extractor.jadwal_kuliah_extractor import JadwalKuliahExtractor
from lib.parser.parser import HTMLParser
from lib.parser.prodi_parser import ProdiParser


class JadwalKuliahParser(HTMLParser):
    def __init__(self, tahun: int, semester: int) -> None:
        super().__init__(f"jadwal_mata_kuliah_{tahun}-{semester}")

        self.tahun = tahun
        self.semester = semester

        self.extractor = JadwalKuliahExtractor()

    def parse(self) -> None:
        list_prodi = ProdiParser().get()
        self.data = []

        for prodi in list_prodi:
            self.extractor.set_config(tahun=self.tahun, semester=self.semester,
                                      fakultas=prodi['fakultas'], prodi=prodi['kode'])

            print(self.extractor.get_config())
            soup = self.extractor.get_soup()
            table = soup.find('table')

            if not table:
                continue

            table_data = table.find_all('tr')

            kelas_mata_kuliah_list = []
            for row in table_data:
                row_data = row.find_all('td')

                if (len(row_data) == 0):
                    continue

                individual_row_data = [data.text.strip()
                                       for data in row_data][1:]
                kode = individual_row_data[0]
                print('Scrapping data kelas', kode)
                nama = individual_row_data[1]
                sks = int(individual_row_data[2])

                # mata_kuliah = MataKuliah(kode, prodi['kode'], nama, sks)
                mata_kuliah = {
                    "kode": kode,
                    "kode_prodi": prodi['kode'],
                    "nama": nama,
                    "sks": sks,
                }

                no_kelas = int(individual_row_data[3])
                kuota = 0
                if individual_row_data[4].isnumeric():
                    kuota = int(individual_row_data[4])

                list_dosen = [dosen.strip()
                              for dosen in individual_row_data[5].split('\n')]

                keterangan_batasan = row_data[-2].find_all('p')
                # kelas_mata_kuliah = KelasMataKuliah(
                #     no_kelas, kuota, list_dosen, self.tahun, self.semester)
                kelas_mata_kuliah = {
                    "no_kelas": no_kelas,
                    "kuota": kuota,
                    "tahun": self.tahun,
                    "semester": self.semester,
                    "keterangan": "",
                    "list_dosen": list_dosen,
                    "list_batasan": []
                }

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
                        kelas_mata_kuliah["list_batasan"] = list_batasan
                    else:
                        kelas_mata_kuliah["keterangan"] = item.text.strip().replace(
                            '  ', '').replace('\n', ' ')

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

                    # jadwal = JadwalKelas(
                    #     hari, waktu_mulai, waktu_akhir, ruangan)
                    jadwal = {
                        "hari": hari,
                        "waktu_awal": waktu_mulai.strftime("%H.%M"),
                        "waktu_akhir": waktu_akhir.strftime("%H.%M"),
                        "ruangan": ruangan
                    }

                    if not self.__is_jadwal_mata_kuliah_exists__(jadwal, list_jadwal):
                        list_jadwal.append(jadwal)
                    else:
                        break

                kelas_mata_kuliah["list_jadwal"] = list_jadwal
                kelas_mata_kuliah_list.append(kelas_mata_kuliah)

                if not self.__is_mata_kuliah_exists__(kode):
                    mata_kuliah["list_kelas"] = [kelas_mata_kuliah]
                    self.data.append(mata_kuliah)
                else:
                    self.data[-1]["list_kelas"].append(kelas_mata_kuliah)

    def __is_mata_kuliah_exists__(self, kode_matkul):
        for matkul in self.data:
            if matkul['kode'] == kode_matkul:
                return True

        return False

    def __is_jadwal_mata_kuliah_exists__(self, jadwal_mk, jadwal_list):
        for jadwal in jadwal_list:
            if (
                jadwal_mk["hari"] == jadwal["hari"] and
                jadwal_mk["waktu_awal"] == jadwal["waktu_awal"] and
                jadwal_mk["waktu_akhir"] == jadwal["waktu_akhir"]
            ):
                return True

        return False
