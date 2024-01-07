from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from lib.config.sqlalchemy import Base


class ProgramStudi(Base):
    __tablename__ = 'program_studi'

    kode = Column('kode', String(3), primary_key=True, autoincrement=False)
    nama = Column('nama', String(50))
    fakultas_nama = Column('fakultas_nama', String(50),
                           ForeignKey('fakultas.nama'))
    fakultas = relationship(
        "Fakultas", back_populates="program_studi", uselist=False)
    mata_kuliah = relationship(
        "MataKuliah", back_populates="program_studi")

    def __init__(self, kode, nama, fakultas):
        self.kode = kode
        self.nama = nama
        self.fakultas = fakultas

    def __repr__(self):
        return "<ProgramStudi(kode='%s', nama='%s')>" % (self.kode, self.nama)
