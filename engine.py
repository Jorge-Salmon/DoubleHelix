
import sys
from engine_ui import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from double_helix import double_helix as dna


class DHEngine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.app = qtw.QApplication(sys.argv)
        self.MainWindow = qtw.QMainWindow()

        #auxiliary global variables
        self.type = 'DNA'

    def setup(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # buttons - actions
        self.ui.pushButton_load.clicked.connect(self.open)
        self.ui.pushButton_randSeq.clicked.connect(self.random_seq)
        self.ui.pushButton_info.clicked.connect(self.seq_info)
        self.ui.pushButton_save.clicked.connect(self.save)
        self.ui.pushButton_translate.clicked.connect(self.translate)
        self.ui.pushButton_transcript.clicked.connect(self.transcript)
        self.ui.pushButton_readingFrames.clicked.connect(self.read_frames)
        self.ui.pushButton_proteinsORF.clicked.connect(self.proteinsORF)
        self.ui.DNA_Button.toggled.connect(self.update_radioButtons)
        self.ui.RNA_button.toggled.connect(self.update_radioButtons)
        self.ui.DNA_Button.toggled.connect(self.update_radioButtons)
        self.ui.RNA_button.toggled.connect(self.update_radioButtons)

        # restrict text_edit_length to integer values only
        self.ui.textEdit_length.setValidator(qtg.QIntValidator())

        # style
        sshFile="darkorange.stylesheet.qss"
        with open(sshFile,"r") as fh:
            self.app.setStyleSheet(fh.read())

    def display(self):
        self.MainWindow.show()
        self.MainWindow.setWindowTitle('Double Helix - Genomics Tools')
        self.MainWindow.setWindowIcon(qtg.QIcon('icon.png'))

    def run(self):
        sys.exit(self.app.exec_())

    def open(self):
        filename, _ = qtw.QFileDialog.getOpenFileName()
        if filename:
            with open(filename, 'r') as handle:
                text = handle.read()
            self.clear()
            self.ui.text_input.insertPlainText(text)
            self.ui.text_input.moveCursor(qtg.QTextCursor.Start)
            self.MainWindow.statusBar().showMessage(f'Editing {filename}', 5000)

    def clear(self):
        self.ui.text_input.clear()
        self.ui.textEdit_console.clear()
        self.ui.textEdit_label.clear()
        self.ui.textEdit_length.clear()

    def save(self):
        text = self.ui.textEdit_console.toPlainText()
        filename, _ = qtw.QFileDialog.getSaveFileName()
        if filename:
            with open(filename, 'w') as handle:
                handle.write(text)
                self.MainWindow.statusBar().showMessage(f'Saved to {filename}', 500)

    def random_seq(self):
        dna_instance = dna()
        if self.ui.textEdit_length.text():
            length=int(self.ui.textEdit_length.text())
            dna_instance.generate_random(length=length, new_type=str(self.type))
        else:
            dna_instance.generate_random(new_type=self.type)
        self.ui.text_input.clear()
        self.ui.text_input.insertPlainText(dna_instance.seq)
        self.ui.text_input.moveCursor(qtg.QTextCursor.Start)

    def seq_info(self):
        input_seq = self.ui.text_input.toPlainText()
        input_label = self.ui.textEdit_label.text()
        try:
            dna_instance = dna(seq=input_seq, type=self.type, label=input_label)
            self.ui.textEdit_console.clear()
            self.ui.textEdit_console.insertPlainText(
                    dna_instance.get_info()+'\n[GC content]: '+ str(dna_instance.gc_content())+'%'
                )
            self.ui.textEdit_console.moveCursor(qtg.QTextCursor.Start)
        except:
            self.invalid()

    def transcript(self):
        input_seq = self.ui.text_input.toPlainText()
        try:
            dna_instance = dna(seq=input_seq, type=self.type)
            self.ui.textEdit_console.clear()
            self.ui.textEdit_console.insertPlainText(dna_instance.transcription())
            self.ui.textEdit_console.moveCursor(qtg.QTextCursor.Start)
        except:
            self.invalid()

    def translate(self):
        input_seq = self.ui.text_input.toPlainText()
        try:
            dna_instance = dna(seq=input_seq, type=self.type)
            self.ui.textEdit_console.clear()
            self.ui.textEdit_console.insertPlainText(dna_instance.translate_seq())
            self.ui.textEdit_console.moveCursor(qtg.QTextCursor.Start)
        except:
            self.invalid()

    def read_frames(self):
        input_seq = self.ui.text_input.toPlainText()
        try:
            dna_instance = dna(seq=input_seq, type=self.type)
            reading_frames = "[Open reading frames]:\n\n"
            for i,j in zip(dna_instance.open_reading_frames(), range(1,7)):
                reading_frames += f"[{j}]: {i}\n\n"
            self.ui.textEdit_console.clear()
            self.ui.textEdit_console.insertPlainText(reading_frames)
            self.ui.textEdit_console.moveCursor(qtg.QTextCursor.Start)
        except:
            self.invalid()

    def proteinsORF(self):
        input_seq = self.ui.text_input.toPlainText()
        try:
            dna_instance = dna(seq=input_seq, type=self.type)
            proteins_found = dna_instance.proteins_rf()
            num_proteins = len(proteins_found)
            prots = f"[Proteins from all open reading frames]: Found {num_proteins} proteins\n\n"
            for i,j in zip(proteins_found, range(1, num_proteins+1)):
                prots += f"[{j}]: {i}\n\n"
            self.ui.textEdit_console.clear()
            self.ui.textEdit_console.insertPlainText(prots)
            self.ui.textEdit_console.moveCursor(qtg.QTextCursor.Start)
        except:
            self.invalid()

    def invalid(self):
        self.ui.textEdit_console.clear()
        self.ui.textEdit_console.insertPlainText('Enter a valid DNA or RNA sequence, or valid sequence type')
        self.ui.textEdit_console.moveCursor(qtg.QTextCursor.Start)

    def update_radioButtons(self):
        radioButton = qtw.QWidget().sender()
        if radioButton.isChecked():
            self.type = radioButton.text()
