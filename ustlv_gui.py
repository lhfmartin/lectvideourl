from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QApplication)
from robobrowser import RoboBrowser
import re
import sys
import time




def generatelists(start, fin):
    l1 = []
    l2 = []
    for i in range(start, fin):
        t1 = str(i)
        for a in range(0, len(t1) - 1):
            appended = False
            for b in range(a + 1, len(t1)):
                if t1[a] == t1[b]:
                    appended = True
                    l1.append(i)
                    break
            if appended == True:
                break
            if a == len(t1) - 1 - 1 and appended == False:
                l2.append(i)
    return l1, l2

def trywith(l3, ccode, lectsession, date):
    lvlink = "https://rvc.ust.hk/mgmt/media.aspx?path=18FA_" + ccode + "-" + lectsession + "_" + date + "_"
    counter = 0
    for i2 in l3:
        if counter % 2 == 0 and counter != 0 and counter % 4!= 0:
            starttime = time.time()
        if counter % 4 == 0 and counter != 0:
            endtime = time.time()
            timetaken = endtime - starttime

        browser = RoboBrowser(history=True)
        browser.open(lvlink + str(i2))
        form = browser.get_form(id="fm1")
        form["username"].value = #Type username here
        form["password"].value = #Type password here

        browser.submit_form(form)
        htmlsource = str(browser.parsed)
        relist = re.findall("System error encount", htmlsource)
        if(len(relist) != 0):
            print("False", "(" + str(l3[counter]) + ")")
            p = round(counter / len(l3) * 100, 2)
            print(str(p) + "%")
        else:
            print("Done!", "Link: " + lvlink + str(i2))
            return (lvlink + str(i2))
        if counter > 4:
            eta = (len(l3) - counter) / 2 * timetaken
            print("ETA:", str(int(eta / 60)) + "m" + str(int(eta % 60)) + "s")
        counter += 1
    return False

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        coursecode = QLabel("Course Code:")
        self.coursecodeinput = QLineEdit()
        self.coursecodeinput.returnPressed.connect(self.startfn)
        lectureses = QLabel("Lecture Session:")
        self.lecturesesinput = QLineEdit()
        self.lecturesesinput.returnPressed.connect(self.startfn)
        date = QLabel("Date (YYMMDD):")
        self.dateinput = QLineEdit()
        self.dateinput.returnPressed.connect(self.startfn)
        starti = QLabel("Start:")
        self.startiinput = QLineEdit("10000")
        self.startiinput.returnPressed.connect(self.startfn)
        endi = QLabel("End:")
        self.endiinput = QLineEdit("100000")
        self.endiinput.returnPressed.connect(self.startfn)
        startbutton = QPushButton("Start", self)
        startbutton.clicked.connect(self.startfn)
        self.lvurl = QTextEdit("The link will appear here.")
        self.lvurl.setReadOnly(True)
        self.lvurl.setStyleSheet("background-color: rgba(0, 0, 0, 0);")


        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(coursecode, 1, 0)
        grid.addWidget(self.coursecodeinput, 1, 1)
        grid.addWidget(lectureses, 2, 0)
        grid.addWidget(self.lecturesesinput, 2, 1)
        grid.addWidget(date, 3, 0)
        grid.addWidget(self.dateinput, 3, 1)
        grid.addWidget(starti, 4, 0)
        grid.addWidget(self.startiinput, 4, 1)
        grid.addWidget(endi, 5, 0)
        grid.addWidget(self.endiinput, 5, 1)
        grid.addWidget(startbutton, 6, 0, 1, 2)
        grid.addWidget(self.lvurl, 7, 0, 1, 2)

        self.setLayout(grid)
        self.setGeometry(450, 450, 300, 340)
        self.setWindowTitle("Get Lecture Video Link")
        self.show()

    def startfn(self):
        if int(self.startiinput.text()) >= int(self.endiinput.text()):
            self.lvurl.setText("Invalid indexes")
            QApplication.processEvents()
            self.lvurl.update()
            return
        l1, l2 = generatelists(int(self.startiinput.text()), int(self.endiinput.text()))
        x1 = trywith(l1, self.coursecodeinput.text(), self.lecturesesinput.text(), self.dateinput.text())
        if(not x1):
            x2 = trywith(l2, self.coursecodeinput.text(), self.lecturesesinput.text(), self.dateinput.text())
            if(not x2):
                self.lvurl.setText("Error 404")
                QApplication.processEvents()
                self.lvurl.update()
            else:
                self.lvurl.setText(x2)
                QApplication.processEvents()
                self.lvurl.update()
        else:
            self.lvurl.setText(x1)
            QApplication.processEvents()
            self.lvurl.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appgui = GUI()
    sys.exit(app.exec_())
