import sys

from PyQt5.QtWidgets import QApplication

from ui.main import MainUI


def main():
    app = QApplication(sys.argv)

    window = MainUI()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
