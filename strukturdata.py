# struktur_data.py

class Stack:
    """
    Stack (LIFO) — digunakan untuk riwayat aksi dan fitur undo.
    Push = tambah ke atas, Pop = ambil dari atas.
    """
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.kosong():
            return None
        return self._data.pop()

    def peek(self):
        if self.kosong():
            return None
        return self._data[-1]

    def kosong(self):
        return len(self._data) == 0

    def ukuran(self):
        return len(self._data)

    def ke_list(self):
        """Kembalikan salinan isi stack (bawah → atas)."""
        return list(self._data)


class Queue:
    """
    Queue (FIFO) — digunakan untuk antrean aksi pet.
    Enqueue = masuk dari belakang, Dequeue = keluar dari depan.
    """
    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.kosong():
            return None
        return self._data.pop(0)

    def peek(self):
        if self.kosong():
            return None
        return self._data[0]

    def kosong(self):
        return len(self._data) == 0

    def ukuran(self):
        return len(self._data)

    def ke_list(self):
        return list(self._data)
    
    def kosongkan(self):
        self._data = []

"""
Single Linked List untuk mencatat makanan yang pernah diberikan
menambahkan yang terbaru di depan agar konstan
"""

class NodeMakanan:
    def __init__(self, nama_makanan: str, waktu_makan: str):
        self.nama_makanan = nama_makanan
        self.waktu_makan  = waktu_makan   # format "DD/MM HH:MM"
        self.berikutnya   = None


class RiwayatMakananSLL:

    def __init__(self):
        self.kepala = None
        self.ukuran = 0

    def tambah(self, nama_makanan: str, waktu_makan: str):
        node = NodeMakanan(nama_makanan, waktu_makan)
        node.berikutnya = self.kepala
        self.kepala = node
        self.ukuran += 1

    def ke_list(self) -> list:
        """Kembalikan list string dari yang terbaru ke terlama."""
        hasil = []
        node = self.kepala
        while node:
            hasil.append(f"{node.nama_makanan} ({node.waktu_makan})")
            node = node.berikutnya
        return hasil

    def ke_dict_list(self) -> list:
        """Untuk serialisasi JSON."""
        hasil = []
        node = self.kepala
        while node:
            hasil.append({
                "nama_makanan": node.nama_makanan,
                "waktu_makan": node.waktu_makan
            })
            node = node.berikutnya
        return hasil

    @classmethod
    def dari_dict_list(cls, data: list):
        sll = cls()
        # data dari JSON biasanya terbaru di awal, jadi tambahkan urut
        for item in reversed(data):
            sll.tambah(item["nama_makanan"], item["waktu_makan"])
        return sll
    


"""
Double Linked List untuk menyimpan kondisi pet disaat itu setiap hari
"""

class NodeHari:
    def __init__(self, hari_ke: int, snapshot: dict):
        self.hari_ke = hari_ke
        self.snapshot = snapshot   # dictionary berisi stat pet saat itu
        self.sebelumnya = None
        self.berikutnya = None


class HistoriHariDLL:
    def __init__(self):
        self.kepala = None
        self.ekor = None
        self.kursor = None   # posisi saat ini (NodeHari)
        self.ukuran = 0

    def tambah_hari(self, hari_ke: int, snapshot: dict):
        node = NodeHari(hari_ke, snapshot)
        if self.ekor is None:
            self.kepala = node
            self.ekor = node
        else:
            self.ekor.berikutnya = node
            node.sebelumnya = self.ekor
            self.ekor = node
        self.kursor = node   # kursor otomatis ke hari terbaru
        self.ukuran += 1

    def maju(self) -> dict | None:
        """Pindah ke hari berikutnya. Kembalikan snapshot atau None."""
        if self.kursor and self.kursor.berikutnya:
            self.kursor = self.kursor.berikutnya
            return self.kursor.snapshot
        return None

    def mundur(self) -> dict | None:
        """Pindah ke hari sebelumnya."""
        if self.kursor and self.kursor.sebelumnya:
            self.kursor = self.kursor.sebelumnya
            return self.kursor.snapshot
        return None

    def ke_awal(self) -> dict | None:
        if self.kepala:
            self.kursor = self.kepala
            return self.kepala.snapshot
        return None

    def ke_akhir(self) -> dict | None:
        if self.ekor:
            self.kursor = self.ekor
            return self.ekor.snapshot
        return None

    def info_kursor(self) -> tuple:
        """Kembalikan (hari_ke, snapshot) dari kursor saat ini."""
        if self.kursor:
            return self.kursor.hari_ke, self.kursor.snapshot
        return None, None

    def hari_sudah_ada(self, hari_ke: int) -> bool:
        """Cek apakah snapshot untuk hari_ke sudah tercatat."""
        node = self.kepala
        while node:
            if node.hari_ke == hari_ke:
                return True
            node = node.berikutnya
        return False

    def ke_dict_list(self) -> list:
        hasil = []
        node = self.kepala
        while node:
            hasil.append({
                "hari_ke": node.hari_ke,
                "snapshot": node.snapshot
            })
            node = node.berikutnya
        return hasil

    @classmethod
    def dari_dict_list(cls, data: list):
        dll = cls()
        for item in data: 
            dll.tambah_hari(item["hari_ke"], item["snapshot"])
        return dll