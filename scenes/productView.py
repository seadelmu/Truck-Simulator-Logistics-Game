import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QTextEdit, QMessageBox,
                             QGroupBox, QComboBox)
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import project.game as game

"""
Product View
UI for user management of the products throughout gameplay
"""
class ProductView(QWidget):
    #  This screen displays information about different products.
    
    switch_to_game_screen = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.g = game.GameState()
        self.current_product = None
        self.buy_quantity = 100
        
        # Product references
        self.low_quality_oil = self.g.products.low_quality_oil
        self.mid_quality_oil = self.g.products.mid_quality_oil
        self.high_quality_oil = self.g.products.high_quality_oil
        
        self.create_layouts()
        self.create_left_panel()
        self.create_right_panel()
        self.connect_signals()
        
        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addLayout(self.right_layout, 4)
        self.setLayout(self.main_layout)

        self.update_product_buttons()
        self.update_player_info()
        self.buy_stock_button.setEnabled(False)

    def create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

    def create_left_panel(self):
        self.player_info_label = QLabel("Loading Player Info...")
        self.player_info_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        self.left_layout.addWidget(self.player_info_label)

        self.low_button = QPushButton("Low Quality Oil")
        self.mid_button = QPushButton("Mid Quality Oil")
        self.high_button = QPushButton("High Quality Oil")
        
        self.buy_stock_button = QPushButton("Buy Stock")
        self.buy_stock_button.setEnabled(False)
        
        self.back_button = QPushButton("Back to Game Screen")

        self.left_layout.addWidget(self.low_button)
        self.left_layout.addWidget(self.mid_button)
        self.left_layout.addWidget(self.high_button)
        self.left_layout.addWidget(self.buy_stock_button)
        self.left_layout.addStretch(1)
        self.left_layout.addWidget(self.back_button)

    def create_right_panel(self):
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Select a product to view its information...")
        self.right_layout.addWidget(self.output_display)

    def connect_signals(self):
        self.low_button.clicked.connect(lambda: self.view_product_info(self.low_quality_oil))
        self.mid_button.clicked.connect(lambda: self.view_product_info(self.mid_quality_oil))
        self.high_button.clicked.connect(lambda: self.view_product_info(self.high_quality_oil))
        self.back_button.clicked.connect(self.switch_to_game_screen.emit)
        self.buy_stock_button.clicked.connect(self.buy_new_stock)

    def update_player_info(self):
        player = self.g.player
        self.player_info_label.setText(str(player))

    def update_product_buttons(self):
        player_level = self.g.player.getLevel()

        self.low_button.setEnabled(True)

        if player_level >= 10:
            self.mid_button.setEnabled(True)
            self.mid_button.setText("Mid Quality Oil")
        else:
            self.mid_button.setEnabled(False)
            self.mid_button.setText("Mid Quality Oil (Lvl 10)")

        if player_level >= 20:
            self.high_button.setEnabled(True)
            self.high_button.setText("High Quality Oil")
        else:
            self.high_button.setEnabled(False)
            self.high_button.setText("High Quality Oil (Lvl 20)")

    def view_product_info(self, product):
        self.current_product = product
        self.buy_stock_button.setEnabled(True)

        purchase_cost = product.productionCost * self.buy_quantity
        self.buy_stock_button.setText(f"Buy {self.buy_quantity} Stock (${purchase_cost:.2f})")

        info = f"{product}\n\nDescription:\n{product.description}"
        self.output_display.setText(info)
        
    def buy_new_stock(self):
        if not self.current_product:
            self.output_display.setText("Error: No product selected.")
            return

        player = self.g.player
        quantity_to_buy = self.buy_quantity
        total_price = self.current_product.productionCost * quantity_to_buy
        productFactory = self.g.productFactory

        if player.balance < total_price:
            self.output_display.setText(f"Insufficient Balance. A purchase of {quantity_to_buy} stock costs ${total_price:.2f}.")
            return
        
        # Make purchase and add product to the productFactory queue
        player.makePurchase(total_price)
        productFactory.appendProduct(self.current_product, quantity_to_buy)

        # Update player info and refresh product info display
        self.update_player_info()
        self.view_product_info(self.current_product)

        message = f"Product: {self.current_product.name} | Quantity: {quantity_to_buy} | Queued for production"
        self.g.messageLog.add_message(message)

    def reset_view(self):
        self.current_product = None
        self.output_display.clear()
        self.output_display.setPlaceholderText("Select a product to view its information...")
        self.buy_stock_button.setEnabled(False)
        self.buy_stock_button.setText("Buy Stock")