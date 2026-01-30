import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QTextEdit, QMessageBox,
                             QGroupBox, QComboBox, QListWidget)
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import project.game as game

"""
GameScreen
Main Game control screen for user functions
"""
class GameScreen(QWidget):
    # This is the second screen with 9 horizontal buttons.
    
    switch_to_truck_view = pyqtSignal()
    switch_to_product_view = pyqtSignal()
    switch_to_order_view = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.g = game.GameState()

        self.main_game_layout = QVBoxLayout(self)
        self.top_section_layout = QHBoxLayout()
        self.lists_layout = QHBoxLayout()

        # Player info
        self.player_info_label = QLabel("Loading Player Info...")
        self.player_info_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

        # Day info
        self.day_label = QLabel(f"Day: {self.g.day}")
        self.day_label.setStyleSheet("font-size: 14px; color: #444; margin-top: 5px;")

        # Group labels vertically
        player_info_layout = QVBoxLayout()
        player_info_layout.addWidget(self.player_info_label)
        player_info_layout.addWidget(self.day_label)

        self.top_section_layout.addLayout(player_info_layout, 1)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.initButton()
        self.top_section_layout.addLayout(self.button_layout, 2)

        # Assemble layout
        self.main_game_layout.addLayout(self.top_section_layout)

        self.active_orders_list = QListWidget()
        self.active_orders_list.setStyleSheet("font-size: 14px; padding: 5px;")
        self.active_orders_list.setWordWrap(True)

        self.product_queue_list = QListWidget()
        self.product_queue_list.setStyleSheet("font-size: 14px; padding: 5px;")
        self.product_queue_list.setWordWrap(True)

        self.message_log = QListWidget()
        self.message_log.setStyleSheet("font-size: 14px; padding: 5px;")
        self.message_log.setWordWrap(True)

        self.lists_layout.addWidget(self.active_orders_list)
        self.lists_layout.addWidget(self.product_queue_list)
        self.lists_layout.addWidget(self.message_log)

        self.main_game_layout.addLayout(self.lists_layout)

        self.setLayout(self.main_game_layout)

    def initButton(self):
        """Initializes and adds the command buttons to the layout."""
        button_labels = [
            "View Orders", "View Trucks", "View Products",
            "Next Day", "Empty", "Empty", "Empty", "Empty", "Exit Game"
        ]
        for i, label in enumerate(button_labels, 1):
            button = QPushButton(label)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(lambda _, index=i: self.handle_button_click(index))
            self.button_layout.addWidget(button)
            
    def update_player_info(self):
        player = self.g.player
        self.player_info_label.setText(str(player))
        self.day_label.setText(f"Day: {self.g.day}")
        self.update_active_orders()
        self.update_product_queue()
        self.update_message_log()
        print("Player info, day, and active orders updated on GameScreen.")

    def update_active_orders(self):
        self.active_orders_list.clear()
        active_orders = [order for order in self.g.getAcceptedOrders() if order]

        if not active_orders:
            self.active_orders_list.addItem("No active orders.")
            return

        for order in active_orders:
            if order:
                display = f"{order.name} - {order.purchaseProduct.name} x{order.purchasedAmount} to {order.orderDestination} ({order.expReward} EXP [Time Remaining: {order.assignedTruck.daysRemaining}])"
                self.active_orders_list.addItem(display)

    def update_product_queue(self):
        self.product_queue_list.clear()

        queue = self.g.productFactory.getProductList()

        if not queue.productQueue:
            self.product_queue_list.addItem("Nothing in production")
            return

        for i, product in enumerate(queue.productQueue):
            display = f"Product: {product.name} | Quantity: 100 | Due in {i+1} day"
            self.product_queue_list.addItem(display)

    def update_message_log(self):
        self.message_log.clear()

        log = self.g.messageLog.get_message_log()

        if not log:
            self.message_log.addItem("Log empty")
            return
        
        for message in log:
            if message:
                self.message_log.addItem(message)

        

    def handle_button_click(self, button_index):
        print(f"Button '{self.sender().text()}' was clicked!")
        match button_index:
            case 1:
                print("Viewing orders...")
                self.switch_to_order_view.emit()
            case 2:
                print("Viewing trucks...")
                self.switch_to_truck_view.emit()
            case 3:
                print("Viewing products...")
                self.switch_to_product_view.emit()
            case 4:
                print("Next day")
                g = game.GameState()
                g.nextDay()
                self.update_player_info()

            case 9:
                print("Exiting the game.")
                QApplication.instance().quit()
            case _:
                print(f"Option {button_index} selected (no specific action yet).")

