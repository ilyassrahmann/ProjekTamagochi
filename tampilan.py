import os
from peliharaan import Peliharaan
from pemain    import Pemain

def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def bilah_progres(nilai, maks=100.0, panjang=12) -> str:
    """Render progress bar teks. Contoh: ████████░░░░"""
    nilai   = max(0.0, min(maks, nilai))
    terisi  = int((nilai / maks) * panjang)
    kosong  = panjang - terisi
    return "█" * terisi + "░" * kosong


def warna_status(nilai: float) -> str:
    """Kembalikan emoji indikator berdasarkan nilai 0-100."""
    if nilai >= 70:
        return "🟢"
    elif nilai >= 35:
        return "🟡"
    else:
        return "🔴"

ASCII_PET = {
    "Slime": [
        "  .-~~~-. ",
        " (  o  o ) ",
        "  \\ ^ ^ / ",
        "   '~~~~~' ",
    ],
    "Kucing": [
        " /\\   /\\  ",
        "(  o o  ) ",
        " =( Y )=  ",
        "  )   (   ",
    ],
    "Anjing": [
        "  / \\___/ ",
        " (  o   o)",
        "  \\  W  / ",
        "   \\_U_/  ",
    ],
}

def render_ascii_pet(spesies: str, tahap: str) -> list:
    """Kembalikan list baris ASCII art. Fallback ke Slime kalau spesies tidak diketahui."""
    seni = ASCII_PET.get(spesies, ASCII_PET["Slime"])
    if tahap == "Telur":
        return [
            "   _____  ",
            "  /     \\ ",
            " |  🥚   |",
            "  \\_____/ ",
        ]
    return seni

def tampilkan_status(peliharaan: Peliharaan, pemain: Pemain, nama_periode: str):
    bersihkan_layar()
    seni = render_ascii_pet(peliharaan.spesies, peliharaan.tahap_evolusi)

    print("╔" + "═"*48 + "╗")
    print("║" + "  🐾  TAMAGOTCHI CLI".center(48) + "║")
    print("╠" + "═"*48 + "╣")

    for baris in seni:
        print("║" + f"  {baris:<46}" + "║")

    print("╠" + "═"*48 + "╣")
    print(f"║  Nama     : {peliharaan.nama:<35}║")
    print(f"║  Spesies  : {peliharaan.spesies:<35}║")
    print(f"║  Evolusi  : {peliharaan.tahap_evolusi:<35}║")
    print(f"║  Usia     : {peliharaan.usia:.1f} hari{'':<29}║")
    print(f"║  Periode  : {nama_periode:<35}║")
    print("╠" + "═"*48 + "╣")

    stats = [
        ("🍖 Lapar   ", peliharaan.kelaparan, peliharaan.status_kelaparan()),
        ("😊 Senang  ", peliharaan.kesenangan, peliharaan.status_mood()),
        ("❤️  Sehat  ", peliharaan.kesehatan,  peliharaan.status_kesehatan()),
        ("⚡ Energi  ", peliharaan.energi,     f"{peliharaan.energi:.0f}"),
    ]

    for label, nilai, teks_status in stats:
        bilah = bilah_progres(nilai)
        indik = warna_status(nilai)
        print(f"║  {label}: {bilah} {indik} {teks_status:<8}║")

    print("╠" + "═"*48 + "╣")
    print(f"║  💰 Koin : {pemain.koin:<37}║")
    print("╚" + "═"*48 + "╝")

def tampilkan_menu_utama():
    print("\n" + "─"*50)
    print("  [1] Beri Makan / Gunakan Item  (Toko)")
    print("  [2] Main Minigame              (Cari Koin)")
    print("  [3] Lihat Riwayat Aksi")
    print("  [4] Info & Badge")
    print("  [0] Simpan & Keluar")
    print("─"*50)
    return input("  Pilih menu: ").strip()

def tampilkan_riwayat(riwayat_aksi: list):
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  📜  RIWAYAT AKSI".center(48) + "║")
    print("╠" + "═"*48 + "╣")
    if not riwayat_aksi:
        print("║" + "  Belum ada aksi.".ljust(48) + "║")
    else:
        for i, aksi in enumerate(reversed(riwayat_aksi[-10:]), 1):
            baris = f"  {i:>2}. {aksi}"
            print("║" + baris[:48].ljust(48) + "║")
    print("╚" + "═"*48 + "╝")
    input("\n  Tekan Enter untuk kembali...")


def tampilkan_info_pemain(pemain: Pemain, peliharaan: Peliharaan):
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  👤  INFO PEMAIN".center(48) + "║")
    print("╠" + "═"*48 + "╣")
    print(f"║  Nama pemain  : {pemain.nama_pemain:<31}║")
    print(f"║  Total koin   : {pemain.koin:<31}║")
    print(f"║  Hari bertahan: {pemain.total_hari_hidup:<31}║")
    print("╠" + "═"*48 + "╣")
    print("║" + "  🏅  Badge".ljust(48) + "║")
    if pemain.daftar_badge:
        for badge in sorted(pemain.daftar_badge):
            print("║" + f"    • {badge}".ljust(48) + "║")
    else:
        print("║" + "    Belum ada badge.".ljust(48) + "║")
    print("╚" + "═"*48 + "╝")
    input("\n  Tekan Enter untuk kembali...")


def tampilkan_layar_kematian(peliharaan: Peliharaan, pemain: Pemain):
    bersihkan_layar()
    print("\n" + "="*48)
    print("  💀  PELIHARAAN MENINGGAL")
    print("="*48)
    print(f"\n  {peliharaan.nama} ({peliharaan.spesies}) telah pergi...")
    print(f"  Usia terakhir : {peliharaan.usia:.1f} hari")
    print(f"  Koin tersisa  : {pemain.koin}")
    print(f"\n  Terima kasih sudah merawat {peliharaan.nama}.")
    print("\n  Game akan ditutup. Data terakhir disimpan.")
    print("="*48 + "\n")


def tampilkan_layar_sambutan():
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  🐾  SELAMAT DATANG DI TAMAGOTCHI CLI".center(48) + "║")
    print("╚" + "═"*48 + "╝")


def pilih_spesies() -> str:
    spesies_tersedia = list(ASCII_PET.keys())
    print("\n  Pilih spesies peliharaan:")
    for i, sp in enumerate(spesies_tersedia, 1):
        print(f"  [{i}] {sp}")
    while True:
        try:
            pilihan = int(input("  > "))
            if 1 <= pilihan <= len(spesies_tersedia):
                return spesies_tersedia[pilihan - 1]
        except ValueError:
            pass
        print("  Pilihan tidak valid.")
