import sys
from typing import Any

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QPlainTextEdit


class Window(QMainWindow):
    """GUI Main Window Code."""

    def __init__(self: Any, parent: Any = None) -> None:
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Notebooky")
        self.resize(500, 500)

        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        self.path = None

        self._createActions()
        self._createMenuBar()

    def _createMenuBar(self: Any) -> None:
        """Creation of Menu bar is done here, Actions created added here"""

        menuBar = self.menuBar()

        # File menu - New, Open, Save, Exit
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        # Edit menu - Copy, Paste, Cut
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        # Help menu - Help, About
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpAction)
        helpMenu.addAction(self.aboutAction)

    def _createActions(self: Any) -> None:
        """All the actions for GUI are declared here"""
        # TODO Add functionality for New, Open, Save
        self.newAction = QAction("&New", self)

        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.close)

        self.copyAction = QAction("&Copy", self)
        self.copyAction.triggered.connect(self.editor.copy)

        self.pasteAction = QAction("&Paste", self)
        self.pasteAction.triggered.connect(self.editor.paste)

        self.cutAction = QAction("&Cut", self)
        self.cutAction.triggered.connect(self.editor.cut)

        # TODO Add functionality for Help, About
        self.helpAction = QAction("&Help", self)
        self.aboutAction = QAction("&About", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
