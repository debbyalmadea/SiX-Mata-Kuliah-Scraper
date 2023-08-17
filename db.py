
import mysql.connector
from datetime import datetime

import lib.fakultas_parser as FakultasParser
import lib.prodi_parser as ProdiParser
import lib.mata_kuliah_parser as MKParser
import lib.input as Input
from config import DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD

database_name = DATABASE_NAME
host = DATABASE_HOST
user = DATABASE_USER
password = DATABASE_PASSWORD


def __create_db__(cursor, connection):
    print('Creating database...')
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    connection.database = database_name


def __save_fakultas_json__(cursor):
    print("Creating table fakultas...")
    create_table_query = "CREATE TABLE IF NOT EXISTS fakultas (nama VARCHAR(20), PRIMARY KEY (nama))"
    cursor.execute(create_table_query)
    fakultas_list = FakultasParser.read_fakultas()
    for fakultas in fakultas_list:
        insert_query = "INSERT INTO fakultas (nama) VALUES (%s)"
        cursor.execute(insert_query, (fakultas,))

    print("Table fakultas creation and data insertion successful.")


def __save_prodi_json__(cursor):
    print("Creating table program_studi...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS program_studi (
                                kode CHAR(3),
                                nama VARCHAR(255),
                                fakultas VARCHAR(20), 
                                PRIMARY KEY (kode),
                                FOREIGN KEY (fakultas) REFERENCES fakultas(nama)
                            )'''
    cursor.execute(create_table_query)
    fakultas_prodi_list = ProdiParser.read_prodi()
    insert_query = "INSERT INTO program_studi (kode, nama, fakultas) VALUES (%s, %s, %s)"
    for fakultas_prodi in fakultas_prodi_list:
        fakultas = fakultas_prodi['fakultas']
        prodi_list = fakultas_prodi['program_studi']
        for prodi in prodi_list:
            cursor.execute(
                insert_query, (prodi['kode'], prodi['nama'], fakultas))

    print("Table program_studi creation and data insertion successful.")


def __save_mata_kuliah_json__(cursor, tahun=2023, semester=1):
    print("Creating table dosen...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS dosen (
                                id INT AUTO_INCREMENT,
                                nama VARCHAR(255),
                                PRIMARY KEY (id),
                                UNIQUE(nama)
                            )'''
    cursor.execute(create_table_query)

    print("Creating table mata_kuliah...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS mata_kuliah (
                                id INT,
                                kode CHAR(6),
                                kode_prodi CHAR(3),
                                nama VARCHAR(255),
                                sks INT,
                                PRIMARY KEY (id),
                                FOREIGN KEY (kode_prodi) REFERENCES program_studi(kode),
                                UNIQUE(kode, kode_prodi)
                            )'''
    cursor.execute(create_table_query)

    print("Creating table kelas_mata_kuliah...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS kelas_mata_kuliah (
                                id INT,
                                id_matkul INT,
                                no_kelas INT,
                                tahun INT,
                                semester INT,
                                keterangan VARCHAR(500),
                                PRIMARY KEY (id),
                                FOREIGN KEY (id_matkul) REFERENCES mata_kuliah(id),
                                UNIQUE(id_matkul, no_kelas, tahun, semester)
                            )'''
    cursor.execute(create_table_query)

    print("Creating table batasan_kelas...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS batasan_kelas (
                                id_kelas INT,
                                batasan VARCHAR(255),
                                PRIMARY KEY (id_kelas, batasan),
                                FOREIGN KEY (id_kelas) REFERENCES kelas_mata_kuliah(id)
                            )'''
    cursor.execute(create_table_query)

    print("Creating table dosen_kelas...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS dosen_kelas (
                                id_kelas INT,
                                id_dosen INT,
                                PRIMARY KEY (id_kelas, id_dosen),
                                FOREIGN KEY (id_kelas) REFERENCES kelas_mata_kuliah(id)
                            )'''
    cursor.execute(create_table_query)

    print("Creating table jadwal_kelas...")
    create_table_query = '''CREATE TABLE IF NOT EXISTS jadwal_kelas (
                                id_kelas INT,
                                hari VARCHAR(20),
                                waktu_awal TIME,
                                waktu_akhir TIME,
                                ruangan VARCHAR(255),
                                PRIMARY KEY (id_kelas, hari, waktu_awal, waktu_akhir),
                                FOREIGN KEY (id_kelas) REFERENCES kelas_mata_kuliah(id)
                            )'''
    cursor.execute(create_table_query)

    mk_insert_query = "INSERT INTO mata_kuliah (id, kode, kode_prodi, nama, sks) VALUES (%s, %s, %s, %s, %s)"
    kelas_mk_insert_query = "INSERT INTO kelas_mata_kuliah (id, id_matkul, no_kelas, tahun, semester, keterangan) VALUES (%s, %s, %s, %s, %s, %s)"
    dosen_kelas_insert_query = "INSERT INTO dosen_kelas (id_kelas, id_dosen) VALUES (%s, %s)"
    batasan_kelas_insert_query = "INSERT INTO batasan_kelas (id_kelas, batasan) VALUES (%s, %s)"

    dosen_insert_query = "INSERT INTO dosen (nama) VALUES (%s)"

    all_dosen_list = Input.read_json(f'dosen_{tahun}-{semester}')['data']
    for dosen in all_dosen_list:
        try:
            cursor.execute(dosen_insert_query, (dosen,))
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
    print("Table dosen creation and data insertion successful.")

    mata_kuliah_list = MKParser.read_mata_kuliah(tahun, semester)

    count_kelas_mk_row_query = "SELECT COUNT(*) FROM kelas_mata_kuliah"
    cursor.execute(count_kelas_mk_row_query)
    kelas_count = cursor.fetchone()[0]

    count_mk_query = "SELECT COUNT(*) FROM mata_kuliah"
    cursor.execute(count_mk_query)
    matkul_count = cursor.fetchone()[0]

    for mk in mata_kuliah_list:
        kode = mk['kode']
        kode_prodi = mk['kode_prodi']
        nama = mk['nama']
        sks = int(mk['sks'])
        print(kode)

        id_matkul_search_query = "SELECT id FROM mata_kuliah WHERE kode = %s and kode_prodi = %s"
        cursor.execute(id_matkul_search_query, (kode, kode_prodi))
        id_matkul = cursor.fetchone()

        if not id_matkul:
            matkul_count += 1
            id_matkul = matkul_count
        else:
            id_matkul = id_matkul[0]

        try:
            cursor.execute(
                mk_insert_query, (id_matkul, kode, kode_prodi, nama, sks,))
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))

        list_kelas = mk['list_kelas']
        for kelas in list_kelas:
            kelas_count += 1
            no_kelas = int(kelas['no_kelas'])
            keterangan = kelas['keterangan']
            cursor.execute(
                kelas_mk_insert_query, (kelas_count, id_matkul,
                                        no_kelas, tahun, semester, keterangan)
            )

            list_batasan = kelas['list_batasan']
            for batasan in list_batasan:
                cursor.execute(
                    batasan_kelas_insert_query, (kelas_count, batasan)
                )

            list_dosen = kelas['list_dosen']
            for dosen in list_dosen:
                id_dosen_search_query = "SELECT id FROM dosen WHERE nama = %s"
                cursor.execute(id_dosen_search_query, (dosen,))
                id_dosen = cursor.fetchone()[0]
                cursor.execute(dosen_kelas_insert_query,
                               (kelas_count, id_dosen))

            list_jadwal = kelas['list_jadwal']
            for jadwal in list_jadwal:
                hari = jadwal['hari']
                waktu_awal = datetime.strptime(
                    jadwal['waktu_awal'], '%H.%M').time()
                waktu_akhir = datetime.strptime(
                    jadwal['waktu_akhir'], '%H.%M').time()
                ruangan = jadwal['ruangan']

                jadwal_kelas_insert_query = "INSERT INTO jadwal_kelas (id_kelas, hari, waktu_awal, waktu_akhir, ruangan) VALUES (%s, %s, %s, %s, %s)"

                try:
                    cursor.execute(jadwal_kelas_insert_query, (
                        kelas_count, hari, waktu_awal, waktu_akhir, ruangan
                    ))
                except mysql.connector.IntegrityError as err:
                    print("Error: {}".format(err))
    print("Table program_studi creation and data insertion successful.")


def save_fakultas_prodi():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
    )

    cursor = connection.cursor()

    __create_db__(cursor, connection)
    __save_fakultas_json__(cursor)
    __save_prodi_json__(cursor)

    connection.commit()
    connection.close()

    print("Database creation and data insertion successful.")
    print()


def save_mata_kuliah_dosen(tahun=2023, semester=1):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )

        cursor = connection.cursor(buffered=True)

        __save_mata_kuliah_json__(cursor, tahun, semester)

        connection.commit()
        connection.close()

        print("Database creation and data insertion successful.")
        print()
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err))
