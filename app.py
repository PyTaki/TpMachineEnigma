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
        self.currentState = {"letter": "",
                             "index": 0,
                             "b1": 0,
                             "b2": 0,
                             "ref": 0,
                             "b3": 0,
                             "ret_b1": 0,
                             "ret_b2": 0,
                             "ret_b3": 0,
                             "ret_ref": 0,
                             "ret_letter": ""}

        self.initialState = {}
        self.encrypterToggled = False
        self.decrypterToggled = False

        self.rotorAdecaler = None

        self.setupUi(self)
        self.InitialRotorState()
        self.disableConfigs()
        # --------------------
        self.configurerButton.clicked.connect(self.configurer_button_clicked)
        self.encrypterButton.clicked.connect(self.encypter_button_clicked)
        self.decrypterButton.clicked.connect(self.decrypter_button_clicked)
        self.suivantButton.clicked.connect(self.suivant_button_clicked)

    # ------ Utils ------
    def InitialRotorState(self):
        for i in range(1, 27, 1):
            for j in range(1, 4, 1):
                for k in range(1, 3, 1):
                    box = "r" + str(j) + "_l" + str(k) + "_box_" + str(i)
                    self.initialState[box] = getattr(self, box).value()

    def setInitialRotorSate(self):
        for i in range(1, 27, 1):
            for j in range(1, 4, 1):
                for k in range(1, 3, 1):
                    box = "r" + str(j) + "_l" + str(k) + "_box_" + str(i)
                    getattr(self, box).setProperty("value", self.initialState[box])

    '''it sets the rotors and the reflecteur on readOnly mode'''

    def disableConfigs(self):
        for i in range(1, 4, 1):
            getattr(self, "c" + str(i) + "_DG").setEnabled(False)
            getattr(self, "c" + str(i) + "_R").setEnabled(False)
            getattr(self, "c" + str(i) + "_box").setEnabled(False)

        # for i in range(1, 27, 1):
        #     for j in range(1, 4, 1):
        #         for k in range(1, 3, 1):
        #             getattr(self, "r" + str(j) + "_l" + str(k) + "_box_" + str(i)).setReadOnly(True)
        #             getattr(self, "r" + str(j) + "_l" + str(k) + "_box_" + str(i)).setButtonSymbols(QAbstractSpinBox.NoButtons)

    '''it sets the rotors and the reflecteur on Edit mode'''

    def enableConfigs(self):
        for i in range(1, 4, 1):
            getattr(self, "c" + str(i) + "_DG").setEnabled(True)
            getattr(self, "c" + str(i) + "_R").setEnabled(True)
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
            self.setInitialRotorSate()
            self.disableConfigs()
            self.configRotors()
            self.configurerButton.setText("Configurer Rotors")

    def encypter_button_clicked(self):
        # this code is just for settling up the button
        msg = self.encryptTextEdit.toPlainText().lower()
        if len(msg) > 0:
            self.encrypterButton.setEnabled(False)
            self.decrypterButton.setEnabled(False)
            self.encrypterToggled = True
            self.decrypterToggled = False
            self.decryptTextEdit.clear()
        #--------------------------
        # txt = ""
        # i=0
        # while(i < len(msg)):
        #     self.currentState["letter"] = msg[i]
        #     if self.currentState["letter"] != " ":
        #         self.currentState["b1"] = ord(self.currentState["letter"]) - 96
        #         box1 = getattr(self, "r1_l2_box_" + str(self.currentState["b1"]))
        #
        #         self.currentState["b2"] = divmod((self.currentState["b1"] + box1.value()), 26)[1] if divmod((self.currentState["b1"] + box1.value()), 26)[1] != 0 else 26
        #
        #         box2 = getattr(self, "r2_l2_box_" + str(self.currentState["b2"]))
        #
        #         self.currentState["b3"] = divmod((self.currentState["b2"] + box2.value()), 26)[1] if divmod((self.currentState["b2"] + box2.value()), 26)[1] != 0 else 26
        #         box3 = getattr(self, "r3_l2_box_" + str(self.currentState["b3"]))
        #
        #         self.currentState["ref"] = divmod((self.currentState["b3"] + box3.value()), 26)[1] if divmod((self.currentState["b3"] + box3.value()), 26)[1] != 0 else 26
        #         box_curr_ref = getattr(self, "ref_box_" + str(self.currentState["ref"]))
        #
        #         # ------------------------------------
        #         self.currentState["ret_ref"] = divmod((self.currentState["ref"] + box_curr_ref.value()), 26)[1] if divmod((self.currentState["ref"] + box_curr_ref.value()), 26)[1] != 0 else 26
        #         # box_ret_ref = getattr(self, "ref_box_" + str(self.currentState["ret_ref"]))
        #
        #         self.currentState["ret_b3"] = self.currentState["ret_ref"]
        #         box3_ret = getattr(self, "r3_l1_box_" + str(self.currentState["ret_b3"]))
        #
        #         self.currentState["ret_b2"] = divmod((self.currentState["ret_b3"] + box3_ret.value()), 26)[1] if divmod((self.currentState["ret_b3"] + box3_ret.value()), 26)[1] != 0 else 26
        #         box2_ret = getattr(self, "r2_l1_box_" + str(self.currentState["ret_b2"]))
        #
        #         self.currentState["ret_b1"] = divmod((self.currentState["ret_b2"] + box2_ret.value()), 26)[1] if divmod((self.currentState["ret_b2"] + box2_ret.value()), 26)[1] != 0 else 26
        #         box1_ret = getattr(self, "r1_l1_box_" + str(self.currentState["ret_b1"]))
        #
        #         tmp = divmod(self.currentState["ret_b1"] + box1_ret.value(), 26)[1] if divmod((self.currentState["ret_b1"] + box1_ret.value()), 26)[1] != 0 else 26
        #         self.currentState["ret_letter"] = chr(tmp + 96)
        #     else:
        #         self.currentState["ret_letter"] = " "
        #     i += 1
        #     txt += self.currentState["ret_letter"]
        #
        # self.decryptTextEdit.setText(txt)
        # self.decryptTextEdit.setAlignment(Qt.AlignCenter)

    def suivant_button_clicked(self):
        # switch: encrypter ou decrypter
        if self.encrypterToggled:
            msg = self.encryptTextEdit.toPlainText().lower()
            if self.currentState["index"] < len(msg):
                #uncolor the previous chemain
                if self.currentState["index"] > 0:
                    self.unColorChemain()
                #colorate the current chemain
                self.currentState["letter"] = msg[self.currentState["index"]]
                self.colorerChemain()
                # ----------------------------------
                if self.currentState["letter"] != " ":
                    txt = self.decryptTextEdit.toPlainText()
                    txt += self.currentState["ret_letter"]
                    self.decryptTextEdit.setText(txt)
                    self.decryptTextEdit.setAlignment(Qt.AlignCenter)

                    # decalage par une position
                    index = self.currentState["index"] % 72
                    if index < 26:
                        rotor = self.c1_R.currentText().lower()
                    elif (index >= 26) & (index < 52):
                        rotor = self.c2_R.currentText().lower()
                    elif index >= 52:
                        rotor = self.c3_R.currentText().lower()

                    direction = self.c1_DG.currentText()
                    self.decalage(rotor,direction,1)

                else:
                    txt = self.decryptTextEdit.toPlainText()
                    txt += " "
                    self.decryptTextEdit.setText(txt)
                    self.decryptTextEdit.setAlignment(Qt.AlignCenter)
                # ----------------------------------
                self.currentState["index"] += 1

            else:
                self.currentState["index"] = 0
                self.encrypterButton.setEnabled(True)
                self.decrypterButton.setEnabled(True)
                self.decrypterToggled = False
                self.encrypterToggled = False
                # self.decryptTextEdit.setText("Fin D'encryption")
                self.unColorChemain()
                self.decryptTextEdit.setAlignment(Qt.AlignCenter)
        #
        elif self.decrypterToggled:
            msg = self.decryptTextEdit.toPlainText().lower()
            if self.currentState["index"] < len(msg):
                # uncolor the previous chemain
                if self.currentState["index"] > 0:
                    self.unColorChemain()
                # colorate the current chemain
                self.currentState["letter"] = msg[self.currentState["index"]]
                self.colorerChemain()
                #-----------------------------------
                # if self.currentState["letter"] != " ":
                #     txt = self.encryptTextEdit.toPlainText()
                #     txt += self.currentState["letter"]
                #     self.encryptTextEdit.setText(txt)
                #     self.encryptTextEdit.setAlignment(Qt.AlignCenter)
                # else:
                #     txt = self.encryptTextEdit.toPlainText()
                #     txt += " "
                #     self.encryptTextEdit.setText(txt)
                #     self.encryptTextEdit.setAlignment(Qt.AlignCenter)
                #----------------------------------
                self.currentState["index"] += 1

            else:
                self.currentState["index"] = 0
                self.encrypterButton.setEnabled(True)
                self.decrypterButton.setEnabled(True)
                self.decrypterToggled = False
                self.encrypterToggled = False
                # self.encryptTextEdit.setText("Fin de decryption")
                self.unColorChemain()
                self.encryptTextEdit.setAlignment(Qt.AlignCenter)

    def decrypter_button_clicked(self):
        # this code is just for settling up the button
        msg = self.decryptTextEdit.toPlainText().lower()
        if len(msg) > 0:
            self.encrypterButton.setEnabled(False)
            self.decrypterButton.setEnabled(False)
            self.decrypterToggled = True
            self.encrypterToggled = False
            self.decryptTextEdit.clear()
        # the code for the decryption here

    # ---------------------------------
    def configRotors(self):
        r1 = self.c1_R.currentText().lower
        r2 = self.c2_R.currentText().lower
        r3 = self.c3_R.currentText().lower
        ic1 = self.c1_box.value()
        ic2 = self.c2_box.value()
        ic3 = self.c3_box.value()

        if (ic1 < 0):
            self.decalage(r1, "G", ic1)
        else:
            self.decalage(r1, "D", ic1)

        if (ic2 < 0):
            self.decalage(r2, "G", ic2)
        else:
            self.decalage(r2, "D", ic2)

        if (ic3 < 0):
            self.decalage(r3, "G", ic3)
        else:
            self.decalage(r3, "D", ic3)

    def colorerChemain(self):
        if self.currentState["letter"] != " ":
            self.changeLetterBackgroundColor(self.currentState["letter"], "red")
            self.currentState["b1"] = ord(self.currentState["letter"]) - 96
            self.changeBoxBackgroundColor("r1_l2_box_" + str(self.currentState["b1"]), "red")
            box1 = getattr(self, "r1_l2_box_" + str(self.currentState["b1"]))
            self.currentState["b2"] = divmod((self.currentState["b1"] + box1.value()), 26)[1] if  divmod((self.currentState["b1"] + box1.value()), 26)[1] != 0 else 26

            self.changeBoxBackgroundColor("r2_l2_box_" + str(self.currentState["b2"]), "red")
            box2 = getattr(self, "r2_l2_box_" + str(self.currentState["b2"]))

            self.currentState["b3"] = divmod((self.currentState["b2"] + box2.value()), 26)[1] if  divmod((self.currentState["b2"] + box2.value()), 26)[1] != 0 else 26
            self.changeBoxBackgroundColor("r3_l2_box_" + str(self.currentState["b3"]), "red")
            box3 = getattr(self, "r3_l2_box_" + str(self.currentState["b3"]))

            self.currentState["ref"] = divmod((self.currentState["b3"] + box3.value()), 26)[1] if  divmod((self.currentState["b3"] + box3.value()), 26)[1] != 0 else 26
            self.changeBoxBackgroundColor("ref_box_" + str(self.currentState["ref"]), "red")
            box_curr_ref = getattr(self, "ref_box_" + str(self.currentState["ref"]))
            # ------------------------------------
            self.currentState["ret_ref"] = divmod((self.currentState["ref"] + box_curr_ref.value()), 26)[1] if  divmod((self.currentState["ref"] + box_curr_ref.value()), 26)[1] != 0 else 26
            self.changeBoxBackgroundColor("ref_box_" + str(self.currentState["ret_ref"]), "blue")
            # box_ret_ref = getattr(self, "ref_box_" + str(self.currentState["ret_ref"]))

            self.currentState["ret_b3"] = self.currentState["ret_ref"]
            self.changeBoxBackgroundColor("r3_l1_box_" + str(self.currentState["ret_b3"]), "blue")
            box3_ret = getattr(self, "r3_l1_box_" + str(self.currentState["ret_b3"]))

            self.currentState["ret_b2"] = divmod((self.currentState["ret_b3"] + box3_ret.value()), 26)[1] if  divmod((self.currentState["ret_b3"] + box3_ret.value()), 26)[1] != 0 else 26
            self.changeBoxBackgroundColor("r2_l1_box_" + str(self.currentState["ret_b2"]), "blue")
            box2_ret = getattr(self, "r2_l1_box_" + str(self.currentState["ret_b2"]))

            self.currentState["ret_b1"] = divmod((self.currentState["ret_b2"] + box2_ret.value()), 26)[1] if divmod((self.currentState["ret_b2"] + box2_ret.value()), 26)[1] != 0 else 26
            self.changeBoxBackgroundColor("r1_l1_box_" + str(self.currentState["ret_b1"]), "blue")
            box1_ret = getattr(self, "r1_l1_box_" + str(self.currentState["ret_b1"]))

            tmp = divmod(self.currentState["ret_b1"] + box1_ret.value(), 26)[1] if divmod((self.currentState["ret_b1"] + box1_ret.value()), 26)[1] != 0 else 26
            self.currentState["ret_letter"] = chr( tmp + 96)
            self.changeLetterBackgroundColor(self.currentState["ret_letter"], "blue")

    def unColorChemain(self):
        # aller
        if self.currentState["letter"] != " ":
            self.changeLetterBackgroundColor(self.currentState["letter"], "transparent")
            self.changeBoxBackgroundColor("r1_l2_box_" + str(self.currentState["b1"]), "transparent")
            self.changeBoxBackgroundColor("r2_l2_box_" + str(self.currentState["b2"]), "transparent")
            self.changeBoxBackgroundColor("r3_l2_box_" + str(self.currentState["b3"]), "transparent")
            self.changeBoxBackgroundColor("ref_box_" + str(self.currentState["ref"]), "transparent")
            # retour
            self.changeBoxBackgroundColor("r1_l1_box_" + str(self.currentState["ret_b1"]), "transparent")
            self.changeBoxBackgroundColor("r2_l1_box_" + str(self.currentState["ret_b2"]), "transparent")
            self.changeBoxBackgroundColor("r3_l1_box_" + str(self.currentState["ret_b3"]), "transparent")
            self.changeBoxBackgroundColor("ref_box_" + str(self.currentState["ret_ref"]), "transparent")
            self.changeLetterBackgroundColor(self.currentState["ret_letter"], "transparent")

# running the app
app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())

# this command is for compiling the .ui file generated by the qt designer :
#                $  pyuic5 -o main_ui.py ui/qt.ui
# when we finish the app, we can convert it to executable file using this commands:
#                $  pyinstaller --onefile --windowed -i".\ui\resources\enigma.ico" ".\app.py"
