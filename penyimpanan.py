import json
import os
from peliharaan import Peliharaan
from pemain    import Pemain

NAMA_FILE_SAVE = "data_save.json"

def simpan_game(peliharaan: Peliharaan, pemain: Pemain, riwayat_aksi: list):
    """
    Tulis state game ke file JSON.
    riwayat_aksi adalah list of string (log aksi yang sudah dilakukan).
    """
    data = {
        "peliharaan"  : peliharaan.ke_dict(),
        "pemain"      : pemain.ke_dict(),
        "riwayat_aksi": riwayat_aksi,
    }
    try:
        with open(NAMA_FILE_SAVE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("  💾 Game berhasil disimpan.")
    except OSError as e:
        print(f"  ⚠️  Gagal menyimpan game: {e}")

def muat_game():
    """
    Baca file save dan kembalikan tuple (Peliharaan, Pemain, riwayat_aksi).
    Kembalikan None kalau file tidak ada atau rusak.
    """
    if not os.path.exists(NAMA_FILE_SAVE):
        return None

    try:
        with open(NAMA_FILE_SAVE, "r", encoding="utf-8") as f:
            data = json.load(f)

        peliharaan   = Peliharaan.dari_dict(data["peliharaan"])
        pemain       = Pemain.dari_dict(data["pemain"])
        riwayat_aksi = data.get("riwayat_aksi", [])
        return peliharaan, pemain, riwayat_aksi

    except (json.JSONDecodeError, KeyError) as e:
        print(f"  ⚠️  File save rusak ({e}). Memulai game baru...")
        return None

def ekspor_peliharaan(peliharaan: Peliharaan, nama_file: str):
    """Ekspor data peliharaan saja ke file terpisah untuk dibagikan."""
    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            json.dump(peliharaan.ke_dict(), f, indent=2, ensure_ascii=False)
        print(f"  📤 Peliharaan berhasil diekspor ke '{nama_file}'.")
    except OSError as e:
        print(f"  ⚠️  Gagal ekspor: {e}")


def impor_peliharaan(nama_file: str):
    """Impor peliharaan dari file ekspor milik orang lain."""
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Peliharaan.dari_dict(data)
    except FileNotFoundError:
        print(f"  ⚠️  File '{nama_file}' tidak ditemukan.")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  ⚠️  File tidak valid: {e}")
        return None
