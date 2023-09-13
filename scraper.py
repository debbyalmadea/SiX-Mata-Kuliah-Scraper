from lib.parser.fakultas_parser import FakultasParser
from lib.parser.prodi_parser import ProdiParser
from lib.parser.jadwal_kuliah_parser import JadwalKuliahParser
from lib.parser.dosen_parser import DosenParser

import db


def main():
    fakultas_parser = FakultasParser()
    fakultas_parser.save()

    prodi_parser = ProdiParser()
    prodi_parser.save()

    jadwal_kuliah_parser = JadwalKuliahParser(2023, 1)
    jadwal_kuliah_parser.save()
    jadwal_kuliah_parser.tahun = 2022
    jadwal_kuliah_parser.semester = 2
    jadwal_kuliah_parser.save()

    dosen_parser = DosenParser(2023, 1)
    dosen_parser.save()
    dosen_parser.tahun = 2022
    dosen_parser.semester = 2
    dosen_parser.save()

    db.save()


if __name__ == "__main__":
    main()
