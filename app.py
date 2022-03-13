import sys
import time
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QRect
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAbstractSpinBox
)

from main_ui import Ui_enigma_board


class Window(QMainWindow, Ui_enigma_board):
    def __init__(self, parent=None):
        super().__init__(parent)

        #props
        self.currentLetter = ""
        self.currentIndex = 0
        self.setupUi(self)
        self.disableConfigs()
        self.changeBoxBackgroundColor("r1_l1_box_1", "red")
        # self.changeLetterBackgroundColor("a","red")
        #--------------------
        self.configurerButton.clicked.connect(self.configurer_button_clicked)
        self.encrypterButton.clicked.connect(self.encypter_button_clicked)
        self.decrypterButton.clicked.connect(self.decrypter_button_clicked)
        self.suivantButton.clicked.connect(self.suivant_button_clicked)

    #----- Utils -----

    '''it sets the rotors and the reflecteur on readOnly mode'''
    def disableConfigs(self):
        for i in range(1, 27, 1):
            getattr(self, "ref_box_"+str(i)).setReadOnly(True)
            getattr(self, "ref_box_" + str(i)).setButtonSymbols(QAbstractSpinBox.NoButtons)
            for j in range(1, 4, 1):
                for k in range(1, 3, 1):
                    getattr(self, "r" + str(j) + "_l" + str(k) + "_box_" + str(i)).setReadOnly(True)
                    getattr(self, "r" + str(j) + "_l" + str(k) + "_box_" + str(i)).setButtonSymbols(QAbstractSpinBox.NoButtons)

    '''it sets the rotors and the reflecteur on Edit mode'''
    def enableConfigs(self):
        for i in range(1, 27, 1):
            getattr(self, "ref_box_" + str(i)).setReadOnly(False)
            getattr(self, "ref_box_" + str(i)).setButtonSymbols(QAbstractSpinBox.UpDownArrows)
            for j in range(1,4, 1):
                for k in range(1, 3, 1):
                    getattr(self, "r"+str(j)+"_l"+str(k)+"_box_"+str(i)).setReadOnly(False)
                    getattr(self, "r"+str(j)+"_l"+str(k)+"_box_"+str(i)).setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    ''' changes the color of the letter in the alphabets row by passing the letter and the color'''
    def changeLetterColor(self, letter, color):
        getattr(self, letter).setAutoFillBackground(True)  # This is important!!
        # getattr(self,letter).setStyleSheet("QLabel { background-color: "+color+" }")
        getattr(self, letter).setStyleSheet("QLabel { color: "+color+" }")

    ''' changes the background color of the letter in the alphabets row by passing the letter and the color'''
    def changeLetterBackgroundColor(self, letter, color):
        getattr(self, letter).setAutoFillBackground(True)  # This is important!!
        getattr(self, letter).setStyleSheet("QLabel { background-color: "+color+" }")

    def changeBoxBackgroundColor(self, box, color):
        getattr(self, box).setAutoFillBackground(True)  # This is important!!
        getattr(self,box).setStyleSheet("QSpinBox { background-color: "+color+" }")

    def animate(self, objectName):
        self.anim = QPropertyAnimation(getattr(self, objectName), b"geometry")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setStartValue(QRect(getattr(self, objectName).geometry()))
        self.anim.setEndValue(QRect(getattr(self, objectName).geometry().adjusted(0,0,-10,40)))
        self.anim.setDuration(1500)
        self.anim.start(QPropertyAnimation.DeleteWhenStopped)

    #--------------Actions when buttons are clicked-----------

    def configurer_button_clicked(self):
        if(self.configurerButton.text() == "Configurer Rotors"):
            self.enableConfigs()
            self.configurerButton.setText("Confirmer")
        elif(self.configurerButton.text() == "Confirmer"):
            self.disableConfigs()
            self.configurerButton.setText("Configurer Rotors")

    def encypter_button_clicked(self):
        msg = self.encryptTextEdit.toPlainText()
        self.decryptTextEdit.setText(msg)
        self.decryptTextEdit.setAlignment(Qt.AlignCenter)

    def suivant_button_clicked(self):
        msg = self.encryptTextEdit.toPlainText()
        if(self.currentIndex < len(msg)):
            if(self.currentIndex > 0):
                self.changeLetterBackgroundColor(self.currentLetter, "transparent")
            self.currentLetter = msg[self.currentIndex]
            self.currentIndex += 1
            self.changeLetterBackgroundColor(self.currentLetter, "red")
            # self.animate("r1_l1_box_1")
        else :
            self.changeLetterBackgroundColor(self.currentLetter, "transparent")
            self.decryptTextEdit.setText("Fin D'encryption")
            self.decryptTextEdit.setAlignment(Qt.AlignCenter)

    def decrypter_button_clicked(self):
        pass

# running the app
app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())

# this command is for compiling the .ui file generated by the qt designer :
#                $  pyuic5 -o main_ui.py ui/qt.ui
# when we finish the app, we can convert it to executable file using this commands:
#                $  pyinstaller --onefile --windowed -i".\ui\resources\enigma.ico" ".\app.py"
