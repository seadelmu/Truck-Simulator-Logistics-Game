import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QTextEdit, QMessageBox,
                             QGroupBox, QComboBox)
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import project.game as game

"""
Truck View
UI for user managment of trucks
"""
class TruckView(QWidget):
    # This is the screen for handling trucks.
    
    switch_to_game_screen = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.g = game.GameState()
        
        self.create_layouts()
        self.create_left_panel()
        self.create_right_panel()
        
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 4)
        self.setLayout(self.main_layout)
        
        self.connect_signals()
        
        self.update_truck_buttons()

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.truck_grid_layout = QGridLayout()

    def create_left_panel(self):
        self.player_info_label = QLabel("Loading Player Info...")
        self.player_info_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        self.left_layout.addWidget(self.player_info_label)

        self.list_button = QPushButton("List All Trucks")
        self.buy_truck_button = QPushButton("Buy New Truck ($1000)")
        self.back_button = QPushButton("Back to Game Screen")
        
        self.left_layout.addWidget(self.list_button)
        self.left_layout.addWidget(self.buy_truck_button)
        self.left_layout.addWidget(self.back_button)
        self.left_layout.addStretch(1)

    def create_right_panel(self):
        self.truck_buttons = []
        for i in range(10):
            button = QPushButton("Locked")
            self.truck_grid_layout.addWidget(button, i // 5, i % 5)
            self.truck_buttons.append(button)
        
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        
        self.right_layout.addLayout(self.truck_grid_layout)
        self.right_layout.addWidget(self.output_display)

    def connect_signals(self):
        self.list_button.clicked.connect(self.list_all_trucks)
        self.buy_truck_button.clicked.connect(self.buy_new_truck)
        self.back_button.clicked.connect(self.switch_to_game_screen.emit)
        
        for i, button in enumerate(self.truck_buttons):
            button.clicked.connect(lambda _, truck_index=i: self.view_truck_info(truck_index))

    def update_player_info(self):
        player = self.g.player
        self.player_info_label.setText(str(player))
        print("Player info updated on TruckView screen.")

    def update_truck_buttons(self):
        for i, button in enumerate(self.truck_buttons):
            if i < self.g.trucks.truckCount:
                truck = self.g.trucks.getTruck(i)
                button.setText(f"{truck.truckID}")
                button.setEnabled(True)
            else:
                button.setText("Locked")
                button.setEnabled(False)

    def list_all_trucks(self):
        output = ""
        if self.g.trucks.truckCount == 0:
            output = "\nNo Trucks Exist Yet\n"
        else:
            output += "Current Fleet:\n"
            for i in range(self.g.trucks.truckCount):
                truck = self.g.trucks.getTruck(i)
                output += f"{truck}\n"
        
        self.output_display.setText(output)

    def buy_new_truck(self):
        p = self.g.player
        if self.g.trucks.truckCount >= 10:
            self.output_display.setText("You have reached the maximum number of trucks.")
            return

        if p.balance >= 1000:
            p.makePurchase(1000)
            self.g.trucks.addTruck(f"Truck {self.g.trucks.truckCount + 1}")
            self.output_display.setText(f"Purchased new truck for $1000!\nYour new balance is ${p.balance}.")
            self.update_truck_buttons()
            self.update_player_info() 
        else:
            self.output_display.setText("Insufficient Balance. A new truck costs $1000.")

    def view_truck_info(self, truck_index):
        truck = self.g.trucks.getTruck(truck_index)
        if truck:
            self.output_display.setText(str(truck))
        else:
            self.output_display.setText("Error: Truck not found.")