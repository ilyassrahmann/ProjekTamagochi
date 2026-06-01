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

        # Sambungkan melingkar
        pagi.berikutnya  = siang
        siang.berikutnya = malam
        malam.berikutnya = pagi   

        self.kepala = pagi

    def periode_sekarang(self):
        """Kembalikan NodeWaktu yang sesuai dengan jam sistem saat ini."""
        jam_sekarang = datetime.now().hour
        node = self.kepala
        for _ in range(3):                          
            if node.jam_mulai <= node.jam_selesai:  
                if node.jam_mulai <= jam_sekarang < node.jam_selesai:
                    return node
            else:                                   
                if jam_sekarang >= node.jam_mulai or jam_sekarang < node.jam_selesai:
                    return node
            node = node.berikutnya
        return self.kepala                          


LAJU_PER_JAM = {
    "kelaparan" : -10.0,   
    "kesenangan":  -5.0,   
    "energi"    :   3.0,   
}
LAJU_KESEHATAN_LAPAR    = -15.0  
LAJU_KESEHATAN_NORMAL   =   1.0  
LAJU_PERTAMBAHAN_USIA   =  1/24 


def hitung_pembusukan(peliharaan, siklus: SiklusWaktu):
    sekarang      = datetime.now()
    terakhir      = datetime.fromisoformat(peliharaan.terakhir_diupdate)
    selisih_detik = (sekarang - terakhir).total_seconds()
    jam_berlalu   = selisih_detik / 3600

    if jam_berlalu < 0.01:          
        return

    periode = siklus.periode_sekarang()

    delta_lapar  = LAJU_PER_JAM["kelaparan"]  * periode.multiplier_lapar  * jam_berlalu
    delta_senang = LAJU_PER_JAM["kesenangan"] * periode.multiplier_senang * jam_berlalu
    delta_energi = LAJU_PER_JAM["energi"]     * periode.multiplier_energi * jam_berlalu

    peliharaan.kelaparan  = max(0.0, min(100.0, peliharaan.kelaparan  + delta_lapar))
    peliharaan.kesenangan = max(0.0, min(100.0, peliharaan.kesenangan + delta_senang))
    peliharaan.energi     = max(0.0, min(100.0, peliharaan.energi     + delta_energi))

    if peliharaan.kelaparan <= 0:
        delta_kesehatan = LAJU_KESEHATAN_LAPAR * jam_berlalu
    else:
        delta_kesehatan = LAJU_KESEHATAN_NORMAL * jam_berlalu
    peliharaan.kesehatan = max(0.0, min(100.0, peliharaan.kesehatan + delta_kesehatan))

    peliharaan.usia += jam_berlalu * LAJU_PERTAMBAHAN_USIA
    peliharaan.usia  = round(peliharaan.usia, 2)

    if peliharaan.kesehatan <= 0:
        peliharaan.masih_hidup = False

    peliharaan.terakhir_diupdate = sekarang.isoformat()

    print(f"\n  [{periode.nama_periode}] Waktu berlalu: {jam_berlalu:.1f} jam")
    if not peliharaan.masih_hidup:
        print("  ❌ Peliharaanmu meninggal saat kamu pergi...")
    else:
        print(f"  Kelaparan : {peliharaan.kelaparan:.1f}  |  "
              f"Kesenangan: {peliharaan.kesenangan:.1f}  |  "
              f"Kesehatan : {peliharaan.kesehatan:.1f}")

def percepat_waktu(peliharaan, siklus: SiklusWaktu, jam: float):
    waktu_palsu = datetime.now() - timedelta(hours=jam)
    peliharaan.terakhir_diupdate = waktu_palsu.isoformat()
    print(f"  ⏩ [DEBUG] Waktu dipercepat {jam} jam ke depan.")
    hitung_pembusukan(peliharaan, siklus)