import lib.fakultas_parser as FakultasParser
import lib.prodi_parser as ProdiParser
import lib.mata_kuliah_parser as MKParser
import lib.input as Input


def main():
    MKParser.get_all_mata_kuliah(2022, 2)


if __name__ == "__main__":
    main()
