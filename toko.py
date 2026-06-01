from peliharaan import Peliharaan
from pemain    import Pemain
from strukturdata import Stack
from datetime import datetime


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


def beli_item(id_item: str, peliharaan: Peliharaan, pemain: Pemain, riwayat: Stack) -> bool:
    """Langsung beli dan pakai item (untuk checkout atau beli langsung)."""
    item = DAFTAR_ITEM.get(id_item.upper())
    if item is None:
        print("  ⚠️  ID item tidak dikenali.")
        return False

    if not pemain.kurangi_koin(item["harga"]):
        return False

    nama_item = item["nama"]
    if item["kategori"] == "makanan":
        peliharaan.kelaparan = min(100.0, peliharaan.kelaparan + item["pulihkan_lapar"])
        peliharaan.berat     = min(99.9, peliharaan.berat + item["tambah_berat"])
        if "bonus_senang" in item:
            peliharaan.kesenangan = min(100.0, peliharaan.kesenangan + item["bonus_senang"])
        if "pulihkan_sehat" in item:
            peliharaan.kesehatan = min(100.0, peliharaan.kesehatan + item["pulihkan_sehat"])
        waktu_str = datetime.now().strftime("%d/%m %H:%M")
        peliharaan.riwayat_makanan.tambah(nama_item, waktu_str)
        print(f"  🍖 {peliharaan.nama} memakan {nama_item}. Kelaparan: {peliharaan.kelaparan:.1f}")
    elif item["kategori"] == "mainan":
        if peliharaan.energi < item["kurangi_energi"]:
            print(f"  😴 {peliharaan.nama} terlalu lelah untuk main!")
            pemain.tambah_koin(item["harga"])
            return False
        peliharaan.energi = max(0.0, peliharaan.energi - item["kurangi_energi"])
        peliharaan.kesenangan = min(100.0, peliharaan.kesenangan + item["tambah_senang"])
        print(f"  🎾 {peliharaan.nama} bermain dengan {nama_item}. Kesenangan: {peliharaan.kesenangan:.1f}")

    riwayat.push(f"Beli & pakai '{nama_item}' seharga {item['harga']} koin")
    return True


def tambah_ke_keranjang(pemain: Pemain):
    """Enqueue item ID ke keranjang pemain."""
    print("\n  Masukkan ID item untuk ditambahkan ke keranjang:")
    id_item = input("  > ").strip().upper()
    if id_item not in DAFTAR_ITEM:
        print("  ID tidak valid.")
        return
    pemain.keranjang.enqueue(id_item)
    print(f"  ✅ {DAFTAR_ITEM[id_item]['nama']} ditambahkan ke keranjang.")


def lihat_keranjang(pemain: Pemain):
    """Tampilkan isi keranjang (urutan FIFO)."""
    print("\n  🛒 ISI KERANJANG (urutan belanja):")
    items = pemain.keranjang.ke_list()
    if not items:
        print("  Keranjang kosong.")
        return
    for idx, id_item in enumerate(items, 1):
        item = DAFTAR_ITEM.get(id_item)
        if item:
            print(f"    {idx}. {item['nama']} - {item['harga']}🪙")
        else:
            print(f"    {idx}. {id_item} (tidak dikenal)")


def checkout(peliharaan: Peliharaan, pemain: Pemain, riwayat: Stack):
    """Proses semua item dalam keranjang secara FIFO."""
    if pemain.keranjang.kosong():
        print("  Keranjang kosong. Tidak ada yang di-checkout.")
        return

    print("\n  🧾 PROSES CHECKOUT (FIFO):")
    total_biaya = 0
    item_ids = pemain.keranjang.ke_list()
    for id_item in item_ids:
        item = DAFTAR_ITEM.get(id_item)
        if item:
            total_biaya += item["harga"]
    if pemain.koin < total_biaya:
        print(f"  ❌ Gagal checkout. Butuh {total_biaya} koin, kamu punya {pemain.koin}.")
        return

    # Proses satu per satu (dequeue)
    while not pemain.keranjang.kosong():
        id_item = pemain.keranjang.dequeue()
        beli_item(id_item, peliharaan, pemain, riwayat)
    print("  ✅ Checkout selesai. Keranjang sekarang kosong.")


def tampilkan_menu_toko(peliharaan: Peliharaan, pemain: Pemain, riwayat: Stack):
    """Loop menu toko dengan opsi keranjang."""
    while True:
        tampilkan_toko()
        print(f"\n  Koin kamu: {pemain.koin} 🪙")
        print("  OPSI:")
        print("  [1] Beli langsung (masukkan ID)")
        print("  [2] Tambah ke keranjang")
        print("  [3] Lihat keranjang")
        print("  [4] Checkout (proses semua item di keranjang)")
        print("  [0] Kembali")
        pilihan = input("  > ").strip()

        if pilihan == "0":
            break
        elif pilihan == "1":
            id_item = input("  Masukkan ID item: ").strip()
            beli_item(id_item, peliharaan, pemain, riwayat)
        elif pilihan == "2":
            tambah_ke_keranjang(pemain)
        elif pilihan == "3":
            lihat_keranjang(pemain)
        elif pilihan == "4":
            checkout(peliharaan, pemain, riwayat)
        else:
            print("  Pilihan tidak valid.")

        input("\n  Tekan Enter untuk melanjutkan...")
