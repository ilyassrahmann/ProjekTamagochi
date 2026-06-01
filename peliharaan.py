from datetime import datetime
from strukturdata import RiwayatMakananSLL, HistoriHariDLL


class Peliharaan:
    def __init__(self, nama, spesies):
        self.nama              = nama
        self.spesies           = spesies
        self.usia              = 0          
        self.kelaparan         = 80.0       
        self.kesenangan        = 70.0       
        self.kesehatan         = 100.0      
        self.berat             = 5.0        
        self.energi            = 100.0     
        self.tahap_evolusi     = "Telur"
        self.masih_hidup       = True
        self.terakhir_diupdate = datetime.now().isoformat()

        self.riwayat_makanan = RiwayatMakananSLL()
        self.histori_hari = HistoriHariDLL()

    def ke_dict(self):
        return {
            "nama"              : self.nama,
            "spesies"           : self.spesies,
            "usia"              : self.usia,
            "kelaparan"         : self.kelaparan,
            "kesenangan"        : self.kesenangan,
            "kesehatan"         : self.kesehatan,
            "berat"             : self.berat,
            "energi"            : self.energi,
            "tahap_evolusi"     : self.tahap_evolusi,
            "masih_hidup"       : self.masih_hidup,
            "terakhir_diupdate" : self.terakhir_diupdate,
            "riwayat_makanan"   : self.riwayat_makanan.ke_dict_list(),
            "histori_hari"      : self.histori_hari.ke_dict_list(),
        }

    @classmethod
    def dari_dict(cls, data):
        p = cls(data["nama"], data["spesies"])
        p.usia              = data["usia"]
        p.kelaparan         = data["kelaparan"]
        p.kesenangan        = data["kesenangan"]
        p.kesehatan         = data["kesehatan"]
        p.berat             = data["berat"]
        p.energi            = data["energi"]
        p.tahap_evolusi     = data["tahap_evolusi"]
        p.masih_hidup       = data["masih_hidup"]
        p.terakhir_diupdate = data["terakhir_diupdate"]
        if "riwayat_makanan" in data:
            p.riwayat_makanan = RiwayatMakananSLL.dari_dict_list(data["riwayat_makanan"])
        if "histori_hari" in data:
            p.histori_hari = HistoriHariDLL.dari_dict_list(data["histori_hari"])
        return p

    def status_kelaparan(self):
        """Kembalikan label teks berdasarkan nilai kelaparan."""
        if self.kelaparan >= 70:
            return "Kenyang"
        elif self.kelaparan >= 40:
            return "Biasa"
        elif self.kelaparan >= 15:
            return "Lapar"
        else:
            return "Sangat Lapar!"

    def status_mood(self):
        if self.kesenangan >= 70:
            return "Bahagia"
        elif self.kesenangan >= 40:
            return "Biasa"
        elif self.kesenangan >= 15:
            return "Sedih"
        else:
            return "Sangat Sedih!"

    def status_kesehatan(self):
        if self.kesehatan >= 70:
            return "Sehat"
        elif self.kesehatan >= 40:
            return "Kurang Sehat"
        elif self.kesehatan >= 15:
            return "Sakit"
        else:
            return "Kritis!"

    def ringkasan(self):
        """Kembalikan string ringkasan satu baris untuk leaderboard/export."""
        return (
            f"{self.nama} ({self.spesies}) | "
            f"Usia: {self.usia} hari | "
            f"Evolusi: {self.tahap_evolusi} | "
            f"{'Hidup' if self.masih_hidup else 'Mati'}"
        )
