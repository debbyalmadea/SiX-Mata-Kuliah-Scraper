class MataKuliah:
    def __init__(self, kode, kode_prodi, nama, sks, list_kelas=[]) -> None:
        self.kode = kode
        self.kode_prodi = kode_prodi
        self.nama = nama
        self.sks = sks
        self.list_kelas = list_kelas

    def to_dict(self):
        dict = {
            "kode": self.kode,
            "kode_prodi": self.kode_prodi,
            "nama": self.nama,
            "sks": self.sks,
            "list_kelas": [kelas.to_dict() for kelas in self.list_kelas]
        }

        return dict

    def __str__(self) -> str:
        return f"kode: {self.kode}\nkode_prodi: {self.kode_prodi}\nnama: {self.nama}\nsks: {self.sks}"
