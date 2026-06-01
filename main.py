from peliharaan   import Peliharaan
from pemain       import Pemain
from waktu        import SiklusWaktu, hitung_pembusukan
from penyimpanan  import simpan_game, muat_game
from toko         import tampilkan_menu_toko
from minigame     import tampilkan_menu_minigame
from strukturdata import Stack
from tampilan     import (
    tampilkan_status,
    tampilkan_menu_utama,
    tampilkan_riwayat,
    tampilkan_info_pemain,
    tampilkan_layar_kematian,
    tampilkan_layar_sambutan,
    pilih_spesies,
)

def mulai_game_baru() -> tuple:
    tampilkan_layar_sambutan()
    print("\n  Tidak ada save ditemukan. Mari mulai petualangan baru!\n")

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

def cek_badge(peliharaan: Peliharaan, pemain: Pemain):
    """Cek kondisi badge dan berikan kalau belum dimiliki."""
    if peliharaan.usia >= 7 and "Bertahan 7 Hari" not in pemain.daftar_badge:
        pemain.tambah_badge("Bertahan 7 Hari")
    if peliharaan.usia >= 30 and "Veteran Sebulan" not in pemain.daftar_badge:
        pemain.tambah_badge("Veteran Sebulan")
    if pemain.koin >= 200 and "Juragan Koin" not in pemain.daftar_badge:
        pemain.tambah_badge("Juragan Koin")
    if peliharaan.kesehatan >= 95 and "Selalu Sehat" not in pemain.daftar_badge:
        pemain.tambah_badge("Selalu Sehat")

def jalankan_game():
    siklus_waktu = SiklusWaktu()

    hasil_muat = muat_game()
    if hasil_muat:
        peliharaan, pemain, riwayat_list = hasil_muat
        riwayat = Stack()
        for aksi in riwayat_list:
            riwayat.push(aksi)
        tampilkan_layar_sambutan()
        print(f"\n  Selamat datang kembali, {pemain.nama_pemain}!")
        print(f"  {peliharaan.nama} merindukanmu...\n")
        hitung_pembusukan(peliharaan, siklus_waktu)
        input("\n  Tekan Enter untuk melanjutkan...")
    else:
        peliharaan, pemain, riwayat = mulai_game_baru()

    while True:
        if not peliharaan.masih_hidup:
            simpan_game(peliharaan, pemain, riwayat.ke_list())
            tampilkan_layar_kematian(peliharaan, pemain)
            break

        cek_badge(peliharaan, pemain)

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
            tampilkan_info_pemain(pemain, peliharaan)
        elif pilihan == "0":
            simpan_game(peliharaan, pemain, riwayat.ke_list())
            print(f"\n  Sampai jumpa! Jaga {peliharaan.nama} baik-baik ya. 👋")
            break
        else:
            print("  Pilihan tidak valid.")

if __name__ == "__main__":
    jalankan_game()
