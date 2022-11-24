import sys
from PyQt5.QtWidgets import QApplication
from ui.controlador import MainWindowTiendaRopa


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowTiendaRopa()
    win.show()
    sys.exit(app.exec_())
