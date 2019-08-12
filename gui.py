import sys
import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QTabWidget, QVBoxLayout, QFileDialog, QComboBox, QLabel, QLineEdit

def show_styles(styles):
    return [
        " ".join(f.split(".")[0].split("_")).title()
        for f in styles
    ]

def get_styles():
    return [f for f in os.listdir('./saved_models')]


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Neural Style Transfer'
        self.width, self.height = 400, 180
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        self.table_widget = Table(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class Table(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        ############################
        # Convert Tab
        ############################

        self.styles = get_styles()

        self.fname = None
        self.style = self.styles[0]

        self.convert_tab = QWidget()

        # --------------
        # Get File
        # --------------

        browse = QPushButton('Browse File', self.convert_tab)
        browse_label = QLabel(self.convert_tab)
        browse_label.move(120, 0)

        def on_browse():
            self.fname = self.openFileNameDialog("Choose Source Image")
            browse_label.setText(self.fname)
            browse_label.adjustSize()

        browse.clicked.connect(on_browse)


        # --------------
        # Choose Style
        # --------------
        cb = QComboBox(self.convert_tab)
        cb.addItems(show_styles(self.styles))

        def on_style(i):
            self.style = self.styles[i]

        cb.currentIndexChanged.connect(on_style)
        cb.move(1, 30)


        # --------------
        # Choose Output
        # --------------
        output_path = QLineEdit(self.convert_tab)
        output_path.setText("Output filepath")
        output_path.move(6, 70)


        # --------------
        # Convert Button
        # --------------
        convert = QPushButton('Convert', self.convert_tab)
        convert.setDefault(True)

        def on_convert():
            eval_command = "python3 neural_style/neural_style.py eval --content-image {} --model saved_models/{} --output-image {} --cuda 0"

            convert.clicked.disconnect()

            if self.fname is not None and self.style is not None:
                command = eval_command.format(self.fname, self.style, output_path.text())
                print(command)
                os.system(command)

            convert.clicked.connect(on_convert)

        convert.clicked.connect(on_convert)
        convert.move(0, 100)


        self.tabs.addTab(self.convert_tab, "Transfer Style to Frame")

        ############################
        # Train Tab
        ############################

        self.train_tab = QWidget()

        # --------------
        # Get File
        # --------------

        source_style = QPushButton('Browse File', self.train_tab)
        source_style_label = QLabel(self.convert_tab)

        def on_source_style():
            self.fname = self.openFileNameDialog("Choose Source Image")
            source_style_label.setText(self.fname)
            source_style_label.adjustSize()

        source_style.clicked.connect(on_source_style)


        # --------------
        # Train Button
        # --------------
        train = QPushButton('Train', self.train_tab)
        train.setDefault(True)

        def on_train():
            train_command = "python3 neural_style/neural_style.py train --dataset datasets --style-image {} --save-model-dir saved_models --cuda 0"

            train.clicked.disconnect()

            if self.fname is not None and self.style is not None:
                command = train_command.format(self.fname)
                print(command)
                os.system(command)

            train.clicked.connect(on_train)

        train.clicked.connect(on_train)
        train.move(0, 30)

        self.tabs.addTab(self.train_tab, "Train New Style")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def openFileNameDialog(self, title):
        fname, _ = QFileDialog.getOpenFileName(
                self, title, "", "All Files (*);;Python Files (*.py)")
        return fname


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
