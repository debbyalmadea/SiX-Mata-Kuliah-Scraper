class JadwalKelas:
    def __init__(self, hari, waktu_awal, waktu_akhir, ruangan) -> None:
        self.hari = hari
        self.waktu_awal = waktu_awal
        self.waktu_akhir = waktu_akhir
        self.ruangan = ruangan

    def is_equal(self, jadwal):
        return (
            self.hari == jadwal.hari and
            self.waktu_awal == jadwal.waktu_awal and
            self.waktu_akhir == jadwal.waktu_akhir
        )

    def to_dict(self):
        dict = {
            "hari": self.hari,
            "waktu_awal": self.waktu_awal.strftime("%H.%M"),
            "waktu_akhir": self.waktu_akhir.strftime("%H.%M"),
            "ruangan": self.ruangan
        }

        return dict

    def __str__(self) -> str:
        return f"hari: {self.hari}\nwaktu_awal: {self.waktu_awal}\nwaktu_akhir: {self.waktu_akhir}\nruangan: {self.ruangan}"
