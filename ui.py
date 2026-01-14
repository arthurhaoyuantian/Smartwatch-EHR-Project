from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from dotenv import load_dotenv # lets us read from .env
import fitbit_auth


#Main App Window Class
class MainWindow(QWidget): 
    #define signal variable
    token_recieved = pyqtSignal(str)
    
    #constructor for MainWindow (child class)
    def __init__(self): 
        super().__init__() #constructor for QWidget (parent class)
        
        #window specs
        self.setWindowTitle("Smartwatch Data App") 
        self.resize(1366, 768)

        #widgets
        self.label = QLabel("welcome! click the app to connect to fitbit") #text label
        self.label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton("connect to fitbit") #clickable button

        #fonts
        self.largeFont = QFont("Arial", 20)
        self.smallFont = QFont("Arial", 10)
        self.label.setFont(self.largeFont)
        self.button.setFont(self.smallFont)

        #layout
        layout = QVBoxLayout() #orders widgets top to bottom
        layout.addWidget(self.label, stretch = 4) 
        layout.addWidget(self.button, stretch = 6) 
        self.setLayout(layout)
        
        #signal
        self.button.clicked.connect(self.on_login_click)
        
    
    #start auth flow on button press
    def on_login_click(self):
        self.label.setText("Attempting to connect...") #update label widget
        
        #start flask server
        fitbit_auth.start_server()
        fitbit_auth.start_auth_flow()