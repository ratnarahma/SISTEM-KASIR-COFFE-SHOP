import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from modul import create_excel_file, save_to_excel, calculate_total, calculate_change, menu_prices

class KasirApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Kasir Coffee Shop")

        # Sesuaikan ukuran window dengan layar penuh
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state("zoomed")

        # Load background image
        self.bg_image = Image.open("bg.png")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.frame = tk.Frame(root, padx=20, pady=20, bg="#C9BCB3")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.font_default = ("Times New Roman", 14)
        self.font_small = ("Times New Roman", 10)
        self.barista = ""
        self.pembeli = ""
        self.menu = {}
        self.uang = 0

        # Create the Excel file if not already created
        create_excel_file()

        self.page1()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def page1(self):
        self.clear_frame()

        tk.Label(self.frame, text="Nama Barista", font=self.font_default, bg="#C9BCB3").grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.entry_barista = tk.Entry(self.frame, font=self.font_default)
        self.entry_barista.grid(row=0, column=1, padx=(0, 20))

        tk.Label(self.frame, text="Nama Pembeli", font=self.font_default, bg="#C9BCB3").grid(row=1, column=0, sticky="w", padx=(0, 20))
        self.entry_pembeli = tk.Entry(self.frame, font=self.font_default)
        self.entry_pembeli.grid(row=1, column=1, padx=(0, 20))

        tk.Button(self.frame, text="Next", font=self.font_default, command=self.page2).grid(row=2, columnspan=2, pady=10)

    def page2(self):
        self.barista = self.entry_barista.get()
        self.pembeli = self.entry_pembeli.get()

        if not self.barista or not self.pembeli:
            messagebox.showerror("Error", "Nama Barista dan Nama Pembeli harus diisi.")
            return

        self.clear_frame()

        # Menginisialisasi menu variabel dan entries
        self.menu_vars = {}
        self.menu_entries = {}
        self.menu_temp = {}
        self.menu_sugar = {}

        # Menampilkan menu
        for i, (menu, price) in enumerate(menu_prices.items()):
            var = tk.IntVar()
            self.menu_vars[menu] = var
            tk.Checkbutton(self.frame, text=f"{menu} - Rp {price}", variable=var, font=self.font_small, bg="#C9BCB3").grid(row=i+1, column=0, sticky="w")
            entry = tk.Entry(self.frame, font=self.font_small)
            entry.grid(row=i+1, column=1)
            self.menu_entries[menu] = entry

            temp_var = tk.StringVar(value="Ice")
            self.menu_temp[menu] = temp_var
            tk.OptionMenu(self.frame, temp_var, "Ice", "Hot").grid(row=i+1, column=2)

            sugar_var = tk.StringVar(value="Normal")
            self.menu_sugar[menu] = sugar_var
            tk.OptionMenu(self.frame, sugar_var, "Normal", "Less Sugar").grid(row=i+1, column=3)

        tk.Label(self.frame, text="Isi jumlah pesanan menggunakan angka!", fg="red", font=self.font_small, bg="#C9BCB3").grid(row=len(menu_prices)+1, column=1, sticky="w")
        tk.Button(self.frame, text="Next", font=self.font_small, command=self.page3).grid(row=len(menu_prices)+2, columnspan=4, pady=10)
        tk.Button(self.frame, text="Back", font=self.font_small, command=self.page1).grid(row=len(menu_prices)+3, columnspan=4, pady=10)
        
    def page3(self):
        self.menu = {}
        for menu, var in self.menu_vars.items():
            if var.get() == 1:
                try:
                    jumlah = int(self.menu_entries[menu].get())
                    if jumlah <= 0:
                        raise ValueError
                    temp = self.menu_temp[menu].get()
                    sugar = self.menu_sugar[menu].get()
                    self.menu[menu] = (jumlah, temp, sugar)
                except ValueError:
                    messagebox.showerror("Error", f"Jumlah untuk {menu} harus berupa angka positif.")
                    return

        if not self.menu:
            messagebox.showerror("Error", "Pilih setidaknya satu menu.")
            return

        self.clear_frame()
        total_harga, diskon, harga_bayar = calculate_total(self.menu, menu_prices)

        tk.Label(self.frame, text="Rincian Pesanan:", font=self.font_default, bg="#C9BCB3").grid(row=0, column=0, sticky="w")
        for i, (menu, (jumlah, temp, sugar)) in enumerate(self.menu.items()):
            tk.Label(self.frame, text=f"{menu} ({temp}, {sugar}) - {jumlah} pcs", font=self.font_default, bg="#C9BCB3").grid(row=i+1, column=0, sticky="w")

        tk.Label(self.frame, text=f"Total Harga: Rp {total_harga}", font=self.font_default, bg="#C9BCB3").grid(row=len(self.menu)+1, column=0, sticky="w")
        tk.Label(self.frame, text=f"Diskon: Rp {diskon}", font=self.font_default, bg="#C9BCB3").grid(row=len(self.menu)+2, column=0, sticky="w")
        tk.Label(self.frame, text=f"Harga Bayar: Rp {harga_bayar}", font=self.font_default, bg="#C9BCB3").grid(row=len(self.menu)+3, column=0, sticky="w")

        tk.Label(self.frame, text="Uang Pembayaran", font=self.font_default, bg="#C9BCB3").grid(row=len(self.menu)+4, column=0, sticky="w")
        self.entry_uang = tk.Entry(self.frame, font=self.font_default)
        self.entry_uang.grid(row=len(self.menu)+4, column=1)

        tk.Button(self.frame, text="Hitung", font=self.font_default, command=self.calculate).grid(row=len(self.menu)+5, columnspan=2, pady=10)
# Memperbaiki bagian tombol back
        tk.Button(self.frame, text="Back", font=self.font_default, command=self.page2).grid(row=len(self.menu)+6, columnspan=2, pady=10)

    def calculate(self):
        try:
            uang = int(self.entry_uang.get())
            if uang <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Uang Pembayaran harus berupa angka positif.")
            return

        total_harga, diskon, harga_bayar = calculate_total(self.menu, menu_prices)

        try:
            uang_kembali = calculate_change(uang, harga_bayar)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        result_text = (
            f"Nama Barista: {self.barista}\n"
            f"Nama Pembeli: {self.pembeli}\n"
            f"\nPesanan:\n" +
            "\n".join([f"{menu} ({temp}, {sugar}) - {jumlah} pcs" for menu, (jumlah, temp, sugar) in self.menu.items()]) +
            f"\nTotal Harga: Rp {total_harga}\n"
            f"Diskon: Rp {diskon}\n"
            f"Harga Bayar: Rp {harga_bayar}\n"
            f"Uang Kembali: Rp {uang_kembali}\n"
            "\nTerima kasih atas kunjungannya.\nSelamat menikmati pesanan Anda."
        )

        save_to_excel(self.barista, self.pembeli, self.menu, total_harga, diskon, harga_bayar, uang, uang_kembali)
        self.show_summary(result_text)

    def show_summary(self, result_text):
        self.clear_frame()
        tk.Label(self.frame, text=result_text, font=self.font_default, bg="#C9BCB3", justify="left").pack()
        tk.Button(self.frame, text="Kembali ke Halaman Awal", font=self.font_default, command=self.page1).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = KasirApp(root)
    root.mainloop()
