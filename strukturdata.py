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
        self.data = []