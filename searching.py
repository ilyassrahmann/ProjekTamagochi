# searching.py
"""
Algoritma searching: Linear Search dan Binary Search
"""
from peliharaan import Peliharaan
from toko import DAFTAR_ITEM   # dictionary item toko

def linear_search_item(nama_kata_kunci: str) -> list:
    """
    Linear search pada DAFTAR_ITEM (hash table/dict) berdasarkan nama item.
    Mengembalikan list of tuple (id_item, item_dict) yang cocok (case-insensitive).
    """
    kata_kunci = nama_kata_kunci.lower()
    hasil = []
    for id_item, item in DAFTAR_ITEM.items():
        if kata_kunci in item["nama"].lower():
            hasil.append((id_item, item))
    return hasil


def binary_search_leaderboard(daftar_terurut: list, target_usia: float) -> int:
    """
    Binary search pada leaderboard yang sudah diurutkan naik berdasarkan usia.
    Mengembalikan index posisi jika ditemukan, -1 jika tidak.
    Catatan: karena usia bisa float, kita bandingkan dengan toleransi 0.01
    """
    kiri = 0
    kanan = len(daftar_terurut) - 1
    
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        usia_tengah = daftar_terurut[tengah].usia
        
        if abs(usia_tengah - target_usia) < 0.01:
            return tengah
        elif usia_tengah < target_usia:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
            
    return -1