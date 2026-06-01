from datetime import datetime, timedelta


class NodeWaktu:
    """Satu periode dalam siklus harian."""
    def __init__(self, nama_periode, jam_mulai, jam_selesai,
                 multiplier_lapar, multiplier_senang, multiplier_energi):
        self.nama_periode   = nama_periode
        self.jam_mulai      = jam_mulai
        self.jam_selesai    = jam_selesai
        self.multiplier_lapar  = multiplier_lapar
        self.multiplier_senang = multiplier_senang
        self.multiplier_energi = multiplier_energi
        self.berikutnya     = None


class SiklusWaktu:
    def __init__(self):
        self.kepala = None
        self._bangun_siklus()

    def _bangun_siklus(self):
        pagi  = NodeWaktu("Pagi",  6,  12, multiplier_lapar=1.0, multiplier_senang=1.0, multiplier_energi=0.5)
        siang = NodeWaktu("Siang", 12, 18, multiplier_lapar=1.5, multiplier_senang=1.2, multiplier_energi=0.3)
        malam = NodeWaktu("Malam", 18,  6, multiplier_lapar=0.5, multiplier_senang=0.8, multiplier_energi=1.5)

        pagi.berikutnya  = siang
        siang.berikutnya = malam
        malam.berikutnya = pagi

        self.kepala = pagi

    def periode_pada_jam(self, jam: int) -> NodeWaktu:
        """API publik: periode aktif untuk jam 0–23."""
        node = self.kepala
        for _ in range(3):
            if node.jam_mulai <= node.jam_selesai:
                if node.jam_mulai <= jam < node.jam_selesai:
                    return node
            else:
                if jam >= node.jam_mulai or jam < node.jam_selesai:
                    return node
            node = node.berikutnya
        return self.kepala

    def periode_sekarang(self) -> NodeWaktu:
        """Kembalikan NodeWaktu yang sesuai dengan jam sistem saat ini."""
        return self.periode_pada_jam(datetime.now().hour)

    def simulasikan_pembusukan(self, peliharaan, waktu_mulai: datetime,
                               waktu_selesai: datetime) -> tuple:
        """
        Simulasi decay per jam antara dua waktu.
        Kembalikan (periode_terakhir, jam_berlalu).
        """
        jam_berlalu = (waktu_selesai - waktu_mulai).total_seconds() / 3600
        if jam_berlalu < 0.01:
            return self.periode_sekarang(), 0.0

        waktu_sim = waktu_mulai
        sisa_jam = jam_berlalu
        periode_terakhir = self.periode_pada_jam(waktu_sim.hour)

        while sisa_jam > 0.001 and peliharaan.masih_hidup:
            langkah = min(1.0, sisa_jam)
            periode_terakhir = self.periode_pada_jam(waktu_sim.hour)
            if not _terapkan_pembusukan_jam(peliharaan, periode_terakhir, langkah):
                break
            waktu_sim += timedelta(hours=langkah)
            sisa_jam -= langkah

        return periode_terakhir, jam_berlalu


LAJU_PER_JAM = {
    "kelaparan" : -10.0,
    "kesenangan":  -5.0,
    "energi"    :   3.0,
}
LAJU_KESEHATAN_LAPAR    = -15.0
LAJU_KESEHATAN_NORMAL   =   1.0
LAJU_PERTAMBAHAN_USIA   =  1/24


def _terapkan_pembusukan_jam(peliharaan, periode: NodeWaktu, jam_delta: float) -> bool:
    """
    Terapkan perubahan stat untuk selang waktu jam_delta.
    Kembalikan False jika peliharaan mati.
    """
    delta_lapar  = LAJU_PER_JAM["kelaparan"]  * periode.multiplier_lapar  * jam_delta
    delta_senang = LAJU_PER_JAM["kesenangan"] * periode.multiplier_senang * jam_delta
    delta_energi = LAJU_PER_JAM["energi"]     * periode.multiplier_energi * jam_delta

    peliharaan.kelaparan  = max(0.0, min(100.0, peliharaan.kelaparan  + delta_lapar))
    peliharaan.kesenangan = max(0.0, min(100.0, peliharaan.kesenangan + delta_senang))
    peliharaan.energi     = max(0.0, min(100.0, peliharaan.energi     + delta_energi))

    if peliharaan.kelaparan <= 0:
        delta_kesehatan = LAJU_KESEHATAN_LAPAR * jam_delta
    else:
        delta_kesehatan = LAJU_KESEHATAN_NORMAL * jam_delta
    peliharaan.kesehatan = max(0.0, min(100.0, peliharaan.kesehatan + delta_kesehatan))

    peliharaan.usia += jam_delta * LAJU_PERTAMBAHAN_USIA
    peliharaan.usia  = round(peliharaan.usia, 2)

    if peliharaan.kesehatan <= 0:
        peliharaan.masih_hidup = False
        _terapkan_kematian(peliharaan)
        return False
    return True


def _terapkan_kematian(peliharaan):
    """Semua kematian berujung pada tahap Arwah (konsisten dengan pohon evolusi)."""
    if peliharaan.tahap_evolusi != "Arwah":
        peliharaan.tahap_evolusi = "Arwah"


def hitung_pembusukan(peliharaan, siklus: SiklusWaktu, tampilkan_log: bool = True):
    """
    Hitung perubahan stat berdasarkan waktu nyata sejak terakhir_diupdate.
    """
    sekarang = datetime.now()
    try:
        terakhir = datetime.fromisoformat(peliharaan.terakhir_diupdate)
    except (ValueError, TypeError):
        terakhir = sekarang
        peliharaan.terakhir_diupdate = sekarang.isoformat()

    if terakhir > sekarang:
        peliharaan.terakhir_diupdate = sekarang.isoformat()
        return

    periode_terakhir, jam_berlalu = siklus.simulasikan_pembusukan(
        peliharaan, terakhir, sekarang
    )
    if jam_berlalu < 0.01:
        return

    peliharaan.terakhir_diupdate = sekarang.isoformat()

    if not tampilkan_log:
        return

    print(f"\n  [{periode_terakhir.nama_periode}] Waktu berlalu: {jam_berlalu:.1f} jam")
    if not peliharaan.masih_hidup:
        print("  ❌ Peliharaanmu meninggal...")
    else:
        print(f"  Kelaparan : {peliharaan.kelaparan:.1f}  |  "
              f"Kesenangan: {peliharaan.kesenangan:.1f}  |  "
              f"Kesehatan : {peliharaan.kesehatan:.1f}")
