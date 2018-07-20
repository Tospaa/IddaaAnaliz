import tkinter as tk
import tkinter.messagebox as msgbox
import recipe as tktable
import sqlite3

__author__ = "Musa Ecer"
__version__ = "0.4"
__email__ = "musaecer@gmail.com"

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("İddaa Analiz v{0}".format(__version__))
        try:
            with open("last","r") as f:
                last = f.readlines()
            for i in range(len(last)):
                last[i] = last[i].strip()
        except FileNotFoundError:
            last = ["","",""]
        # Etiket ve butonlar:
        self.statik_etiket_ms1 = tk.Label(self, text="1", font=("Helvetica", 15))
        self.statik_etiket_ms0 = tk.Label(self, text="X", font=("Helvetica", 15))
        self.statik_etiket_ms2 = tk.Label(self, text="2", font=("Helvetica", 15))
        self.dinamik_etiket_ust = tk.Label(self, text="Üst Bitme Oranı:", font=("Helvetica", 15))
        self.dinamik_etiket_alt = tk.Label(self, text="Alt Bitme Oranı:", font=("Helvetica", 15))
        self.dinamik_etiket_toplam_mac = tk.Label(self, text="Toplam bulunan maç:", font=("Helvetica", 15))
        self.dinamik_etiket_ortalama_gol = tk.Label(self, text="Ortalama gol sayısı:", font=("Helvetica", 15))
        self.giris_ms1 = tk.Entry(self, font=("Helvetica", 15))
        self.giris_ms1.insert(0, last[0])
        self.giris_ms0 = tk.Entry(self, font=("Helvetica", 15))
        self.giris_ms0.insert(0, last[1])
        self.giris_ms2 = tk.Entry(self, font=("Helvetica", 15))
        self.giris_ms2.insert(0, last[2])
        self.buton_numunelik = tk.Button(self, text="Arama yap", command=self.arama_yap, font=("Helvetica", 15))
        self.bind("<Return>", self.arama_yap)
        # Geometri ve nesne yerleştirmeleri:
        self.statik_etiket_ms1.grid(row=0,column=0)
        self.giris_ms1.grid(row=0,column=1)
        self.statik_etiket_ms0.grid(row=1,column=0)
        self.giris_ms0.grid(row=1,column=1)
        self.statik_etiket_ms2.grid(row=2,column=0)
        self.giris_ms2.grid(row=2,column=1)
        self.dinamik_etiket_ust.grid(row=3,column=0,columnspan=2)
        self.dinamik_etiket_alt.grid(row=4,column=0,columnspan=2)
        self.dinamik_etiket_toplam_mac.grid(row=5,column=0,columnspan=2)
        self.dinamik_etiket_ortalama_gol.grid(row=6,column=0,columnspan=2)
        self.buton_numunelik.grid(row=7,column=0,columnspan=2)
        # Veritabanı ilişiği:
        self.conn = sqlite3.connect("veri.db")
        self.c = self.conn.cursor()
        # Tablo nesnesi:
        self.tablo = tktable.Table(self, ["Lig", "Ev", "Deplasman", "İY", "MS", "1", "X", "2", "İY1", "İY0", "İY2", "KG Var", "KG Yok", "Alt", "Üst", "TG 0-1", "TG 2-3", "TG 4-6", "TG 7+"], column_minwidths=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])

    def arama_yap(self, *args):
        self.tablo.grid_forget()
        try:
            ms1 = format(float(self.giris_ms1.get().replace(",",".").strip()), '.2f')
            ms0 = format(float(self.giris_ms0.get().replace(",",".").strip()), '.2f')
            ms2 = format(float(self.giris_ms2.get().replace(",",".").strip()), '.2f')
        except ValueError:
            msgbox.showerror("Hata","Doğru formatta girdi yapılmadı.")
            return None
        
        oranlist = [ms1, ms0, ms2]
        
        self.c.execute("SELECT * FROM MACLAR WHERE ms1==? AND ms0==? AND ms2==?", oranlist)
        ham_veri_listesi = list(self.c.fetchall())
        
        if len(ham_veri_listesi) > 0:
            with open("last", "w") as f:
                f.write("{0}\n{1}\n{2}".format(ms1, ms0, ms2))
        
        self.tablo.set_data([[]])
        self.tablo.delete_row(1)
        
        ust = 0
        alt = 0
        toplamgol = 0
        toplama_katilmayacak_mac_sayisi = 0
        
        for i in ham_veri_listesi:
            self.tablo.insert_row(i)
            try:
                toplamgol+=(int(i[4][0]) + int(i[4][-1]))
                if (int(i[4][0]) + int(i[4][-1])) > 2.5:
                    ust+=1
                else:
                    alt+=1
            except ValueError:
                toplama_katilmayacak_mac_sayisi += 1
                continue
        
        if len(ham_veri_listesi) > 0:
            ustoran = ust / (len(ham_veri_listesi) - toplama_katilmayacak_mac_sayisi)
            altoran = alt / (len(ham_veri_listesi) - toplama_katilmayacak_mac_sayisi)
            toplamgoloran = toplamgol / (len(ham_veri_listesi) - toplama_katilmayacak_mac_sayisi)
            self.dinamik_etiket_alt.configure(text="Alt Bitme Oranı: % {}".format(round(altoran*100, 2)))
            self.dinamik_etiket_ust.configure(text="Üst Bitme Oranı: % {}".format(round(ustoran*100, 2)))
            self.dinamik_etiket_toplam_mac.configure(text="Toplam bulunan maç: {}".format(len(ham_veri_listesi)))
            self.dinamik_etiket_ortalama_gol.configure(text="Ortalama gol sayısı: {}".format(round(toplamgoloran, 2)))
            self.tablo.grid(row=8,column=0,columnspan=2)
            self.update()

        else:
            msgbox.showerror("Hata","Girilen oranlarla aynı orana sahip maç bulunamadı.")
            self.dinamik_etiket_alt.configure(text="Alt Bitme Oranı:")
            self.dinamik_etiket_ust.configure(text="Üst Bitme Oranı:")
            self.dinamik_etiket_toplam_mac.configure(text="Toplam bulunan maç: 0")
            self.dinamik_etiket_ortalama_gol.configure(text="Ortalama gol sayısı:")


if __name__ == "__main__":
    window = mainWindow()
    window.mainloop()