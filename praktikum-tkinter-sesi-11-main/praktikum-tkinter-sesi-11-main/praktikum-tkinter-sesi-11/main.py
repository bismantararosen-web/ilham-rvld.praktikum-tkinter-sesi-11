"""
Praktikum Python Tkinter - Sesi 11
Advanced Widgets dan Event Handling

Aplikasi Pendaftaran Kegiatan Mahasiswa.
Widget yang digunakan: Entry, Combobox, Radiobutton, Checkbutton, Text,
Listbox, Button, Label, Frame/LabelFrame, Menu, Messagebox, dan Toplevel.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------------------------------------------
# Data pilihan
# ---------------------------------------------------------------------------
PROGRAM_STUDI = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Elektro",
    "Manajemen",
    "Akuntansi",
    "Desain Komunikasi Visual",
]

KEGIATAN = [
    "Seminar Teknologi",
    "Lomba Coding",
    "Pelatihan Public Speaking",
    "Bakti Sosial",
    "Turnamen Olahraga",
    "Pentas Seni",
]

JENIS_KELAMIN = ["Laki-laki", "Perempuan"]


# ---------------------------------------------------------------------------
# Fungsi validasi (dipisah dari GUI agar mudah diuji)
# ---------------------------------------------------------------------------
def validasi_form(nama, prodi, gender, kegiatan, alasan):
    """Mengembalikan (valid, pesan_error, widget_target)."""
    if not nama.strip():
        return False, "Nama tidak boleh kosong.", "nama"
    if not prodi:
        return False, "Silakan pilih program studi.", "prodi"
    if not gender:
        return False, "Silakan pilih jenis kelamin.", "gender"
    if not kegiatan:
        return False, "Pilih minimal satu kegiatan.", "kegiatan"
    if not alasan.strip():
        return False, "Alasan mengikuti kegiatan tidak boleh kosong.", "alasan"
    return True, "", None


class AplikasiPendaftaran:
    def __init__(self, root):
        self.root = root
        self.root.title("Pendaftaran Kegiatan Mahasiswa")
        self.root.geometry("820x640")
        self.root.minsize(760, 600)

        # Variabel kontrol
        self.var_nama = tk.StringVar()
        self.var_prodi = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_kegiatan = {k: tk.BooleanVar(value=False) for k in KEGIATAN}

        self._buat_menu()
        self._buat_antarmuka()
        self._pasang_event()

        self.entry_nama.focus_set()

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------
    def _buat_menu(self):
        menubar = tk.Menu(self.root)

        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Reset Formulir", accelerator="Ctrl+R",
                              command=self.reset)
        menu_file.add_separator()
        menu_file.add_command(label="Keluar", accelerator="Ctrl+Q",
                              command=self.keluar)
        menubar.add_cascade(label="File", menu=menu_file)

        menu_bantuan = tk.Menu(menubar, tearoff=0)
        menu_bantuan.add_command(label="Tentang Aplikasi", accelerator="F1",
                                 command=self.tampilkan_about)
        menubar.add_cascade(label="Bantuan", menu=menu_bantuan)

        self.root.config(menu=menubar)

    # ------------------------------------------------------------------
    # Antarmuka
    # ------------------------------------------------------------------
    def _buat_antarmuka(self):
        # Judul
        frame_judul = tk.Frame(self.root, bg="#1f4e79")
        frame_judul.pack(fill="x")
        tk.Label(frame_judul, text="FORMULIR PENDAFTARAN KEGIATAN MAHASISWA",
                 bg="#1f4e79", fg="white",
                 font=("Segoe UI", 14, "bold"), pady=10).pack()

        # Container utama: kiri = formulir, kanan = ringkasan
        container = tk.Frame(self.root, padx=12, pady=10)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(0, weight=1)

        frame_form = ttk.LabelFrame(container, text=" Data Pendaftar ", padding=10)
        frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        frame_form.columnconfigure(1, weight=1)

        frame_info = ttk.LabelFrame(container, text=" Ringkasan Pendaftaran ", padding=10)
        frame_info.grid(row=0, column=1, sticky="nsew")
        frame_info.rowconfigure(0, weight=1)
        frame_info.columnconfigure(0, weight=1)

        # --- Nama (Entry)
        ttk.Label(frame_form, text="Nama Lengkap").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_nama = ttk.Entry(frame_form, textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, sticky="ew", pady=4)

        # --- Program studi (Combobox)
        ttk.Label(frame_form, text="Program Studi").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_prodi = ttk.Combobox(frame_form, textvariable=self.var_prodi,
                                        values=PROGRAM_STUDI, state="readonly")
        self.combo_prodi.grid(row=1, column=1, sticky="ew", pady=4)

        # --- Jenis kelamin (Radiobutton)
        ttk.Label(frame_form, text="Jenis Kelamin").grid(row=2, column=0, sticky="w", pady=4)
        frame_gender = ttk.Frame(frame_form)
        frame_gender.grid(row=2, column=1, sticky="w", pady=4)
        self.radio_gender = []
        for jk in JENIS_KELAMIN:
            rb = ttk.Radiobutton(frame_gender, text=jk, value=jk, variable=self.var_gender)
            rb.pack(side="left", padx=(0, 14))
            self.radio_gender.append(rb)

        # --- Kegiatan (Checkbutton)
        ttk.Label(frame_form, text="Pilih Kegiatan").grid(row=3, column=0, sticky="nw", pady=4)
        frame_cek = ttk.Frame(frame_form)
        frame_cek.grid(row=3, column=1, sticky="w", pady=4)
        self.check_kegiatan = []
        for i, kegiatan in enumerate(KEGIATAN):
            cb = ttk.Checkbutton(frame_cek, text=kegiatan,
                                 variable=self.var_kegiatan[kegiatan],
                                 command=self.perbarui_listbox)
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 14), pady=1)
            self.check_kegiatan.append(cb)

        # --- Listbox pilihan kegiatan
        ttk.Label(frame_form, text="Kegiatan Terpilih").grid(row=4, column=0, sticky="nw", pady=4)
        frame_list = ttk.Frame(frame_form)
        frame_list.grid(row=4, column=1, sticky="ew", pady=4)
        frame_list.columnconfigure(0, weight=1)
        self.listbox = tk.Listbox(frame_list, height=4, activestyle="none",
                                  exportselection=False)
        self.listbox.grid(row=0, column=0, sticky="ew")
        scroll_list = ttk.Scrollbar(frame_list, orient="vertical",
                                    command=self.listbox.yview)
        scroll_list.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scroll_list.set)

        # --- Alasan (Text)
        ttk.Label(frame_form, text="Alasan Mengikuti").grid(row=5, column=0, sticky="nw", pady=4)
        frame_alasan = ttk.Frame(frame_form)
        frame_alasan.grid(row=5, column=1, sticky="nsew", pady=4)
        frame_alasan.columnconfigure(0, weight=1)
        frame_form.rowconfigure(5, weight=1)
        self.text_alasan = tk.Text(frame_alasan, height=5, width=30, wrap="word")
        self.text_alasan.grid(row=0, column=0, sticky="nsew")
        scroll_alasan = ttk.Scrollbar(frame_alasan, orient="vertical",
                                      command=self.text_alasan.yview)
        scroll_alasan.grid(row=0, column=1, sticky="ns")
        self.text_alasan.config(yscrollcommand=scroll_alasan.set)
        frame_alasan.rowconfigure(0, weight=1)

        # --- Tombol Submit & Reset
        frame_tombol = ttk.Frame(frame_form)
        frame_tombol.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(frame_tombol, text="Submit", width=12,
                   command=self.submit).pack(side="left", padx=6)
        ttk.Button(frame_tombol, text="Reset", width=12,
                   command=self.reset).pack(side="left", padx=6)

        # --- Area informasi / ringkasan (Text read-only)
        self.text_info = tk.Text(frame_info, width=34, wrap="word",
                                 state="disabled", bg="#f5f5f5",
                                 font=("Consolas", 10), padx=6, pady=6)
        self.text_info.grid(row=0, column=0, sticky="nsew")
        scroll_info = ttk.Scrollbar(frame_info, orient="vertical",
                                    command=self.text_info.yview)
        scroll_info.grid(row=0, column=1, sticky="ns")
        self.text_info.config(yscrollcommand=scroll_info.set)
        self._tulis_info("Belum ada data pendaftaran.\n\n"
                         "Isi formulir lalu tekan Submit\n(atau tombol Enter).")

        # --- Status bar
        self.var_status = tk.StringVar(value="Siap. Tekan Enter untuk Submit.")
        tk.Label(self.root, textvariable=self.var_status, anchor="w",
                 relief="sunken", bd=1, padx=6).pack(fill="x", side="bottom")

    # ------------------------------------------------------------------
    # Event keyboard
    # ------------------------------------------------------------------
    def _pasang_event(self):
        # Enter pada widget input (kecuali Text, agar Enter tetap membuat baris baru)
        for widget in (self.entry_nama, self.combo_prodi, self.listbox,
                       *self.radio_gender, *self.check_kegiatan):
            widget.bind("<Return>", self.submit)
        # Pada Text, gunakan Ctrl+Enter
        self.text_alasan.bind("<Control-Return>", self._submit_dari_text)

        # Shortcut global
        self.root.bind("<Control-r>", lambda e: self.reset())
        self.root.bind("<Control-q>", lambda e: self.keluar())
        self.root.bind("<F1>", lambda e: self.tampilkan_about())
        self.root.protocol("WM_DELETE_WINDOW", self.keluar)

        # Event saat memilih prodi / gender memperbarui status bar
        self.combo_prodi.bind("<<ComboboxSelected>>",
                              lambda e: self.var_status.set(f"Prodi dipilih: {self.var_prodi.get()}"))

    def _submit_dari_text(self, event=None):
        self.submit()
        return "break"  # cegah penambahan baris baru

    # ------------------------------------------------------------------
    # Logika
    # ------------------------------------------------------------------
    def _kegiatan_terpilih(self):
        return [k for k in KEGIATAN if self.var_kegiatan[k].get()]

    def perbarui_listbox(self):
        """Menampilkan kegiatan yang dicentang pada Listbox."""
        self.listbox.delete(0, tk.END)
        for k in self._kegiatan_terpilih():
            self.listbox.insert(tk.END, k)
        self.var_status.set(f"{self.listbox.size()} kegiatan dipilih.")

    def _tulis_info(self, teks):
        self.text_info.config(state="normal")
        self.text_info.delete("1.0", tk.END)
        self.text_info.insert("1.0", teks)
        self.text_info.config(state="disabled")

    def _fokus(self, target):
        {
            "nama": self.entry_nama,
            "prodi": self.combo_prodi,
            "gender": self.radio_gender[0],
            "kegiatan": self.check_kegiatan[0],
            "alasan": self.text_alasan,
        }[target].focus_set()

    def submit(self, event=None):
        nama = self.var_nama.get()
        prodi = self.var_prodi.get()
        gender = self.var_gender.get()
        kegiatan = self._kegiatan_terpilih()
        alasan = self.text_alasan.get("1.0", tk.END)

        valid, pesan, target = validasi_form(nama, prodi, gender, kegiatan, alasan)
        if not valid:
            messagebox.showwarning("Validasi Gagal", pesan)
            self.var_status.set("Validasi gagal: " + pesan)
            self._fokus(target)
            return

        daftar_kegiatan = "\n".join(f"  {i}. {k}" for i, k in enumerate(kegiatan, 1))
        ringkasan = (
            "=== RINGKASAN PENDAFTARAN ===\n\n"
            f"Nama          : {nama.strip()}\n"
            f"Program Studi : {prodi}\n"
            f"Jenis Kelamin : {gender}\n\n"
            f"Kegiatan ({len(kegiatan)}):\n{daftar_kegiatan}\n\n"
            f"Alasan:\n{alasan.strip()}\n"
        )
        self._tulis_info(ringkasan)
        self.var_status.set(f"Pendaftaran atas nama {nama.strip()} berhasil.")
        messagebox.showinfo("Pendaftaran Berhasil",
                            f"Terima kasih, {nama.strip()}!\n"
                            "Pendaftaran Anda telah dicatat.")

    def reset(self):
        self.var_nama.set("")
        self.var_prodi.set("")
        self.var_gender.set("")
        for var in self.var_kegiatan.values():
            var.set(False)
        self.listbox.delete(0, tk.END)
        self.text_alasan.delete("1.0", tk.END)
        self._tulis_info("Belum ada data pendaftaran.\n\n"
                         "Isi formulir lalu tekan Submit\n(atau tombol Enter).")
        self.var_status.set("Formulir telah direset.")
        self.entry_nama.focus_set()

    def keluar(self):
        if messagebox.askyesno("Konfirmasi Keluar",
                               "Apakah Anda yakin ingin keluar dari aplikasi?"):
            self.root.destroy()

    def tampilkan_about(self):
        """Jendela About menggunakan Toplevel."""
        about = tk.Toplevel(self.root)
        about.title("Tentang Aplikasi")
        about.geometry("360x240")
        about.resizable(False, False)
        about.transient(self.root)   # selalu di atas jendela utama
        about.grab_set()             # bersifat modal

        frame = ttk.Frame(about, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Pendaftaran Kegiatan Mahasiswa",
                  font=("Segoe UI", 13, "bold")).pack(pady=(0, 4))
        ttk.Label(frame, text="Versi 1.0").pack()
        ttk.Separator(frame).pack(fill="x", pady=10)
        ttk.Label(frame, justify="center",
                  text=("Praktikum Python Tkinter - Sesi 11\n"
                        "Advanced Widgets dan Event Handling\n\n"
                        "Dibuat oleh: Nama / NIM Anda")).pack()
        ttk.Button(frame, text="Tutup", command=about.destroy).pack(pady=(14, 0))
        about.bind("<Escape>", lambda e: about.destroy())


def main():
    root = tk.Tk()
    AplikasiPendaftaran(root)
    root.mainloop()


if __name__ == "__main__":
    main() 