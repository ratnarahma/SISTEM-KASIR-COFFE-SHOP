import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

# Fungsi untuk membaca menu dari Excel
def baca_menu(nama_file='menu.xlsx'):
    try:
        df = pd.read_excel(nama_file)
        menu = {row['id']: {'jenis': row['nama'], 'harga': row['harga']} for _, row in df.iterrows()}
        return menu
    except FileNotFoundError:
        print("File menu.xlsx tidak ditemukan. Pastikan file menu tersedia.")
        exit()

# Fungsi untuk menyimpan data transaksi ke file Excel
def simpan_ke_excel(data, nama_file='transaksi.xlsx'):
    from openpyxl.utils.dataframe import dataframe_to_rows

    try:
        book = load_workbook(nama_file)
        sheet = book.active
    except FileNotFoundError:
        from openpyxl import Workbook
        book = Workbook()
        sheet = book.active
        sheet.title = "Sheet1"

    df = pd.DataFrame(data)
    startrow = sheet.max_row + 1 if sheet.max_row > 1 else 1

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=startrow == 1), start=startrow):
        for c_idx, value in enumerate(row, start=1):
            sheet.cell(row=r_idx, column=c_idx, value=value)

    book.save(nama_file)

# Fungsi untuk menampilkan garis
def garis():
    print("=" * 90)

# Fungsi untuk menampilkan menu dan meminta nama barista serta pembeli
def display_menu(menu):
    print("=> C O F F E E   S H O P   J A Y A <=".center(90))
    print("Jl. Slamet Riyadi no.11".center(90))
    print("Kota Surakarta, Jawa Tengah - 17610".center(90))
    print("contact person : 08123456789".center(90))
    garis()
    print("Kami Memberikan Diskon 10% Minimal Belanja 100rb".center(90))
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(90))
    garis()

    n_barista = input("Nama barista: ")
    n_pembeli = input("Nama pembeli: ")

    garis()
    print("Menu yang Tersedia:")
    for key, value in menu.items():
        print(f"{key:<3}. {value['jenis']:<20} Rp.{value['harga']:>8,}")
    garis()
    return n_barista, n_pembeli

# Fungsi utama untuk mengelola pesanan
def main():
    menu = baca_menu()

    listjenis = []
    listharga = []
    listjb = []
    listtotbel = []
    listicehot = []

    totalbelanja = 0
    totalsemua = 0

    n_barista, n_pembeli = display_menu(menu)

    while True:
        try:
            a = int(input("Berapa menu pemesanan yang anda inginkan: "))
            break
        except ValueError:
            print("Masukkan dengan angka!")

    for i in range(a):
        while True:
            try:
                print(f"Jenis Menu Ke-{i + 1}")
                pilihan = int(input("Pilihan: "))
                if pilihan not in menu:
                    print("Masukkan angka sesuai pada nomor menu.")
                else:
                    break
            except ValueError:
                print("Masukkan angka sesuai pada nomor menu.")

        while True:
            try:
                jb = int(input("Jumlah beli: "))
                break
            except ValueError:
                print("Masukkan jumlah beli dengan angka!")

        while True:
            icehot = input("Pilihan penyajian [Ice/Hot]: ").strip().capitalize()
            if icehot not in ["Ice", "Hot"]:
                print("Masukkan pilihan minuman Ice/Hot!")
            else:
                break

        jenis = menu[pilihan]["jenis"]
        harga = menu[pilihan]["harga"]

        listjenis.append(jenis)
        listharga.append(harga)
        listjb.append(jb)
        listicehot.append(icehot)

        total_bayar = jb * harga
        listtotbel.append(total_bayar)

    print("\n" + "=> Rincian Pesanan Anda <=".center(90))
    garis()
    print(f"{'No.':<4} {'Jenis':<20} {'Harga':<10} {'Jumlah Beli':<15} {'Total Bayar':<15} {'Penyajian':<10}")
    print("-" * 90)

    for i in range(a):
        print(
            f"{i + 1:<4} {listjenis[i]:<20} Rp.{listharga[i]:<8,} {listjb[i]:<15} Rp.{listtotbel[i]:<13,} {listicehot[i]:<10}"
        )
        totalbelanja += listjb[i]
        totalsemua += listtotbel[i]

    garis()
    print(f"{'Total belanja':<40} = {totalbelanja} item")
    print(f"{'Total harga semuanya':<40} = Rp. {totalsemua:,}")
    diskon = totalsemua * 0.10 if totalsemua >= 100000 else 0
    harga_setelah_diskon = totalsemua - diskon
    print(f"{'Total Diskon 10%':<40} = Rp. {diskon:,}")
    print(f"{'Harga bayar menjadi':<40} = Rp. {harga_setelah_diskon:,}")

    garis()

    while True:
        try:
            bayar = int(input(f"{'Masukkan jumlah uang yang dibayar':<40} = Rp. ").strip().replace(",", ""))
            if bayar < harga_setelah_diskon:
                print("Jumlah uang yang diinputkan kurang dari harga bayar. Silakan input ulang.")
            else:
                break
        except ValueError:
            print("Masukkan jumlah uang dengan angka!")

    kembali = bayar - harga_setelah_diskon
    print(f"{'Uang kembali anda':<40} = Rp. {kembali:,}")

    garis()
    print("Terima kasih, Selamat menikmati minuman anda :D")

    data = {
        "Nama Barista": [n_barista] * a,
        "Nama Pembeli": [n_pembeli] * a,
        "Jenis": listjenis,
        "Harga": listharga,
        "Jumlah Beli": listjb,
        "Penyajian": listicehot,
        "Total Bayar": listtotbel,
        "Tanggal": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * a,
    }
    simpan_ke_excel(data)

if __name__ == "__main__":
    main()