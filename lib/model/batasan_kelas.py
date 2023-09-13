from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from lib.config.sqlalchemy import Base


class BatasanKelas(Base):
    __tablename__ = 'batasan_kelas'

    kelas_id = Column('kelas_id', Integer, ForeignKey(
        'kelas_mata_kuliah.id'), primary_key=True)
    batasan_kelas = Column('batasan_kelas', String(100), primary_key=True)

    kelas_mata_kuliah = relationship(
        "KelasMataKuliah", back_populates="batasan_kelas", uselist=False)

    def __init__(self, kelas_mata_kuliah, batasan_kelas):
        self.kelas_mata_kuliah = kelas_mata_kuliah
        self.batasan_kelas = batasan_kelas

    def __repr__(self):
        return "<BatasanKelas(kelas_mata_kuliah='%s', batasan_kelas='%s')>" % (
            self.kelas_mata_kuliah, self.batasan_kelas)
