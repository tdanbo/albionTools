import sys
import os
from functionOne import *
#from texImport.functionTwo import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import time

scriptpath = os.path.split((os.path.abspath(__file__)))[0]

app = QApplication(sys.argv)

class window(QWidget):
    def __init__(self):
        super(window, self).__init__(None, Qt.WindowStaysOnTopHint)
        # create a PyQt application object
        

        # button widget
        tb1 = QPushButton("FUNCTION 1")
        tb2 = QPushButton("FUNCTION 2")
        tb1.clicked.connect(self.testFunc)
        #tb2.clicked.connect(self.testFuncTwo)
        self.lineedit = QLineEdit()

        tb1.setFixedSize(600,50)
        tb2.setFixedSize(600,50)

        vbox = QVBoxLayout()
        vbox.addWidget(tb1)
        vbox.addWidget(tb2)
        vbox.addWidget(self.lineedit)
        self.setLayout(vbox)
        #vbox.addWidget(tableItem)

        
    def testFunc(self):
        dataOne, dataTwo = funcOne()
        print dataOne
        print dataTwo
        self.lineedit.setText(dataOne+" "+dataTwo)

#    def testFuncTwo(self):
#        initdata = funcTwo()
#        print initdata
#        self.lineedit.setText(initdata)


panel = window()
panel.show()
sys.exit(app.exec_())


