import os
from peliharaan import Peliharaan
from pemain    import Pemain
from strukturdata import Stack
from sorting import bubble_sort_peliharaan, bubble_sort_str
from searching import linear_search_item, binary_search_leaderboard

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
            "   _____   ",
            "  /     \\  ",
            " |   O   |  ",
            "  \\_____/  ",
        ]
    return seni

def tampilkan_status(peliharaan: Peliharaan, pemain: Pemain, nama_periode: str):
    bersihkan_layar()
    seni = render_ascii_pet(peliharaan.spesies, peliharaan.tahap_evolusi)

    print("╔" + "═"*48 + "╗")
    print("║" + "  🐾  TAMAGOTCHI CLI".center(47) + "║")
    print("╠" + "═"*48 + "╣")

    for baris in seni:
        print("║" + f"  {baris:<46}" + "║")

    print("╠" + "═"*48 + "╣")
    print(f"║  Nama     : {peliharaan.nama:<35}║")
    print(f"║  Spesies  : {peliharaan.spesies:<35}║")
    print(f"║  Evolusi  : {peliharaan.tahap_evolusi:<35}║")
    print(f"║  Usia     : {peliharaan.usia:.1f} hari{'':<27}║")
    print(f"║  Periode  : {nama_periode:<35}║")
    print("╠" + "═"*48 + "╣")

    stats = [
        ("🍖 Lapar   ", peliharaan.kelaparan, peliharaan.status_kelaparan()),
        ("😊 Senang  ", peliharaan.kesenangan, peliharaan.status_mood()),
        ("❤️  Sehat   ", peliharaan.kesehatan,  peliharaan.status_kesehatan()),
        ("⚡ Energi  ", peliharaan.energi,     f"{peliharaan.energi:.0f}"),
    ]

    for label, nilai, teks_status in stats:
        bilah = bilah_progres(nilai)
        indik = warna_status(nilai)
        print(f"║  {label}: {bilah} {indik} {teks_status:<17}║")

    skor = peliharaan.hitung_skor_kebugaran()
    kategori = peliharaan.kategori_skor()
    print("╠" + "═"*48 + "╣")
    print(f"║  🧮 Skor Kebugaran: {skor:.1f} / 100  ({kategori:<1})   ║")

    print("╠" + "═"*48 + "╣")
    print(f"║  💰 Koin : {pemain.koin:<36}║")
    print("╚" + "═"*48 + "╝")

def tampilkan_menu_utama():
    print("\n" + "─"*50)
    print("  [1] Beri Makan / Gunakan Item  (Toko)")
    print("  [2] Main Minigame              (Cari Koin)")
    print("  [3] Lihat Riwayat Aksi")
    print("  [4] Info & Badge")
    print("  [5] Riwayat Makanan")
    print("  [6] Histori Hari")
    print("  [7] Leaderboard")
    print("  [8] Cari Item di Toko")
    print("  [9] Cari Peliharaan menurut Usia")
    print("  [D] Percepat Waktu")
    print("  [0] Simpan & Keluar")
    print("─"*50)
    return input("  Pilih menu: ").strip()

def tampilkan_riwayat(riwayat: Stack):
    while True:
        bersihkan_layar()
        print("╔" + "═"*48 + "╗")
        print("║" + "  📜  RIWAYAT AKSI (Stack / log)".center(47) + "║")
        print("╠" + "═"*48 + "╣")
        daftar_aksi = riwayat.ke_list()
        if not daftar_aksi:
            print("║" + "  Belum ada aksi.".ljust(48) + "║")
        else:
            for i, aksi in enumerate(reversed(daftar_aksi[-10:]), 1):
                baris = f"  {i:>2}. {aksi}"
                print("║" + baris[:48].ljust(48) + "║")
        print("╠" + "═"*48 + "╣")
        print("║  [H] Hapus entri log terakhir  [0] Kembali".ljust(49) + "║")
        print("║" + "  (Hanya teks log; koin/stat tidak berubah)".ljust(48) + "║")
        print("╚" + "═"*48 + "╝")
        pilih = input("\n  > ").strip().upper()
        if pilih == "H":
            aksi = riwayat.pop()
            if aksi:
                print(f"\n  🗑️  Entri log dihapus: '{aksi}'")
                input("  Tekan Enter...")
            else:
                print("\n  Log kosong.")
                input("  Tekan Enter...")
        elif pilih == "0":
            break
        else:
            break


def tampilkan_info_pemain(pemain: Pemain, peliharaan: Peliharaan,
                         graph_evolusi=None, pohon_evolusi=None):
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  👤  INFO PEMAIN".center(47) + "║")
    print("╠" + "═"*48 + "╣")
    print(f"║  Nama pemain  : {pemain.nama_pemain:<31}║")
    print(f"║  Total koin   : {pemain.koin:<31}║")
    print(f"║  Hari bertahan: {pemain.total_hari_hidup:<31}║")
    print("╠" + "═"*48 + "╣")
    print("║" + "  🏅  Badge".ljust(47) + "║")
    if pemain.daftar_badge:
        for badge in bubble_sort_str(list(pemain.daftar_badge), "naik"):
            print("║" + f"    • {badge}".ljust(48) + "║")
    else:
        print("║" + "    Belum ada badge.".ljust(48) + "║")
    print("╚" + "═"*48 + "╝")

    if graph_evolusi:
        print(f"\n  🌱 Jalur evolusi dari '{peliharaan.tahap_evolusi}':")
        graph_evolusi.tampilkan_jalur(peliharaan.tahap_evolusi)
    if pohon_evolusi:
        print("\n  🌳 Pohon evolusi (Tree):")
        pohon_evolusi.tampilkan_pohon()

    input("\n  Tekan Enter untuk kembali...")


def konfirmasi_game_baru() -> bool:
    """Tanya pemain apakah ingin memulai game baru."""
    while True:
        pilih = input("  Mulai game baru? [Y/n]: ").strip().lower()
        if pilih in ("", "y", "ya"):
            return True
        if pilih in ("n", "tidak"):
            return False
        print("  Ketik Y untuk ya, atau n untuk keluar.")


def tampilkan_layar_kematian(peliharaan: Peliharaan, pemain: Pemain) -> bool:
    """
    Tampilkan layar kematian.
    Kembalikan True jika pemain ingin memulai game baru.
    """
    bersihkan_layar()
    print("\n" + "="*48)
    print("  💀  PELIHARAAN MENINGGAL")
    print("="*48)
    print(f"\n  {peliharaan.nama} ({peliharaan.spesies}) telah pergi...")
    print(f"  Tahap akhir : {peliharaan.tahap_evolusi} 👻")
    print(f"  Usia terakhir : {peliharaan.usia:.1f} hari")
    print(f"  Koin tersisa  : {pemain.koin}")
    print(f"\n  Terima kasih sudah merawat {peliharaan.nama}.")
    print("  Data terakhir sudah disimpan.")
    print("="*48 + "\n")
    return konfirmasi_game_baru()


def tampilkan_layar_sambutan():
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  🐾  SELAMAT DATANG DI TAMAGOTCHI CLI".center(47) + "║")
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

def tampilkan_riwayat_makanan(peliharaan: Peliharaan):
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  🍽️  RIWAYAT MAKANAN (Single Linked List)".center(49) + "║")
    print("╠" + "═"*48 + "╣")
    daftar = peliharaan.riwayat_makanan.ke_list()
    if not daftar:
        print("║" + "  Belum pernah memberi makan.".ljust(48) + "║")
    else:
        for i, item in enumerate(daftar[:10], 1):   # tampilkan 10 terbaru
            print("║" + f"  {i}. {item}".ljust(48) + "║")
    print("╚" + "═"*48 + "╝")
    input("\n  Tekan Enter untuk kembali...")

def tampilkan_navigasi_histori(peliharaan: Peliharaan):
    """Menu untuk navigasi Double Linked List histori hari."""
    while True:
        bersihkan_layar()
        hari_ke, snapshot = peliharaan.histori_hari.info_kursor()
        print("╔" + "═"*48 + "╗")
        print("║" + "  📅  HISTORI HARI (Double Linked List)".center(47) + "║")
        print("╠" + "═"*48 + "╣")
        if snapshot is None:
            print("║" + "  Belum ada histori hari.".ljust(48) + "║")
        else:
            print(f"║  Hari ke-{hari_ke}".ljust(48) + "║")
            print("║" + "  Statistik (saat dicatat):".ljust(48) + "║")
            usia_tampil = snapshot.get("usia", 0.0)
            print(f"║    Usia      : {usia_tampil:.1f} hari".ljust(48) + "║")
            print(f"║    Kelaparan : {snapshot.get('kelaparan', 0):.1f}".ljust(48) + "║")
            print(f"║    Kesenangan: {snapshot.get('kesenangan', 0):.1f}".ljust(48) + "║")
            print(f"║    Kesehatan : {snapshot.get('kesehatan', 0):.1f}".ljust(48) + "║")
            print(f"║    Berat     : {snapshot.get('berat', 0):.1f}".ljust(48) + "║")
            print(f"║    Energi    : {snapshot.get('energi', 0):.1f}".ljust(48) + "║")
            print(f"║    Evolusi   : {snapshot.get('tahap_evolusi', '?')}".ljust(48) + "║")
        print("╠" + "═"*48 + "╣")
        print("║  [A] Awal  [M] Mundur  [J] Maju".ljust(49) + "║")
        print("║  [AK] Akhir  [0] Kembali".ljust(49) + "║")
        print("╚" + "═"*48 + "╝")
        pilih = input("  > ").strip().upper()
        if pilih == "A":
            peliharaan.histori_hari.ke_awal()
        elif pilih == "M":
            peliharaan.histori_hari.mundur()
        elif pilih == "J":
            peliharaan.histori_hari.maju()
        elif pilih == "AK":
            peliharaan.histori_hari.ke_akhir()
        elif pilih == "0":
            break
        else:
            input("  Pilihan tidak valid. Tekan Enter...")

def tampilkan_leaderboard(peliharaan_sekarang: Peliharaan, semua_pet: list = None):
    """
    Tampilkan leaderboard menggunakan bubble sort.
    Karena game hanya punya satu peliharaan, kita tetap buat demo dengan 
    menampilkan peliharaan saat ini dan beberapa dummy.
    Untuk keperluan demo, kita buat list berisi peliharaan sekarang + dummy.
    """
    if semua_pet is None:
        dummy1 = Peliharaan("Rex", "Anjing")
        dummy1.usia = 12.5
        dummy1.kesehatan = 85.0
        dummy2 = Peliharaan("Luna", "Kucing")
        dummy2.usia = 5.2
        dummy2.kesehatan = 95.0
        dummy3 = Peliharaan("Slimey", "Slime")
        dummy3.usia = 20.0
        dummy3.kesehatan = 60.0
        semua_pet = [peliharaan_sekarang, dummy1, dummy2, dummy3]
    
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + "  🏆  LEADERBOARD (Bubble Sort)".center(47) + "║")
    print("╠" + "═"*48 + "╣")
    
    print("\n  Urutan berdasarkan usia (tertua ke termuda):")
    urut_usia = bubble_sort_peliharaan(semua_pet, "usia", "turun")
    for i, pet in enumerate(urut_usia, 1):
        print(f"    {i}. {pet.nama} ({pet.spesies}) - Usia: {pet.usia:.1f} hari")
    
    print("\n  Urutan berdasarkan kesehatan (tertinggi ke terendah):")
    urut_kesehatan = bubble_sort_peliharaan(semua_pet, "kesehatan", "turun")
    for i, pet in enumerate(urut_kesehatan, 1):
        print(f"    {i}. {pet.nama} ({pet.spesies}) - Kesehatan: {pet.kesehatan:.1f}")
    
    print("\n" + "╚" + "═"*48 + "╝")
    input("\n  Tekan Enter untuk kembali...")


def tampilkan_pencarian_item():
    """Menu linear search untuk mencari item di toko berdasarkan nama."""
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + " 🔍  CARI ITEM DI TOKO (Linear Search)".center(48) + "║")
    print("╚" + "═"*48 + "╝")
    kata = input("\n  Masukkan kata kunci nama item: ").strip()
    if not kata:
        print("  Kata kunci kosong.")
        input("\n  Tekan Enter...")
        return
    
    hasil = linear_search_item(kata)
    if not hasil:
        print(f"  Tidak ada item dengan nama mengandung '{kata}'.")
    else:
        print(f"\n  Ditemukan {len(hasil)} item:")
        for id_item, item in hasil:
            print(f"    {id_item}: {item['nama']} - {item['harga']}🪙")
    input("\n  Tekan Enter untuk kembali...")


def tampilkan_pencarian_pet_usia(peliharaan_sekarang: Peliharaan, semua_pet: list = None):
    """
    Binary search pada leaderboard yang sudah diurutkan berdasarkan usia (naik).
    Mencari pet dengan usia tertentu.
    """
    if semua_pet is None:
        dummy1 = Peliharaan("Rex", "Anjing")
        dummy1.usia = 12.5
        dummy2 = Peliharaan("Luna", "Kucing")
        dummy2.usia = 5.2
        dummy3 = Peliharaan("Slimey", "Slime")
        dummy3.usia = 20.0
        semua_pet = [peliharaan_sekarang, dummy1, dummy2, dummy3]

    # Urutkan berdasarkan usia (naik) untuk binary search
    urut_usia_naik = bubble_sort_peliharaan(semua_pet, "usia", "naik")
    
    bersihkan_layar()
    print("╔" + "═"*48 + "╗")
    print("║" + " 🔎  BINARY SEARCH PELIHARAAN BERDASARKAN USIA".center(47) + "║")
    print("╚" + "═"*48 + "╝")
    
    try:
        target = float(input("\n  Masukkan usia yang dicari (dalam hari): ").strip())
    except ValueError:
        print("  Masukkan angka yang valid.")
        input("\n  Tekan Enter...")
        return
    
    index = binary_search_leaderboard(urut_usia_naik, target)
    if index == -1:
        print(f"  Tidak ada peliharaan dengan usia {target:.1f} hari (toleransi ±0.01).")
    else:
        pet = urut_usia_naik[index]
        print(f"\n  Ditemukan pada urutan ke-{index+1}:")
        print(f"    Nama      : {pet.nama}")
        print(f"    Spesies   : {pet.spesies}")
        print(f"    Usia      : {pet.usia:.1f} hari")
        print(f"    Kesehatan : {pet.kesehatan:.1f}")
    input("\n  Tekan Enter untuk kembali...")

