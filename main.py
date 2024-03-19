import sys
import psutil
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget, QMenu, QFileDialog
from PyQt5.QtCore import QPoint

class GorevYoneticisiUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Görev Yöneticisi")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.ana_duzen = QVBoxLayout()

        self.gorev_listesi_etiketi = QLabel("Çalışan İşlemler:")
        self.ana_duzen.addWidget(self.gorev_listesi_etiketi)

        self.gorev_listesi = QListWidget()
        self.gorev_listesi.setContextMenuPolicy(3)  # Sağ tık menüsü için
        self.gorev_listesi.customContextMenuRequested.connect(self.sag_tik_menu)
        self.ana_duzen.addWidget(self.gorev_listesi)

        self.yenile_butonu = QPushButton("Yenile")
        self.yenile_butonu.clicked.connect(self.gorev_listesini_yenile)
        self.ana_duzen.addWidget(self.yenile_butonu)

        self.central_widget.setLayout(self.ana_duzen)

        self.gorev_listesini_yenile()

    def gorev_listesini_yenile(self):
        self.gorev_listesi.clear()
        for islem in psutil.process_iter(['pid', 'name']):
            self.gorev_listesi.addItem(f"{islem.info['pid']} - {islem.info['name']}")

    def sag_tik_menu(self, pos):
        menu = QMenu(self)
        enjekte_et_action = menu.addAction("DLL Enjekte Et")
        action = menu.exec_(self.gorev_listesi.mapToGlobal(pos))

        if action == enjekte_et_action:
            secili_eleman = self.gorev_listesi.currentItem()
            if secili_eleman:
                pid = int(secili_eleman.text().split(" - ")[0])
                dll_sec = QFileDialog.getOpenFileName(self, 'DLL Seç', filter='DLL Dosyaları (*.dll)')[0]
                if dll_sec:
                    try:
                        kernel32 = ctypes.windll.kernel32
                        h_process = kernel32.OpenProcess(0x1F0FFF, False, pid)
                        if h_process:
                            kernel32.LoadLibraryExW.restype = ctypes.c_void_p
                            kernel32.LoadLibraryExW.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD]
                            h_module = kernel32.LoadLibraryExW(dll_sec, None, 0x00000001)
                            if h_module:
                                print("DLL başarıyla enjekte edildi.")
                            else:
                                print("DLL enjekte edilemedi.")
                        else:
                            print("İşlem bulunamadı.")
                    except Exception as e:
                        print("Hata:", e)

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = GorevYoneticisiUygulamasi()
    pencere.show()
    sys.exit(uygulama.exec_())
