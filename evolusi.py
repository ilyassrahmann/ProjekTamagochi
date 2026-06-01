"""
Tree pohon evolusi dan Graph hubungan antar tahap evolusi dengan syarat unlock.
"""

# =============================================================================
# TREE — Pohon Evolusi (struktur hierarki)
# =============================================================================

class NodeEvolusi:
    """Satu node dalam pohon evolusi."""
    def __init__(self, nama: str, deskripsi: str = ""):
        self.nama = nama
        self.deskripsi = deskripsi
        self.anak = []      # list of NodeEvolusi
        self.induk = None

    def tambah_anak(self, node):
        node.induk = self
        self.anak.append(node)


class PohonEvolusi:
    """
    Pohon evolusi yang menunjukkan jalur perkembangan peliharaan.
    Akar = Telur, cabang berdasarkan kondisi perawatan.
    """
    def __init__(self):
        self.akar = self._bangun_pohon()

    def _bangun_pohon(self):
        # Level 0
        telur = NodeEvolusi("Telur", "Tahap awal, baru menetas.")

        # Level 1
        bayi = NodeEvolusi("Bayi", "Mulai tumbuh, butuh perhatian.")
        telur.tambah_anak(bayi)

        # Level 2 — percabangan pertama
        sehat = NodeEvolusi("Remaja Sehat", "Tumbuh optimal karena dirawat baik.")
        kurang = NodeEvolusi("Remaja Kurus", "Sering lapar, pertumbuhan terhambat.")
        bayi.tambah_anak(sehat)
        bayi.tambah_anak(kurang)

        # Level 3 — percabangan kedua
        atletis = NodeEvolusi("Dewasa Atletis", "Bugar, sering diajak main.")
        bijak = NodeEvolusi("Dewasa Bijak", "Sehat dan tenang.")
        kurus = NodeEvolusi("Dewasa Kurus", "Bertahan dengan berat kurang.")
        sakit = NodeEvolusi("Dewasa Sakit", "Sering sakit, butuh perhatian medis.")
        sehat.tambah_anak(atletis)
        sehat.tambah_anak(bijak)
        kurang.tambah_anak(kurus)
        kurang.tambah_anak(sakit)

        # Level 4 — tahap akhir
        legenda = NodeEvolusi("Legenda", "Puncak evolusi, sangat langka.")
        tua_sehat = NodeEvolusi("Tua Sehat", "Usia lanjut dengan kesehatan baik.")
        tua_kurus = NodeEvolusi("Tua Kurus", "Bertahan hingga tua meski kurang gizi.")
        arwah = NodeEvolusi("Arwah", "Sudah tiada, namun dikenang.")
        atletis.tambah_anak(legenda)
        bijak.tambah_anak(tua_sehat)
        kurus.tambah_anak(tua_kurus)
        sakit.tambah_anak(arwah)

        return telur

    def cari_node(self, nama_tahap: str):
        """BFS mencari node berdasarkan nama."""
        from collections import deque
        if not self.akar:
            return None
        queue = deque([self.akar])
        while queue:
            node = queue.popleft()
            if node.nama == nama_tahap:
                return node
            queue.extend(node.anak)
        return None

    def tampilkan_pohon(self, node=None, level=0):
        """Cetak pohon ke terminal (untuk debugging/info)."""
        if node is None:
            node = self.akar
        print("  " + "  " * level + f"└─ {node.nama}")
        for anak in node.anak:
            self.tampilkan_pohon(anak, level + 1)


# =============================================================================
# GRAPH — Hubungan antar tahap dengan syarat (adjacency list)
# =============================================================================

class GraphEvolusi:
    """
    Graph berarah yang mendefinisikan dari suatu tahap, ke tahap apa saja
    yang bisa dicapai beserta syarat minimal stat yang harus dipenuhi.
    """
    def __init__(self):
        self.adjacency = {}   # { dari_tahap: [ {tujuan, syarat} ] }

    def _tambah_edge(self, dari: str, ke: str, syarat: dict):
        if dari not in self.adjacency:
            self.adjacency[dari] = []
        self.adjacency[dari].append({"tujuan": ke, "syarat": syarat})

    def bangun_graph(self):
        """Mendefinisikan semua edge evolusi dengan syaratnya."""
        # Dari Telur ke Bayi
        self._tambah_edge("Telur", "Bayi", {"usia": 0.5})

        # Dari Bayi ke Remaja (cabang)
        self._tambah_edge("Bayi", "Remaja Sehat", {"usia": 2, "kesehatan": 60, "kelaparan": 50})
        self._tambah_edge("Bayi", "Remaja Kurus", {"usia": 2})   # fallback

        # Dari Remaja Sehat ke Dewasa (fallback di akhir agar prioritas tetap ke jalur utama)
        self._tambah_edge("Remaja Sehat", "Dewasa Atletis", {"usia": 5, "kesenangan": 70, "energi": 60})
        self._tambah_edge("Remaja Sehat", "Dewasa Bijak", {"usia": 5, "kesehatan": 80})
        self._tambah_edge("Remaja Sehat", "Dewasa Kurus", {"usia": 5})

        # Dari Remaja Kurus ke Dewasa
        self._tambah_edge("Remaja Kurus", "Dewasa Kurus", {"usia": 5, "kesehatan": 30})
        self._tambah_edge("Remaja Kurus", "Dewasa Sakit", {"usia": 5})   # jika kesehatan sangat rendah

        # Dari Dewasa Atletis ke Legenda
        self._tambah_edge("Dewasa Atletis", "Legenda", {"usia": 15, "kesehatan": 90, "kesenangan": 80})
        # Dari Dewasa Bijak ke Tua Sehat
        self._tambah_edge("Dewasa Bijak", "Tua Sehat", {"usia": 15, "kesehatan": 75})
        # Dari Dewasa Kurus ke Tua Kurus
        self._tambah_edge("Dewasa Kurus", "Tua Kurus", {"usia": 15})
        # Arwah dicapai saat kematian (lihat waktu._terapkan_kematian)

    def cek_evolusi(self, peliharaan) -> str | None:
        """
        Cek apakah peliharaan memenuhi syarat untuk berevolusi ke tahap berikutnya.
        Kembalikan nama tahap baru, atau None jika tidak ada.
        Prioritas: edge pertama yang syaratnya terpenuhi.
        """
        tahap_kini = peliharaan.tahap_evolusi
        if tahap_kini not in self.adjacency:
            return None
        for edge in self.adjacency[tahap_kini]:
            syarat = edge["syarat"]
            terpenuhi = all(
                getattr(peliharaan, stat, 0) >= nilai
                for stat, nilai in syarat.items()
            )
            if terpenuhi:
                return edge["tujuan"]
        return None

    def tampilkan_jalur(self, dari: str):
        """Tampilkan semua kemungkinan evolusi dari suatu tahap."""
        if dari not in self.adjacency:
            print(f"  {dari} adalah tahap akhir (tidak bisa berevolusi lebih lanjut).")
            return
        print(f"  Dari {dari}, dapat berevolusi ke:")
        for edge in self.adjacency[dari]:
            syarat_str = ", ".join(f"{k}≥{v}" for k, v in edge["syarat"].items())
            print(f"    → {edge['tujuan']}  (syarat: {syarat_str})")