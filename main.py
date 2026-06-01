from peliharaan   import Peliharaan
from pemain       import Pemain
from waktu        import SiklusWaktu, hitung_pembusukan
from penyimpanan  import simpan_game, muat_game, hapus_save
from toko         import tampilkan_menu_toko
from minigame     import tampilkan_menu_minigame
from strukturdata import Stack
from evolusi      import PohonEvolusi, GraphEvolusi
import math
from tampilan     import (
    tampilkan_status,
    tampilkan_menu_utama,
    tampilkan_riwayat,
    tampilkan_info_pemain,
    tampilkan_layar_kematian,
    tampilkan_layar_sambutan,
    tampilkan_navigasi_histori,
    tampilkan_riwayat_makanan,
    tampilkan_leaderboard,
    tampilkan_pencarian_item,
    tampilkan_pencarian_pet_usia,
    pilih_spesies,
    konfirmasi_game_baru,
)


def mulai_game_baru() -> tuple:
    tampilkan_layar_sambutan()
    print("\n  Mari mulai petualangan baru!\n")

    nama_pemain = input("  Masukkan nama pemain: ").strip() or "Pemain"
    nama_pet    = input("  Beri nama peliharaanmu: ").strip() or "Dihar"
    spesies     = pilih_spesies()

    peliharaan  = Peliharaan(nama_pet, spesies)
    pemain      = Pemain(nama_pemain)
    riwayat     = Stack()

    print(f"\n  Selamat! {nama_pet} si {spesies} baru saja lahir. 🥚")
    print(f"  Kamu punya {pemain.koin} koin untuk memulai.")
    input("\n  Tekan Enter untuk mulai...")
    return peliharaan, pemain, riwayat


def buat_snapshot_hari(peliharaan: Peliharaan, hari_ke: int) -> dict:
    """Snapshot kondisi pet; usia dicatat sesuai nomor hari."""
    return {
        "usia": float(hari_ke),
        "kelaparan": peliharaan.kelaparan,
        "kesenangan": peliharaan.kesenangan,
        "kesehatan": peliharaan.kesehatan,
        "berat": peliharaan.berat,
        "energi": peliharaan.energi,
        "tahap_evolusi": peliharaan.tahap_evolusi,
    }


def catat_hari_baru(peliharaan: Peliharaan, pemain: Pemain, hari_terakhir: int) -> int:
    """Simpan snapshot per hari baru dan perbarui total_hari_hidup."""
    hari_sekarang = math.floor(peliharaan.usia)
    if hari_sekarang <= hari_terakhir:
        return hari_terakhir

    for h in range(hari_terakhir + 1, hari_sekarang + 1):
        if not peliharaan.histori_hari.hari_sudah_ada(h):
            snapshot = buat_snapshot_hari(peliharaan, h)
            peliharaan.histori_hari.tambah_hari(h, snapshot)
            print(f"  📅 Snapshot hari ke-{h} tersimpan.")

    pemain.total_hari_hidup = max(pemain.total_hari_hidup, hari_sekarang)
    return hari_sekarang


def cek_badge(peliharaan: Peliharaan, pemain: Pemain):
    """Cek kondisi badge dan berikan kalau belum dimiliki."""
    if peliharaan.usia >= 7 and "Bertahan 7 Hari" not in pemain.daftar_badge:
        pemain.tambah_badge("Bertahan 7 Hari")
    if peliharaan.usia >= 30 and "Veteran Sebulan" not in pemain.daftar_badge:
        pemain.tambah_badge("Veteran Sebulan")
    if pemain.koin >= 200 and "Juragan Koin" not in pemain.daftar_badge:
        pemain.tambah_badge("Juragan Koin")
    if (peliharaan.kesehatan >= 95
            and peliharaan.kelaparan >= 50
            and peliharaan.kesenangan >= 50
            and "Kesehatan Prima" not in pemain.daftar_badge):
        pemain.tambah_badge("Kesehatan Prima")


def cek_dan_terapkan_evolusi(peliharaan: Peliharaan, pemain: Pemain,
                              riwayat: Stack, graph_evolusi: GraphEvolusi) -> bool:
    """Cek evolusi; kembalikan True jika terjadi evolusi."""
    tahap_baru = graph_evolusi.cek_evolusi(peliharaan)
    if tahap_baru and tahap_baru != peliharaan.tahap_evolusi:
        print(f"\n  ✨✨ {peliharaan.nama} berevolusi menjadi {tahap_baru}! ✨✨")
        peliharaan.tahap_evolusi = tahap_baru
        riwayat.push(f"Evolusi! {peliharaan.nama} menjadi {tahap_baru}")
        pemain.tambah_koin(20)
        print("  Bonus evolusi: +20 koin!")
        return True
    return False


def muat_atau_buat_sessi(siklus_waktu: SiklusWaktu):
    """
    Muat save atau buat game baru.
    Kembalikan (peliharaan, pemain, riwayat, hari_terakhir) atau None jika batal.
    """
    hasil_muat = muat_game()
    if not hasil_muat:
        peliharaan, pemain, riwayat = mulai_game_baru()
        return peliharaan, pemain, riwayat, math.floor(peliharaan.usia)

    peliharaan, pemain, riwayat_list = hasil_muat
    riwayat = Stack()
    for aksi in riwayat_list:
        riwayat.push(aksi)

    tampilkan_layar_sambutan()

    if not peliharaan.masih_hidup:
        print(f"\n  Save ditemukan: {peliharaan.nama} sudah meninggal.")
        if konfirmasi_game_baru():
            hapus_save()
            peliharaan, pemain, riwayat = mulai_game_baru()
            return peliharaan, pemain, riwayat, math.floor(peliharaan.usia)
        return None

    print(f"\n  Selamat datang kembali, {pemain.nama_pemain}!")
    print(f"  {peliharaan.nama} merindukanmu...\n")
    hitung_pembusukan(peliharaan, siklus_waktu, tampilkan_log=True)

    if not peliharaan.masih_hidup:
        simpan_game(peliharaan, pemain, riwayat.ke_list())
        if tampilkan_layar_kematian(peliharaan, pemain):
            hapus_save()
            peliharaan, pemain, riwayat = mulai_game_baru()
            return peliharaan, pemain, riwayat, math.floor(peliharaan.usia)
        return None

    input("\n  Tekan Enter untuk melanjutkan...")
    hari_terakhir = max(
        math.floor(peliharaan.usia),
        _hari_tertinggi_dari_histori(peliharaan),
    )
    return peliharaan, pemain, riwayat, hari_terakhir


def _hari_tertinggi_dari_histori(peliharaan: Peliharaan) -> int:
    """Ambil nomor hari tertinggi yang sudah tersimpan di DLL."""
    terbesar = 0
    for item in peliharaan.histori_hari.ke_dict_list():
        terbesar = max(terbesar, item["hari_ke"])
    return terbesar


def jalankan_loop_utama(peliharaan: Peliharaan, pemain: Pemain, riwayat: Stack,
                        siklus_waktu: SiklusWaktu, pohon_evolusi: PohonEvolusi,
                        graph_evolusi: GraphEvolusi, hari_terakhir: int) -> bool:
    """
    Loop permainan utama.
    Kembalikan True jika pemain ingin memulai game baru setelah kematian.
    """
    while True:
        if not peliharaan.masih_hidup:
            simpan_game(peliharaan, pemain, riwayat.ke_list())
            return tampilkan_layar_kematian(peliharaan, pemain)

        hitung_pembusukan(peliharaan, siklus_waktu, tampilkan_log=False)

        if not peliharaan.masih_hidup:
            simpan_game(peliharaan, pemain, riwayat.ke_list())
            return tampilkan_layar_kematian(peliharaan, pemain)

        hari_terakhir = catat_hari_baru(peliharaan, pemain, hari_terakhir)
        cek_badge(peliharaan, pemain)
        cek_dan_terapkan_evolusi(peliharaan, pemain, riwayat, graph_evolusi)

        periode_kini = siklus_waktu.periode_sekarang()
        tampilkan_status(peliharaan, pemain, periode_kini.nama_periode)

        pilihan = tampilkan_menu_utama()

        if pilihan == "1":
            tampilkan_menu_toko(peliharaan, pemain, riwayat)
        elif pilihan == "2":
            tampilkan_menu_minigame(peliharaan, pemain, riwayat)
        elif pilihan == "3":
            tampilkan_riwayat(riwayat)
        elif pilihan == "4":
            tampilkan_info_pemain(pemain, peliharaan, graph_evolusi, pohon_evolusi)
        elif pilihan == "5":
            tampilkan_riwayat_makanan(peliharaan)
        elif pilihan == "6":
            tampilkan_navigasi_histori(peliharaan)
        elif pilihan == "7":
            tampilkan_leaderboard(peliharaan)
        elif pilihan == "8":
            tampilkan_pencarian_item()
        elif pilihan == "9":
            tampilkan_pencarian_pet_usia(peliharaan)
        elif pilihan in ("U", "u"):
            aksi = riwayat.pop()
            if aksi:
                print(f"  ↩️  Aksi dihapus dari riwayat: '{aksi}'")
                print("  (Catatan: perubahan stat tidak di-rollback)")
            else:
                print("  Tidak ada aksi untuk di-undo.")
        elif pilihan == "0":
            simpan_game(peliharaan, pemain, riwayat.ke_list())
            print(f"\n  Sampai jumpa! Jaga {peliharaan.nama} baik-baik ya. 👋")
            return False
        else:
            print("  Pilihan tidak valid.")


def jalankan_game():
    siklus_waktu = SiklusWaktu()
    pohon_evolusi = PohonEvolusi()
    graph_evolusi = GraphEvolusi()
    graph_evolusi.bangun_graph()

    while True:
        sessi = muat_atau_buat_sessi(siklus_waktu)
        if sessi is None:
            break

        peliharaan, pemain, riwayat, hari_terakhir = sessi
        mau_baru = jalankan_loop_utama(
            peliharaan, pemain, riwayat,
            siklus_waktu, pohon_evolusi, graph_evolusi, hari_terakhir,
        )

        if not mau_baru:
            break

        hapus_save()
        print("\n  Save lama dihapus. Memulai petualangan baru...\n")


if __name__ == "__main__":
    jalankan_game()
