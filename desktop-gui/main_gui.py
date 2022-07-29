import sys
from typing import Any

from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import (
    QAction, QApplication, QHBoxLayout, QMainWindow, QPlainTextEdit,
    QPushButton, QVBoxLayout, QWidget
)


class Window(QMainWindow):
    """GUI Main Window Code."""

    def __init__(self: Any, parent: Any = None) -> None:
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Notebooky")
        self.resize(500, 500)

        # TODO Add Tooltips for buttons
        # TODO Add functionalities for buttons
        # TODO Set shortcuts for buttons

        oButton = QPushButton('Open')
        oButton.setIcon(QIcon('./resources/new.ico'))
        oButton.clicked.connect(self.micFunction)

        sButton = QPushButton('Save')
        sButton.setIcon(QIcon('./resources/save.ico'))
        sButton.clicked.connect(self.micFunction)

        micButton = QPushButton('Microphone')
        micButton.setIcon(QIcon('./resources/mic.ico'))
        micButton.setCheckable(True)
        # micButton.setStyleSheet("QPushButton:checked {color: white; background-color: green;}")
        micButton.clicked.connect(self.micFunction)

        self.editor = QPlainTextEdit()
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(oButton)
        buttons_layout.addWidget(sButton)
        buttons_layout.addWidget(micButton)

        layout.addLayout(buttons_layout)
        layout.addWidget(self.editor)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.path = None

        self._createActions()
        self._createMenuBar()

    def _createMenuBar(self: Any) -> None:
        """Creation of Menu bar is done here, Actions created added here"""
        menuBar = self.menuBar()

        # TODO Set shortcuts for Menu items
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
        self.openAction.triggered.connect(self.file_open)

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

    def micFunction(self: Any) -> None:
        """Function for Microphone dictation"""
        pass

    def file_open(self: Any) -> None:
        """Opens files via a dialog box"""
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as file:
                    text = file.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
