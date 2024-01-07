from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from lib.config.sqlalchemy import Base
import re


class MataKuliah(Base):
    __tablename__ = 'mata_kuliah'

    kode = Column('kode', String(6), primary_key=True)
    id = Column('id', Integer)
    nama = Column('nama', String(255))
    sks = Column('sks', Integer)
    sks_praktikum = Column('sks_praktikum', Float)
    program_studi_kode = Column('program_studi_kode', String(3),
                                ForeignKey('program_studi.kode'))
    program_studi = relationship(
        "ProgramStudi", back_populates="mata_kuliah", uselist=False)
    kelas_mata_kuliah = relationship(
        "KelasMataKuliah", back_populates="mata_kuliah")

    def __init__(self, kode, id, nama, sks, sks_praktikum, program_studi):
        self.kode = kode
        self.id = id
        self.nama = nama
        self.sks = sks
        self.sks_praktikum = sks_praktikum
        self.program_studi = program_studi

    def __repr__(self):
        return "<MataKuliah(kode='%s', id='%s', nama='%s', sks='%s')>" % (self.kode, self.id, self.nama, self.sks)
