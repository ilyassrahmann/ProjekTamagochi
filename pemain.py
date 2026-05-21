class Pemain:
    def __init__(self, nama_pemain):
        self.nama_pemain      = nama_pemain
        self.koin             = 50          
        self.total_hari_hidup = 0          
        self.daftar_badge     = set()       

    def ke_dict(self):
        return {
            "nama_pemain"      : self.nama_pemain,
            "koin"             : self.koin,
            "total_hari_hidup" : self.total_hari_hidup,
            "daftar_badge"     : list(self.daftar_badge),  
        }

    @classmethod
    def dari_dict(cls, data):
        p = cls(data["nama_pemain"])
        p.koin             = data["koin"]
        p.total_hari_hidup = data["total_hari_hidup"]
        p.daftar_badge     = set(data["daftar_badge"])
        return p

    def tambah_koin(self, jumlah):
        self.koin += jumlah
        print(f"  +{jumlah} koin! Total koin: {self.koin}")

    def kurangi_koin(self, jumlah):
        """Kembalikan True kalau berhasil, False kalau koin tidak cukup."""
        if self.koin < jumlah:
            print(f"  Koin tidak cukup! Kamu punya {self.koin} koin.")
            return False
        self.koin -= jumlah
        return True

    def tambah_badge(self, nama_badge):
        if nama_badge not in self.daftar_badge:
            self.daftar_badge.add(nama_badge)
            print(f"  🏅 Badge baru terbuka: {nama_badge}!")
