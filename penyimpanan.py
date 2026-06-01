import json
import os
from peliharaan import Peliharaan
from pemain    import Pemain

NAMA_FILE_SAVE = "data_save.json"
SAVE_VERSION   = 1


def _migrasi_save(data: dict) -> dict:
    """
    Normalisasi save lama: pastikan riwayat_makanan & histori_hari ada
    di dalam blok peliharaan (save v0 tidak punya save_version).
    """
    pel = data.setdefault("peliharaan", {})
    pel.setdefault("riwayat_makanan", [])
    pel.setdefault("histori_hari", [])
    data["save_version"] = SAVE_VERSION
    return data


def simpan_game(peliharaan: Peliharaan, pemain: Pemain, riwayat_aksi: list):
    """
    Tulis state game ke file JSON.
    riwayat_makanan & histori_hari diserialisasi lewat peliharaan.ke_dict().
    """
    data = {
        "save_version" : SAVE_VERSION,
        "peliharaan"   : peliharaan.ke_dict(),
        "pemain"       : pemain.ke_dict(),
        "riwayat_aksi" : riwayat_aksi,
    }
    try:
        with open(NAMA_FILE_SAVE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("  💾 Game berhasil disimpan.")
    except OSError as e:
        print(f"  ⚠️  Gagal menyimpan game: {e}")


def hapus_save() -> bool:
    """Hapus file save jika ada. Kembalikan True jika berhasil atau file tidak ada."""
    if not os.path.exists(NAMA_FILE_SAVE):
        return True
    try:
        os.remove(NAMA_FILE_SAVE)
        return True
    except OSError as e:
        print(f"  ⚠️  Gagal menghapus save: {e}")
        return False


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

        if "peliharaan" not in data or "pemain" not in data:
            raise KeyError("struktur save tidak lengkap")

        data = _migrasi_save(data)

        peliharaan   = Peliharaan.dari_dict(data["peliharaan"])
        pemain       = Pemain.dari_dict(data["pemain"])
        riwayat_aksi = data.get("riwayat_aksi", [])
        return peliharaan, pemain, riwayat_aksi

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"  ⚠️  File save rusak ({e}). Memulai game baru...")
        return None
