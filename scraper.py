import lib.prodi_parser as ProdiParser
import lib.mata_kuliah_parser as MKParser
import db


def main():
    ProdiParser.get_all_prodi()
    MKParser.get_all_mata_kuliah(2023, 1)
    MKParser.get_all_mata_kuliah(2022, 2)
    db.save_fakultas_prodi()
    db.save_mata_kuliah_dosen(2023, 1)
    db.save_mata_kuliah_dosen(2022, 2)


if __name__ == "__main__":
    main()
