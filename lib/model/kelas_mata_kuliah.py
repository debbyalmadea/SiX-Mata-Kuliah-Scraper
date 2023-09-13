from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from lib.config.sqlalchemy import Base

dosen_kelas_association = Table(
    'dosen_kelas', Base.metadata,
    Column('dosen_id', Integer, ForeignKey('dosen.id')),
    Column('kelas_id', Integer, ForeignKey('kelas_mata_kuliah.id'))
)


class KelasMataKuliah(Base):
    __tablename__ = 'kelas_mata_kuliah'

    id = Column('id', Integer, primary_key=True)
    no_kelas = Column('no_kelas', Integer)
    kuota = Column('kuota', Integer)
    keterangan = Column('keterangan', String(300), nullable=True)
    tahun = Column('tahun', Integer)
    semester = Column('semester', Integer)
    mata_kuliah_kode = Column('mata_kuliah_kode', String(6),
                              ForeignKey('mata_kuliah.kode'))
    mata_kuliah = relationship(
        "MataKuliah", back_populates="kelas_mata_kuliah", uselist=False)

    jadwal_kelas = relationship(
        "JadwalKelas", back_populates="kelas_mata_kuliah")
    batasan_kelas = relationship(
        "BatasanKelas", back_populates="kelas_mata_kuliah")
    dosen_kelas = relationship(
        "Dosen", secondary=dosen_kelas_association)

    def __init__(self, no_kelas, kuota, keterangan, tahun, semester, mata_kuliah):
        self.no_kelas = no_kelas
        self.kuota = kuota
        self.keterangan = keterangan
        self.tahun = tahun
        self.semester = semester
        self.mata_kuliah = mata_kuliah

    def __repr__(self):
        return "<KelasMataKuliah(no_kelas='%s', kuota='%s', keterangan='%s', tahun='%s', semester='%s', mata_kuliah='%s')>" % (
            self.no_kelas, self.kuota, self.keterangan, self.tahun, self.semester, self.mata_kuliah)
