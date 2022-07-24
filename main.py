import sys

from PyQt6.QtWidgets import QApplication

from ui.main import MainUI


def main():
    app = QApplication(sys.argv)

    window = MainUI()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
