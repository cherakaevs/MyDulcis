from PyQt5.QtWidgets import QApplication
import window

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = window.Window()
    window.show()
    app.exec()
