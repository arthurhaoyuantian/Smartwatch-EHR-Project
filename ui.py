from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QFont
from dotenv import load_dotenv # lets us read from .env
import fitbit_auth


# creates custom window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__() # call the constructor of QWidget
        
        # ~ QWidget is the base class for all the objects relating to UI 
        
        #creating app window
        self.setWindowTitle("Smartwatch Data App") #title at the top of window
        self.resize(1366, 768)

        #creates widgets
        self.label = QLabel("welcome! click the app to connect to fitbit") #just text
        self.label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton("connect to fitbit") #clickable button

        #fonts
        self.largeFont = QFont("Arial", 20)
        self.smallFont = QFont("Arial", 10)
        self.label.setFont(self.largeFont)
        self.button.setFont(self.smallFont)

        #Start the Flask Server
        fitbit_auth.start_server()

        # ~ this is the function that will run when the button is clicked 

        #connect the signal of the button being clicked to our function
        self.button.clicked.connect(self.on_login_click)

        # box layout makes widgets go top to bottom instead of stacking on top of each other which is the default
        layout = QVBoxLayout()
        layout.addWidget(self.label, stretch = 4) # adds the label first, then the button. so button is under
        layout.addWidget(self.button, stretch = 6) # expand the widgets, stretch is how much they expand

        self.setLayout(layout)
        
    # runs when the button is pressed
    def on_login_click(self):
        print("login button pressed") #print this to the terminal
        self.label.setText("Attempting to connect...") # updates label text
        fitbit_auth.start_auth_flow()