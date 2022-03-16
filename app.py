import sys

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

from main_ui import Ui_enigma_board


class Window(QMainWindow, Ui_enigma_board):
    def __init__(self, parent=None):
        super().__init__(parent)

        # props
        self.currentLetter = "a"
        self.currentIndex = 0

        self.current_b1 = 0
        self.current_b2 = 0
        self.current_b3 = 0
        self.current_ref = 0

        self.ret_b1 = 0
        self.ret_b2 = 0
        self.ret_b3 = 0
        self.ret_ref = 0
        self.ret_letter = ""

        self.initialState = {}
        self.encrypterToggled = False
        self.decrypterToggled = False

        self.setupUi(self)
        self.initState()
        self.disableConfigs()
        # --------------------
        self.configurerButton.clicked.connect(self.configurer_button_clicked)
        self.encrypterButton.clicked.connect(self.encypter_button_clicked)
        self.decrypterButton.clicked.connect(self.decrypter_button_clicked)
        self.suivantButton.clicked.connect(self.suivant_button_clicked)

    # ------ Utils ------
    def initState(self):
        for i in range(1, 27, 1):
            for j in range(1, 4, 1):
                for k in range(1, 3, 1):
                    box = "r" + str(j) + "_l" + str(k) + "_box_" + str(i)
                    self.initialState[box] = getattr(self, box).value()

    def setInitialSate(self):
        for i in range(1, 27, 1):
            for j in range(1, 4, 1):
                for k in range(1, 3, 1):
                    box = "r" + str(j) + "_l" + str(k) + "_box_" + str(i)
                    getattr(self, box).setProperty("value", self.initialState[box])

    '''it sets the rotors and the reflecteur on readOnly mode'''

    def disableConfigs(self):
        for i in range(1, 4, 1):
            getattr(self, "c" + str(i) + "_DG").setEnabled(False)
            getattr(self, "c" + str(i) + "_box").setEnabled(False)

        # for i in range(1, 27, 1):
        #     getattr(self, "ref_box_"+str(i)).setReadOnly(True)
        #     getattr(self, "ref_box_" + str(i)).setButtonSymbols(QAbstractSpinBox.NoButtons)
        #     for j in range(1, 4, 1):
        #         for k in range(1, 3, 1):
        #             getattr(self, "r" + str(j) + "_l" + str(k) + "_box_" + str(i)).setReadOnly(True)
        #             getattr(self, "r" + str(j) + "_l" + str(k) + "_box_" + str(i)).setButtonSymbols(QAbstractSpinBox.NoButtons)

    '''it sets the rotors and the reflecteur on Edit mode'''

    def enableConfigs(self):
        for i in range(1, 4, 1):
            getattr(self, "c" + str(i) + "_DG").setEnabled(True)
            getattr(self, "c" + str(i) + "_box").setEnabled(True)

    ''' changes the color of the letter in the alphabets row by passing the letter and the color'''

    def changeLetterColor(self, letter, color):
        getattr(self, letter).setAutoFillBackground(True)  # This is important!!
        getattr(self, letter).setStyleSheet("QLabel { color: " + color + " }")

    ''' changes the background color of the letter in the alphabets row by passing the letter and the color'''

    def changeLetterBackgroundColor(self, letter, color):
        getattr(self, letter).setAutoFillBackground(True)  # This is important!!
        getattr(self, letter).setStyleSheet("QLabel { background-color: " + color + " }")

    def changeBoxBackgroundColor(self, box, color):
        getattr(self, box).setAutoFillBackground(True)  # This is important!!
        getattr(self, box).setStyleSheet("QSpinBox { background-color: " + color + " }")

    def decalage(self, rotor, direction, iteration):
        if direction == "G":
            for p in range(0, abs(iteration), 1):
                tmp1 = getattr(self, rotor + "_l1_box_1").value()
                tmp2 = getattr(self, rotor + "_l2_box_1").value()
                for k in range(1, 3, 1):
                    for i in range(1, 26, 1):
                        val = getattr(self, rotor + "_l" + str(k) + "_box_" + str(i + 1)).value()
                        getattr(self, rotor + "_l" + str(k) + "_box_" + str(i)).setProperty("value", val)
                getattr(self, rotor + "_l1_box_26").setProperty("value", tmp1)
                getattr(self, rotor + "_l2_box_26").setProperty("value", tmp2)

        elif direction == "D":
            for p in range(0, abs(iteration), 1):
                tmp1 = getattr(self, rotor + "_l1_box_26").value()
                tmp2 = getattr(self, rotor + "_l2_box_26").value()
                for k in range(1, 3, 1):
                    for i in range(26, 1, -1):
                        val = getattr(self, rotor + "_l" + str(k) + "_box_" + str(i - 1)).value()
                        getattr(self, rotor + "_l" + str(k) + "_box_" + str(i)).setProperty("value", val)
                getattr(self, rotor + "_l1_box_1").setProperty("value", tmp1)
                getattr(self, rotor + "_l2_box_1").setProperty("value", tmp2)

    def animate(self, object_name):
        self.anim = QPropertyAnimation(getattr(self, object_name), b"geometry")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setStartValue(QRect(getattr(self, object_name).geometry()))
        self.anim.setEndValue(QRect(getattr(self, object_name).geometry().adjusted(0, 0, -10, 40)))
        self.anim.setDuration(1500)
        self.anim.start(QPropertyAnimation.DeleteWhenStopped)

    # --------------Actions when buttons are clicked-----------

    def configurer_button_clicked(self):
        if (self.configurerButton.text() == "Configurer Rotors"):
            self.enableConfigs()
            self.configurerButton.setText("Confirmer")
        elif (self.configurerButton.text() == "Confirmer"):
            self.setInitialSate()
            self.disableConfigs()
            self.configRotors()
            self.configurerButton.setText("Configurer Rotors")

    def encypter_button_clicked(self):
        # this code is just for settling up the button
        msg = self.encryptTextEdit.toPlainText()
        if len(msg) > 0:
            self.encrypterButton.setEnabled(False)
            self.decrypterButton.setEnabled(False)
            self.encrypterToggled = True
            self.decrypterToggled = False
        # the code for the encryption here

#%%
    def suivant_button_clicked(self):
        # switch: encrypter ou decrypter
        self.colorerChemainEncryption()
        # if self.encrypterToggled:
        #     msg = self.encryptTextEdit.toPlainText().strip().replace(" ", "").lower()
        #     self.currentLetter = msg[self.currentIndex]
        #     if self.currentIndex < len(msg):
        #         self.colorerChemainEncryption()
        #         self.currentIndex += 1
        #     else:
        #         self.currentIndex = 0
        #         self.encrypterButton.setEnabled(True)
        #         self.decrypterButton.setEnabled(True)
        #         self.decrypterToggled = False
        #         self.encrypterToggled = False
        #         self.decryptTextEdit.setText("Fin D'encryption")
        #         self.decryptTextEdit.setAlignment(Qt.AlignCenter)
        #
        # elif self.decrypterToggled:
        #     msg = self.decryptTextEdit.toPlainText()
        #     if self.currentIndex < len(msg):
        #         # uncolor the elements of the previous step
        #         if (self.currentIndex > 0):
        #             self.changeLetterBackgroundColor(self.currentLetter, "transparent")
        #             self.changeBoxBackgroundColor("r1_l2_box_" + str(self.current_b1), "transparent")
        #             self.changeBoxBackgroundColor("r2_l2_box_" + str(self.current_b2), "transparent")
        #             self.changeBoxBackgroundColor("r3_l2_box_" + str(self.current_b3), "transparent")
        #             self.changeBoxBackgroundColor("ref_box_" + str(self.current_ref), "transparent")
        #
        #         self.currentLetter = msg[self.currentIndex].lower()
        #         self.changeLetterBackgroundColor(self.currentLetter, "red")
        #         # let's assume it's a encryption
        #         current_b1 = ord(self.currentLetter) - 96
        #         self.changeBoxBackgroundColor("r1_l2_box_" + str(current_b1), "red")
        #         box1 = getattr(self, "r1_l2_box_" + str(current_b1))
        #
        #         current_b2 = divmod((current_b1 + box1.value()), 26)[1]
        #         self.changeBoxBackgroundColor("r2_l2_box_" + str(current_b2), "red")
        #         box2 = getattr(self, "r2_l2_box_" + str(current_b2))
        #
        #         current_b3 = divmod((current_b2 + box2.value()), 26)[1]
        #         self.changeBoxBackgroundColor("r3_l2_box_" + str(current_b3), "red")
        #         box3 = getattr(self, "r3_l2_box_" + str(current_b3))
        #
        #         current_ref = divmod((current_b3 + box3.value()), 26)[1]
        #         self.changeBoxBackgroundColor("ref_box_" + str(current_ref), "red")
        #
        #         self.currentIndex += 1
        #
        #     else:
        #         self.currentIndex = 0
        #         self.encrypterButton.setEnabled(True)
        #         self.decrypterButton.setEnabled(True)
        #         self.decrypterToggled = False
        #         self.encrypterToggled = False
        #         self.changeLetterBackgroundColor(self.currentLetter, "transparent")
        #         self.encryptTextEdit.setText("Fin de decryption")
        #         self.encryptTextEdit.setAlignment(Qt.AlignCenter)



    def decrypter_button_clicked(self):
        # this code is just for settling up the button
        msg = self.decryptTextEdit.toPlainText()
        if len(msg) > 0:
            self.encrypterButton.setEnabled(False)
            self.decrypterButton.setEnabled(False)
            self.decrypterToggled = True
            self.encrypterToggled = False
        # the code for the decryption here

    def configRotors(self):
        ic1 = self.c1_box.value()
        ic2 = self.c2_box.value()
        ic3 = self.c3_box.value()

        if (ic1 < 0):
            self.decalage("r1", "G", ic1)
        else:
            self.decalage("r1", "D", ic1)

        if (ic2 < 0):
            self.decalage("r2", "G", ic2)
        else:
            self.decalage("r2", "D", ic2)

        if (ic3 < 0):
            self.decalage("r3", "G", ic3)
        else:
            self.decalage("r3", "D", ic3)

    def colorerChemainEncryption(self):

        self.changeLetterBackgroundColor(self.currentLetter, "red")
        self.current_b1 = ord(self.currentLetter) - 96
        self.changeBoxBackgroundColor("r1_l2_box_" + str(self.current_b1), "red")
        box1 = getattr(self, "r1_l2_box_" + str(self.current_b1))

        self.current_b2 = divmod((self.current_b1 + box1.value()), 26)[1]
        self.changeBoxBackgroundColor("r2_l2_box_" + str(self.current_b2), "red")
        box2 = getattr(self, "r2_l2_box_" + str(self.current_b2))

        self.current_b3 = divmod((self.current_b2 + box2.value()), 26)[1]
        self.changeBoxBackgroundColor("r3_l2_box_" + str(self.current_b3), "red")
        box3 = getattr(self, "r3_l2_box_" + str(self.current_b3))

        self.current_ref = divmod((self.current_b3 + box3.value()), 26)[1]
        self.changeBoxBackgroundColor("ref_box_" + str(self.current_ref), "red")
        box_curr_ref = getattr(self, "ref_box_" + str(self.current_ref))
        #------------------------------------
        self.ret_ref = divmod((self.current_ref + box_curr_ref.value()), 26)[1]
        self.changeBoxBackgroundColor("ref_box_" + str(self.ret_ref), "blue")
        box_ret_ref = getattr(self, "ref_box_" + str(self.ret_ref))

        self.ret_b3 = self.ret_ref
        self.changeBoxBackgroundColor("r3_l1_box_" + str(self.ret_b3), "blue")
        box3_ret = getattr(self, "r3_l1_box_" + str(self.ret_b3))

        self.ret_b2 = divmod((self.ret_b3 + box3_ret.value()), 26)[1]
        self.changeBoxBackgroundColor("r2_l1_box_" + str(self.ret_b2), "blue")
        box2_ret = getattr(self, "r2_l1_box_" + str(self.ret_b2))

        self.ret_b1 = divmod((self.ret_b2 + box2_ret.value()), 26)[1]
        self.changeBoxBackgroundColor("r1_l1_box_" + str(self.ret_b1), "blue")
        box1_ret = getattr(self, "r1_l1_box_" + str(self.ret_b1))

        self.ret_letter = chr( divmod(self.ret_b1 + box1_ret.value(), 26)[1] + 96)
        self.changeLetterBackgroundColor(self.ret_letter, "blue")

    def unColorChemain(self):
        # aller
        self.changeLetterBackgroundColor(self.currentLetter, "transparent")
        self.changeBoxBackgroundColor("r1_l2_box_" + str(self.current_b1), "transparent")
        self.changeBoxBackgroundColor("r2_l2_box_" + str(self.current_b2), "transparent")
        self.changeBoxBackgroundColor("r3_l2_box_" + str(self.current_b3), "transparent")
        self.changeBoxBackgroundColor("ref_box_" + str(self.current_ref), "transparent")
        # retour
        self.changeBoxBackgroundColor("r1_l1_box_" + str(self.ret_b1), "transparent")
        self.changeBoxBackgroundColor("r2_l1_box_" + str(self.ret_b2), "transparent")
        self.changeBoxBackgroundColor("r3_l1_box_" + str(self.ret_b3), "transparent")
        self.changeBoxBackgroundColor("ref_box_" + str(self.ret_ref), "transparent")
        self.changeLetterBackgroundColor(self.ret_letter, "transparent")

# running the app
app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())

# this command is for compiling the .ui file generated by the qt designer :
#                $  pyuic5 -o main_ui.py ui/qt.ui
# when we finish the app, we can convert it to executable file using this commands:
#                $  pyinstaller --onefile --windowed -i".\ui\resources\enigma.ico" ".\app.py"
