import sys #for interacting with the python interpreter eg. exit()
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

#create an "app" object. manages event loop, argv links my code with the terminal
app = QApplication(sys.argv) 

#assign layout from ui.py to our window and display it
window = MainWindow()
window.show()

#starts event loop (waiting for clicks and stuff)
sys.exit(app.exec_())