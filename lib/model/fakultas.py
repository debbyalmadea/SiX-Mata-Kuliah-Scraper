from sqlalchemy import Column, String
from lib.config.sqlalchemy import Base
from sqlalchemy.orm import relationship


class Fakultas(Base):
    __tablename__ = 'fakultas'

    nama = Column('nama', String(50), primary_key=True)

    program_studi = relationship(
        "ProgramStudi", back_populates="fakultas")

    def __init__(self, nama):
        self.nama = nama

    def __repr__(self):
        return "<Fakultas(nama='%s')>" % (self.nama)
