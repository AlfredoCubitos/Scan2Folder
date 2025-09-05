from PyQt6.QtWidgets import QApplication
import sys

def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.scanners()
    
    #window.show()
    
    sys.exit(app.exec())
    
if __name__ == "__main__":
    from .scan2folder import MainWindow
    main()