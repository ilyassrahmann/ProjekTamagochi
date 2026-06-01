from datetime import datetime
from strukturdata import RiwayatMakananSLL, HistoriHariDLL


class Peliharaan:
    def __init__(self, nama, spesies):
        self.nama              = nama
        self.spesies           = spesies
        self.usia              = 0.0          
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
        p.riwayat_makanan = RiwayatMakananSLL.dari_dict_list(
            data.get("riwayat_makanan", []))
        p.histori_hari = HistoriHariDLL.dari_dict_list(
            data.get("histori_hari", []))
        return p

    def status_kelaparan(self):
        """Kembalikan label teks berdasarkan nilai kelaparan."""
        v = max(0.0, min(100.0, self.kelaparan))
        if v >= 70:
            return "Kenyang"
        elif v >= 40:
            return "Biasa"
        elif v >= 15:
            return "Lapar"
        return "Sangat Lapar!"

    def status_mood(self):
        v = max(0.0, min(100.0, self.kesenangan))
        if v >= 70:
            return "Bahagia"
        elif v >= 40:
            return "Biasa"
        elif v >= 15:
            return "Sedih"
        return "Sangat Sedih!"

    def status_kesehatan(self):
        v = max(0.0, min(100.0, self.kesehatan))
        if v >= 70:
            return "Sehat"
        elif v >= 40:
            return "Kurang Sehat"
        elif v >= 15:
            return "Sakit"
        return "Kritis!"

    def ringkasan(self):
        """Kembalikan string ringkasan satu baris untuk leaderboard/export."""
        return (
            f"{self.nama} ({self.spesies}) | "
            f"Usia: {self.usia} hari | "
            f"Evolusi: {self.tahap_evolusi} | "
            f"{'Hidup' if self.masih_hidup else 'Mati'}"
        )

    def hitung_skor_kebugaran(self, kedalaman: int = 0) -> float:
        """
        Hitung skor kebugaran keseluruhan secara rekursif.
        Setiap level rekursif menambahkan kontribusi satu stat dengan bobot tertentu.
        """
        # Daftar stat dan bobotnya (total 100%)
        stat_bobot = [
            ("kesehatan",  0.40),   # 40%
            ("kelaparan",  0.25),   # 25%
            ("kesenangan", 0.20),   # 20%
            ("energi",     0.15),   # 15%
        ]
        
        # Base case: sudah melewati semua stat
        if kedalaman >= len(stat_bobot):
            return 0.0
        
        nama_stat, bobot = stat_bobot[kedalaman]
        nilai_stat = getattr(self, nama_stat)
        
        # Rekursif: kontribusi stat ini + lanjut ke stat berikutnya
        return (nilai_stat * bobot) + self.hitung_skor_kebugaran(kedalaman + 1)
    
    def kategori_skor(self) -> str:
        """Kembalikan label kategori berdasarkan skor rekursif."""
        skor = self.hitung_skor_kebugaran()
        if skor >= 80:
            return "Luar Biasa"
        elif skor >= 60:
            return "Baik"
        elif skor >= 40:
            return "Cukup"
        else:
            return "Buruk"
