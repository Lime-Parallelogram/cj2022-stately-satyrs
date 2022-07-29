import sys
from typing import Any

from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import (
    QAction, QApplication, QFileDialog, QHBoxLayout, QMainWindow, QMessageBox,
    QPlainTextEdit, QPushButton, QVBoxLayout, QWidget
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
        oButton.clicked.connect(self.file_open)

        sButton = QPushButton('Save')
        sButton.setIcon(QIcon('./resources/save.ico'))
        sButton.clicked.connect(self.file_save)

        self.micButton = QPushButton('Microphone')
        self.micButton.setIcon(QIcon('./resources/mic.ico'))
        self.micButton.setCheckable(True)
        # micButton.setStyleSheet("QPushButton:checked {color: white; background-color: green;}")
        self.micButton.clicked.connect(self.micFunction)

        self.editor = QPlainTextEdit()
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(oButton)
        buttons_layout.addWidget(sButton)
        buttons_layout.addWidget(self.micButton)

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
        self.saveAction.triggered.connect(self.file_save)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.file_save)
        self.exitAction.triggered.connect(self.close)

        self.copyAction = QAction("&Copy", self)
        self.copyAction.triggered.connect(self.editor.copy)

        self.pasteAction = QAction("&Paste", self)
        self.pasteAction.triggered.connect(self.editor.paste)

        self.cutAction = QAction("&Cut", self)
        self.cutAction.triggered.connect(self.editor.cut)

        # TODO Add functionality for Help, About
        self.helpAction = QAction("&Help", self)
        self.helpAction.triggered.connect(self.helpFunction)

        self.aboutAction = QAction("&About", self)
        self.aboutAction.triggered.connect(self.AboutFunction)

    def micFunction(self: Any) -> None:
        """Function for Microphone dictation"""
        if self.micButton.isChecked():
            # Add Speech to text output here
            self.editor.appendPlainText("When you speak text will be appended")

    def new_file(self: Any) -> None:
        """New file functionality"""
        pass

    def file_open(self: Any) -> None:
        """Opens files via a dialog box"""
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'r') as file:
                    text = file.read()
            except Exception as e:
                exception_dialog = QMessageBox(self)
                exception_dialog.setWindowTitle("Error")
                exception_dialog.setText(e)
                exception_dialog.setIcon(QMessageBox.Critical)
                exception_dialog.show()
            else:
                self.path = path
                self.editor.setPlainText(text)

    def file_save(self: Any) -> None:
        """File save"""
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self: Any) -> None:
        """File save as"""
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self: Any, path: str) -> None:
        """Save to path"""
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as file:
                file.write(text)

        except Exception as e:
            exception_dialog = QMessageBox(self)
            exception_dialog.setWindowTitle("Error")
            exception_dialog.setText(e)
            exception_dialog.setIcon(QMessageBox.Critical)
            exception_dialog.show()

        else:
            self.path = path

    def helpFunction(self: Any) -> None:
        """Displays the help dialog box"""
        help_msg = """Really? Help in Notepad application. Come on man.\n
            It's a notepad. You write stuff in it."""
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Help")
        dlg.setText(help_msg)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def AboutFunction(self: Any) -> None:
        """Displays the About dialog box"""
        about_msg = """Notebooky App for Codejam 2022.\n
            Created by PyDiscord Team Stately Satyrs."""
        about_dlg = QMessageBox(self)
        about_dlg.setWindowTitle("About")
        about_dlg.setText(about_msg)
        about_dlg.setIcon(QMessageBox.Information)
        about_dlg.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
