from sqlalchemy import Column, String, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship
from lib.config.sqlalchemy import Base


class JadwalKelas(Base):
    __tablename__ = 'jadwal_kelas'

    kelas_id = Column('kelas_id', Integer, ForeignKey(
        'kelas_mata_kuliah.id'), primary_key=True)
    hari = Column('hari', String(10), primary_key=True)
    waktu_awal = Column('waktu_awal', Time, primary_key=True)
    waktu_akhir = Column('waktu_akhir', Time, primary_key=True)
    ruangan = Column('ruangan', String(100))

    kelas_mata_kuliah = relationship(
        "KelasMataKuliah", back_populates="jadwal_kelas", uselist=False)

    def __init__(self, kelas_mata_kuliah, hari, waktu_awal, waktu_akhir, ruangan):
        self.kelas_mata_kuliah = kelas_mata_kuliah
        self.hari = hari
        self.waktu_awal = waktu_awal
        self.waktu_akhir = waktu_akhir
        self.ruangan = ruangan

    def __repr__(self):
        return "<JadwalKelas(kelas_mata_kuliah='%s', hari='%s', waktu_awal='%s', waktu_akhir='%s', ruangan='%s')>" % (
            self.kelas_mata_kuliah, self.hari, self.waktu_awal, self.waktu_akhir, self.ruangan)
