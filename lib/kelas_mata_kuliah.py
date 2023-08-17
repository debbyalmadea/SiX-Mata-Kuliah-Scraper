class KelasMataKuliah:

    def __init__(self, no_kelas, kuota, list_dosen, tahun: int, semester: int, keterangan='', list_batasan=[], list_jadwal=[]) -> None:
        self.no_kelas = no_kelas
        self.kuota = kuota
        self.tahun = tahun
        self.semester = semester
        self.list_dosen = list_dosen
        self.keterangan = keterangan
        self.list_batasan = list_batasan
        self.list_jadwal = list_jadwal

    def to_dict(self):
        dict = {
            "no_kelas": self.no_kelas,
            "kuota": self.kuota,
            "tahun": self.tahun,
            "semester": self.semester,
            "list_dosen": self.list_dosen,
            "keterangan": self.keterangan,
            "list_batasan": self.list_batasan,
            "list_jadwal": [jadwal.to_dict() for jadwal in self.list_jadwal]
        }

        return dict

    def __str__(self) -> str:
        return f"no_kelas: {self.no_kelas}\nkuota: {self.kuota}\nlist_dosen: {self.list_dosen}\ntahun: {self.tahun}\nsemester: {self.semester}\nketerangan: {self.keterangan}\nlist_batasan: {self.list_batasan}\nlist_jadwal: {self.list_jadwal}"
