import tkinter as tk
import recipe as tktable
import sqlite3

__author__ = "Musa Ecer"
__version__ = "0.1"
__email__ = "musaecer@gmail.com"

class mainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("İddaa Analiz v{0}".format(__version__))
        # Etiket ve butonlar:
        self.statik_etiket_ms1 = tk.Label(self, text="MS1", font=("Helvetica", 30))
        self.statik_etiket_ms0 = tk.Label(self, text="MS0", font=("Helvetica", 30))
        self.statik_etiket_ms2 = tk.Label(self, text="MS2", font=("Helvetica", 30))
        self.giris_ms1 = tk.Entry(self, font=("Helvetica", 30))
        self.giris_ms0 = tk.Entry(self, font=("Helvetica", 30))
        self.giris_ms2 = tk.Entry(self, font=("Helvetica", 30))
        self.buton_numunelik = tk.Button(self, text="Arama yap", command=self.arama_yap, font=("Helvetica", 30))
        # Geometri ve nesne yerleştirmeleri:
        self.statik_etiket_ms1.grid(row=0,column=0)
        self.giris_ms1.grid(row=0,column=1)
        self.statik_etiket_ms0.grid(row=1,column=0)
        self.giris_ms0.grid(row=1,column=1)
        self.statik_etiket_ms2.grid(row=2,column=0)
        self.giris_ms2.grid(row=2,column=1)
        self.buton_numunelik.grid(row=3,column=0,columnspan=2)
        # Veritabanı ilişiği:
        self.conn = sqlite3.connect("veri.db")
        self.c = self.conn.cursor()

    def arama_yap(self, *args):
        oranlist = [self.giris_ms1.get(), self.giris_ms0.get(), self.giris_ms2.get()]
        
        self.c.execute("SELECT * FROM MACLAR WHERE ms1==? AND ms0==? AND ms2==?", oranlist)
        
        tablo = tktable.Table(self, ["Lig", "Ev", "Deplasman", "İY", "MS", "MS1", "MS0", "MS2", "İY1", "İY0", "İY2", "KG Var", "KG Yok", "Alt", "Üst", "TG 0-1", "TG 2-3", "TG 4-6", "TG 7+"], column_minwidths=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        
        for i in self.c.fetchall():
            tablo.insert_row(i)
        
        tablo.grid(row=4,column=0,columnspan=2)
        self.update()
        
        
        
if __name__ == "__main__":
    window = mainWindow()
    window.mainloop()