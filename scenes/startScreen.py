import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QTextEdit, QMessageBox,
                             QGroupBox, QComboBox)
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import project.game as games
import project.objects as obj


"""
Start Screen Object
Functions as the main menu of the game
"""
class StartScreen(QWidget):
    # This is the first screen with 'Start Game' and 'Exit Game' buttons.
    
    switch_to_game = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.create_widgets()
        self.create_layout()
        self.connect_signals()

    def create_widgets(self):
        # Creates the widgets for the start screen.

        self.label = QLabel("Main Menu")
        self.label.setStyleSheet("font-size: 24px;")
        
        self.start_button = QPushButton("Start Game")
        self.start_button.setStyleSheet("font-size: 18px;")
        
        self.exit_button = QPushButton("Exit Game")
        self.exit_button.setStyleSheet("font-size: 18px;")

    def create_layout(self):
        # Arranges the widgets in a vertical layout.

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.exit_button)
        self.setLayout(self.layout)

    def connect_signals(self):
        # Connects the buttons to their actions.

        self.start_button.clicked.connect(self.switch_to_game.emit)
        self.exit_button.clicked.connect(QApplication.instance().quit)