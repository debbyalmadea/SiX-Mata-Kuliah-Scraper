from lib.parser.jadwal_kuliah_parser import JadwalKuliahParser

import db


def main():
    # MKParser.get_all_mata_kuliah(2023, 1)
    # MKParser.get_all_mata_kuliah(2022, 2)
    JadwalKuliahParser.save(2023, 1)
    JadwalKuliahParser.save(2022, 2)

    db.save_fakultas_prodi()
    db.save_mata_kuliah_dosen(2023, 1)
    db.save_mata_kuliah_dosen(2022, 2)


if __name__ == "__main__":
    main()
