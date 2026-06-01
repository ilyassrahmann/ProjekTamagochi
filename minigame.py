import random
from peliharaan import Peliharaan
from pemain    import Pemain
from strukturdata import Stack

BIAYA_ENERGI_GAME = 20.0
PENURUNAN_BERAT_GAME = 0.3


def _cek_energi(peliharaan: Peliharaan) -> bool:
    """Cek apakah peliharaan punya energi cukup untuk main."""
    if peliharaan.energi < BIAYA_ENERGI_GAME:
        print(f"\n  😴 {peliharaan.nama} terlalu lelah untuk main! "
              f"(Energi: {peliharaan.energi:.1f})")
        print("  Biarkan peliharaan istirahat atau beli mainan ringan dulu.")
        return False
    return True


def _selesai_main(peliharaan: Peliharaan, pemain: Pemain,
                  koin_menang: int, riwayat_aksi: Stack, nama_game: str):
    """Terapkan hasil game: kurangi energi, tambah koin, catat riwayat."""
    peliharaan.energi     = max(0.0, peliharaan.energi - BIAYA_ENERGI_GAME)
    peliharaan.kesenangan = min(100.0, peliharaan.kesenangan + 5.0)
    peliharaan.berat      = max(3.0, peliharaan.berat - PENURUNAN_BERAT_GAME)
    pemain.tambah_koin(koin_menang)
    riwayat_aksi.push(f"Main '{nama_game}', menang {koin_menang} koin")
    print(f"  ⚡ Energi {peliharaan.nama}: {peliharaan.energi:.1f}  |  "
          f"Berat: {peliharaan.berat:.1f}")

def game_tebak_angka(peliharaan: Peliharaan, pemain: Pemain,
                     riwayat_aksi: Stack):
    """
    Tebak angka 1-20 dalam 5 kesempatan.
    Makin sedikit tebakan, makin banyak koin.
    """
    if not _cek_energi(peliharaan):
        return

    print("\n" + "="*44)
    print("  🔢  TEBAK ANGKA")
    print("="*44)
    print("  Tebak angka antara 1 sampai 20.")
    print("  Makin sedikit tebakan = makin banyak koin!")
    print("-"*44)

    angka_rahasia = random.randint(1, 20)
    maks_tebak    = 5
    koin_menang   = 0
    percobaan     = 0
    menang        = False

    while percobaan < maks_tebak and not menang:
        percobaan += 1
        try:
            tebak = int(input(f"  Tebakan ke-{percobaan}: "))
        except ValueError:
            print("  Masukkan angka yang valid! (tidak dihitung sebagai tebakan)")
            percobaan -= 1
            continue

        if tebak == angka_rahasia:
            koin_menang = max(10, 50 - (percobaan - 1) * 10)
            print(f"\n  🎉 Benar! Angkanya memang {angka_rahasia}.")
            menang = True
        elif tebak < angka_rahasia:
            print("  📈 Terlalu kecil!")
        else:
            print("  📉 Terlalu besar!")

    if not menang:
        print(f"\n  😅 Kehabisan kesempatan! Angkanya adalah {angka_rahasia}.")
        koin_menang = 5

    _selesai_main(peliharaan, pemain, koin_menang, riwayat_aksi, "Tebak Angka")

PILIHAN_SUIT = {"1": "Batu", "2": "Gunting", "3": "Kertas"}
MENANG_LAWAN = {
    "Batu"   : "Gunting",
    "Gunting": "Kertas",
    "Kertas" : "Batu",
}

def game_suit(peliharaan: Peliharaan, pemain: Pemain, riwayat_aksi: Stack):
    if not _cek_energi(peliharaan):
        return

    print("\n" + "="*44)
    print(f"  ✊  SUIT MELAWAN {peliharaan.nama.upper()}")
    print("="*44)
    print("  Menangkan 2 dari 3 ronde untuk jackpot!")
    print("-"*44)

    menang_pemain = 0
    menang_pet    = 0

    for ronde in range(1, 4):
        print(f"\n  Ronde {ronde}:")
        print("  [1] Batu  [2] Gunting  [3] Kertas")
        pilihan_input = input("  Pilihanmu: ").strip()

        if pilihan_input not in PILIHAN_SUIT:
            print("  Pilihan tidak valid, ronde dilewati.")
            continue

        pilihan_pemain = PILIHAN_SUIT[pilihan_input]
        pilihan_pet    = random.choice(list(PILIHAN_SUIT.values()))

        print(f"  Kamu  : {pilihan_pemain}")
        print(f"  {peliharaan.nama:<10}: {pilihan_pet}")

        if pilihan_pemain == pilihan_pet:
            print("  🤝 Seri!")
        elif MENANG_LAWAN[pilihan_pemain] == pilihan_pet:
            print("  ✅ Kamu menang ronde ini!")
            menang_pemain += 1
        else:
            print(f"  ❌ {peliharaan.nama} menang ronde ini!")
            menang_pet += 1

    print(f"\n  Hasil akhir: Kamu {menang_pemain} - {menang_pet} {peliharaan.nama}")

    if menang_pemain > menang_pet:
        koin_menang = 40
        print("  🏆 Kamu menang! Peliharaanmu terkesan.")
    elif menang_pemain == menang_pet:
        koin_menang = 15
        print("  🤝 Seri! Lumayan.")
    else:
        koin_menang = 5
        print(f"  😔 Kalah dari peliharaan sendiri... setidaknya ada hadiah hiburan.")

    _selesai_main(peliharaan, pemain, koin_menang, riwayat_aksi, "Suit")

def tampilkan_menu_minigame(peliharaan: Peliharaan, pemain: Pemain,
                             riwayat_aksi: Stack):
    while True:
        print("\n" + "="*44)
        print("  🎮  MINIGAME")
        print("="*44)
        print(f"  Energi {peliharaan.nama}: {peliharaan.energi:.1f} "
              f"(butuh {BIAYA_ENERGI_GAME:.0f} per game)")
        print(f"  Koin kamu: {pemain.koin} 🪙")
        print("-"*44)
        print("  [1] Tebak Angka  (maks 50 koin)")
        print("  [2] Suit         (maks 40 koin)")
        print("  [0] Kembali")
        print("="*44)

        pilihan = input("  Pilih game: ").strip()

        if pilihan == "1":
            game_tebak_angka(peliharaan, pemain, riwayat_aksi)
        elif pilihan == "2":
            game_suit(peliharaan, pemain, riwayat_aksi)
        elif pilihan == "0":
            break
        else:
            print("  Pilihan tidak valid.")

        input("\n  Tekan Enter untuk melanjutkan...")
