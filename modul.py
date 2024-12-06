import os
from openpyxl import load_workbook
from tkinter import messagebox

# Harga menu
menu_prices = {
    'Espresso': 12000,
    'Americano': 15000,
    'Cappucino': 20000,
    'Mochacino': 20000,
    'Caramel Macchiato': 20000,
    'Vanilla Latte': 20000,
    'Hazelnut Latte': 20000,
    'Caffe Latte': 20000,
    'Chocolatte': 20000,
    'Matcha': 20000,
    'Taro': 20000,
    'Cookies & Cream': 20000,
    'Jasmine Tea': 12000,
    'Original Tea': 10000,
    'Lemon Tea': 13000,
    'Lychee Tea': 17000,
    'Strawberry Tea': 15000
}

# Nama file Excel
excel_file = "rekapan_pesanan.xlsx"

# Buat file Excel jika belum ada
def create_excel_file():
    if not os.path.exists(excel_file):
        try:
            wb = load_workbook(excel_file)
            ws = wb.active
            ws.title = "Data Pembelian"
            ws.append(["Nama Barista", "Nama Pembeli", "Menu", "Total Harga", "Diskon", "Harga Bayar", "Uang Pembayaran", "Uang Kembali"])
            wb.save(excel_file)
        except Exception as e:
            print(f"Error creating Excel file: {e}")

# Fungsi untuk menyimpan data ke dalam Excel
def save_to_excel(barista, pembeli, menu, total_harga, diskon, harga_bayar, uang_pembayaran, uang_kembali):
    try:
        wb = load_workbook(excel_file)
        ws = wb.active
        ws.append([barista, pembeli, str(menu), total_harga, diskon, harga_bayar, uang_pembayaran, uang_kembali])
        wb.save(excel_file)
    except Exception as e:
        raise Exception(f"Error saving to Excel file: {e}")

# Fungsi untuk menghitung total harga dan diskon
def calculate_total(menu, menu_prices):
    total_harga = sum(menu_prices[menu] * jumlah for menu, (jumlah, _, _) in menu.items())
    diskon = 0
    if total_harga >= 100000:
        diskon = total_harga * 0.1
    harga_bayar = total_harga - diskon
    return total_harga, diskon, harga_bayar

# Fungsi untuk menghitung uang kembali
def calculate_change(uang_pembayaran, harga_bayar):
    if uang_pembayaran < harga_bayar:
        raise ValueError("Uang pembayaran kurang dari harga bayar.")
    return uang_pembayaran - harga_bayar