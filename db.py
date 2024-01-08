from lib.model.fakultas import Fakultas
from lib.model.program_studi import ProgramStudi
from lib.model.dosen import Dosen
from lib.model.mata_kuliah import MataKuliah
from lib.model.kelas_mata_kuliah import KelasMataKuliah
from lib.model.jadwal_kelas import JadwalKelas
from lib.model.batasan_kelas import BatasanKelas

from lib.parser.fakultas_parser import FakultasParser
from lib.parser.prodi_parser import ProdiParser
from lib.parser.dosen_parser import DosenParser
from lib.parser.mata_kuliah_parser import MataKuliahParser
from lib.parser.jadwal_kuliah_parser import JadwalKuliahParser

from lib.config.sqlalchemy import Session, engine, Base

from datetime import datetime


def save_jadwal_kuliah(tahun: int, semester: int, session: Session):
    jadwal_kuliah_parser = JadwalKuliahParser(tahun, semester)
    jadwal_kuliah_list = jadwal_kuliah_parser.read()

    for jadwal_kuliah in jadwal_kuliah_list:
        mata_kuliah = session.query(MataKuliah).filter_by(
            kode=jadwal_kuliah['kode']).all()
        kode_prodi = jadwal_kuliah['kode_prodi']
        print(mata_kuliah)
        if len(mata_kuliah) > 0:
            mata_kuliah = mata_kuliah[0]

            for kelas in jadwal_kuliah['list_kelas']:
                # kelas mata kuliah
                kelas_mata_kuliah_obj = KelasMataKuliah(
                    kelas['no_kelas'], kelas['kuota'], kelas['keterangan'], kelas['tahun'], kelas['semester'], mata_kuliah, kode_prodi)

                # jadwal kelas
                for jadwal in kelas['list_jadwal']:
                    jadwal_kelas_obj = JadwalKelas(
                        kelas_mata_kuliah_obj, jadwal['hari'], datetime.strptime(
                            jadwal['waktu_awal'], '%H.%M').time(), datetime.strptime(
                            jadwal['waktu_akhir'], '%H.%M').time(), jadwal['ruangan'])
                    kelas_mata_kuliah_obj.jadwal_kelas.append(jadwal_kelas_obj)
                    session.add(jadwal_kelas_obj)

                # dosen kelas
                for dosen in kelas['list_dosen']:
                    dosen_obj = session.query(Dosen).filter_by(
                        nama=dosen).first()
                    if dosen_obj is None:
                        dosen_obj = Dosen(dosen)
                        session.add(dosen_obj)
                    kelas_mata_kuliah_obj.dosen_kelas.append(dosen_obj)

                # batasan kelas
                if kelas.get('batasan') is not None:
                    for batasan in kelas['batasan']:
                        batasan_kelas_obj = BatasanKelas(
                            kelas_mata_kuliah_obj, batasan)
                        kelas_mata_kuliah_obj.batasan_kelas.append(
                            batasan_kelas_obj)
                        session.add(batasan_kelas_obj)

                print(kelas_mata_kuliah_obj)
                session.add(kelas_mata_kuliah_obj)
        else:
            print('Mata kuliah tidak ditemukan')


def save():
    Base.metadata.create_all(engine)

    session = Session()

    # fakultas
    fakultas_parser = FakultasParser()
    fakultas_list = fakultas_parser.read()

    for fakultas in fakultas_list:
        fakultas_obj = Fakultas(fakultas)
        print(fakultas_obj)
        session.add(fakultas_obj)

    # program studi
    prodi_parser = ProdiParser()
    prodi_list = prodi_parser.read()

    for prodi in prodi_list:
        fakultas = session.query(Fakultas).filter_by(
            nama=prodi['fakultas']).first()
        prodi_obj = ProgramStudi(prodi['kode'], prodi['nama'], fakultas)
        print(prodi_obj)
        session.add(prodi_obj)

    # dosen
    dosen_parser_2023_1 = DosenParser(2023, 1)
    dosen_list_2023_1 = dosen_parser_2023_1.read()
    for dosen in dosen_list_2023_1:
        dosen_obj = Dosen(dosen)
        print(dosen_obj)
    session.add(dosen_obj)

    dosen_parser_2022_2 = DosenParser(2022, 2)
    dosen_list_2022_2 = dosen_parser_2022_2.read()
    for dosen in dosen_list_2022_2:
        if dosen not in dosen_list_2023_1:
            dosen_obj = Dosen(dosen)
            print(dosen_obj)
    session.add(dosen_obj)

    # mata kuliah
    mata_kuliah_parser = MataKuliahParser()
    mata_kuliah_list = mata_kuliah_parser.read()
    for mata_kuliah in mata_kuliah_list:
        prodi = session.query(ProgramStudi).filter_by(
            kode=mata_kuliah['prodi']).first()
        parts = mata_kuliah['sks'].split()
        sks = int(parts[0])
        sks_praktikum = 0 if len(parts) == 1 else float(
            parts[1][1:-1].split(',')[0])
        mata_kuliah_obj = MataKuliah(
            mata_kuliah['kode'], mata_kuliah['id'], mata_kuliah['nama'], sks, sks_praktikum, prodi)
        print(mata_kuliah_obj)
        session.add(mata_kuliah_obj)

    # jadwal kuliah
    save_jadwal_kuliah(2023, 1, session)
    save_jadwal_kuliah(2022, 2, session)

    session.commit()
    session.close()
