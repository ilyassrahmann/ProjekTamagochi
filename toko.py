from peliharaan import Peliharaan
from pemain    import Pemain


DAFTAR_ITEM = {
    "M001": {
        "nama"            : "Kibble Biasa",
        "kategori"        : "makanan",
        "harga"           : 10,
        "pulihkan_lapar"  : 20.0,
        "tambah_berat"    : 0.5,
        "deskripsi"       : "Makanan sehari-hari. Murah dan mengenyangkan.",
    },
    "M002": {
        "nama"            : "Makanan Mewah",
        "kategori"        : "makanan",
        "harga"           : 35,
        "pulihkan_lapar"  : 50.0,
        "tambah_berat"    : 1.5,
        "deskripsi"       : "Makanan premium. Peliharaan jadi lebih bahagia!",
        "bonus_senang"    : 10.0,
    },
    "M003": {
        "nama"            : "Camilan Diet",
        "kategori"        : "makanan",
        "harga"           : 20,
        "pulihkan_lapar"  : 25.0,
        "tambah_berat"    : 0.1,
        "deskripsi"       : "Rendah kalori. Cocok kalau berat badan sudah tinggi.",
    },
    "M004": {
        "nama"            : "Obat",
        "kategori"        : "makanan",
        "harga"           : 40,
        "pulihkan_lapar"  : 5.0,
        "tambah_berat"    : 0.0,
        "pulihkan_sehat"  : 30.0,
        "deskripsi"       : "Memulihkan kesehatan saat peliharaan sakit.",
    },

    "T001": {
        "nama"            : "Bola Karet",
        "kategori"        : "mainan",
        "harga"           : 15,
        "tambah_senang"   : 20.0,
        "kurangi_energi"  : 15.0,
        "deskripsi"       : "Mainan simpel. Peliharaan suka menggelindingkannya.",
    },
    "T002": {
        "nama"            : "Puzzle Kayu",
        "kategori"        : "mainan",
        "harga"           : 30,
        "tambah_senang"   : 40.0,
        "kurangi_energi"  : 25.0,
        "deskripsi"       : "Mainan seru tapi melelahkan. Kesenangan naik banyak.",
    },
}


def tampilkan_toko():
    print("\n" + "="*52)
    print("  🛒  TOKO")
    print("="*52)
    print(f"  {'ID':<6} {'Nama':<20} {'Harga':>6}  Keterangan")
    print("-"*52)

    for id_item, item in DAFTAR_ITEM.items():
        print(f"  {id_item:<6} {item['nama']:<20} {item['harga']:>5}🪙  {item['deskripsi']}")

    print("="*52)


def beli_item(id_item: str, peliharaan: Peliharaan, pemain: Pemain,
              riwayat_aksi: list) -> bool:
    """
    Cari item di hash table, kurangi koin pemain, terapkan efek ke peliharaan.
    Kembalikan True kalau berhasil.
    """

    item = DAFTAR_ITEM.get(id_item.upper())

    if item is None:
        print("  ⚠️  ID item tidak dikenali.")
        return False

    if not pemain.kurangi_koin(item["harga"]):
        return False

    nama_item = item["nama"]
    if item["kategori"] == "makanan":
        peliharaan.kelaparan = min(100.0, peliharaan.kelaparan + item["pulihkan_lapar"])
        peliharaan.berat    += item["tambah_berat"]
        if "bonus_senang" in item:
            peliharaan.kesenangan = min(100.0, peliharaan.kesenangan + item["bonus_senang"])
        if "pulihkan_sehat" in item:
            peliharaan.kesehatan  = min(100.0, peliharaan.kesehatan  + item["pulihkan_sehat"])
        print(f"  🍖 {peliharaan.nama} memakan {nama_item}. "
              f"Kelaparan: {peliharaan.kelaparan:.1f}")

    elif item["kategori"] == "mainan":
        if peliharaan.energi < item["kurangi_energi"]:
            print(f"  😴 {peliharaan.nama} terlalu lelah untuk main!")
            pemain.tambah_koin(item["harga"])  # kembalikan koin
            return False
        peliharaan.energi     = max(0.0, peliharaan.energi - item["kurangi_energi"])
        peliharaan.kesenangan = min(100.0, peliharaan.kesenangan + item["tambah_senang"])
        print(f"  🎾 {peliharaan.nama} bermain dengan {nama_item}. "
              f"Kesenangan: {peliharaan.kesenangan:.1f}")

    riwayat_aksi.append(f"Beli & pakai '{nama_item}' seharga {item['harga']} koin")
    return True


def tampilkan_menu_toko(peliharaan: Peliharaan, pemain: Pemain,
                        riwayat_aksi: list):
    """Loop menu toko yang dipanggil dari main menu."""
    while True:
        tampilkan_toko()
        print(f"\n  Koin kamu: {pemain.koin} 🪙")
        print("  Masukkan ID item untuk membeli, atau '0' untuk kembali:")
        pilihan = input("  > ").strip()

        if pilihan == "0":
            break

        beli_item(pilihan, peliharaan, pemain, riwayat_aksi)
        input("\n  Tekan Enter untuk melanjutkan...")
