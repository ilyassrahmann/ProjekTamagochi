# sorting.py
"""
Algoritma sorting custom: Bubble Sort
"""

def bubble_sort_peliharaan(daftar_peliharaan: list, kunci: str, urutan: str = "turun") -> list:
    """
    Bubble sort untuk list objek Peliharaan.
    kunci: atribut yang akan dijadikan acuan sorting (misal: 'usia', 'kesehatan')
    urutan: 'naik' (ascending) atau 'turun' (descending)
    """
    if not daftar_peliharaan:
        return []
    
    hasil = list(daftar_peliharaan)   # salin agar tidak mengubah asli
    n = len(hasil)
    
    for i in range(n - 1):
        for j in range(n - i - 1):
            nilai_kiri = getattr(hasil[j], kunci)
            nilai_kanan = getattr(hasil[j + 1], kunci)
            
            if urutan == "turun":
                kondisi_tukar = nilai_kiri < nilai_kanan
            else:  # naik
                kondisi_tukar = nilai_kiri > nilai_kanan
                
            if kondisi_tukar:
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
                
    return hasil


def bubble_sort_str(daftar_str: list, urutan: str = "naik") -> list:
    """Bubble sort untuk list of string."""
    if not daftar_str:
        return []
    hasil = list(daftar_str)
    n = len(hasil)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if urutan == "naik":
                if hasil[j] > hasil[j + 1]:
                    hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
            else:  # turun
                if hasil[j] < hasil[j + 1]:
                    hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
    return hasil