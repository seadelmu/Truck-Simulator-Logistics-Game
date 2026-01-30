import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QTextEdit, QMessageBox,
                             QGroupBox, QComboBox)
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import project.game as game

"""
OrderView
Screen for viewing and managing orders
"""
class OrderView(QWidget):
    # Screen for viewing order and managing them
    
    switch_to_game_screen = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.g = game.GameState()
        self.selected_order = None
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.addLayout(self.create_sidebar(), 2)
        layout.addLayout(self.create_main_area(), 2)
        self.setLayout(layout)

    def create_sidebar(self):
        sidebar = QVBoxLayout()
        back_button = QPushButton("Back to Game")
        back_button.clicked.connect(self.switch_to_game_screen.emit)
        sidebar.addWidget(back_button)
        sidebar.addStretch()
        return sidebar

    def create_main_area(self):
        self.main_area = QVBoxLayout()

        # Sections for available and accepted orders
        self.available_orders_layout = QVBoxLayout()
        self.accepted_orders_layout = QVBoxLayout()

        self.main_area.addWidget(QLabel("Available Orders"))
        self.main_area.addLayout(self.available_orders_layout)

        self.main_area.addWidget(QLabel("Accepted Orders"))
        self.main_area.addLayout(self.accepted_orders_layout)

        # Detailed view + accept controls
        self.details_box = self.create_order_details_box()
        self.main_area.addWidget(self.details_box)

        self.populate_orders()
        return self.main_area

    def create_order_details_box(self):
        group = QGroupBox("Order Details")
        layout = QVBoxLayout()

        self.details_label = QLabel("Select an order to view details.")
        self.accept_button = QPushButton("Accept Order")
        self.accept_button.clicked.connect(self.accept_order)
        self.accept_button.setEnabled(False)

        self.truck_combo = QComboBox()
        self.truck_combo.setEnabled(False)

        layout.addWidget(self.details_label)
        layout.addWidget(QLabel("Assign Truck:"))
        layout.addWidget(self.truck_combo)
        layout.addWidget(self.accept_button)

        group.setLayout(layout)
        return group
    
    def create_sidebar(self):
        sidebar = QVBoxLayout()

        back_button = QPushButton("Back to Game")
        back_button.clicked.connect(self.switch_to_game_screen.emit)
        sidebar.addWidget(back_button)

        sidebar.addSpacing(10)

        self.product_info_label = QLabel("Product Info:")
        self.product_info_label.setStyleSheet("font-weight: bold;")
        sidebar.addWidget(self.product_info_label)

        self.product_info_display = QTextEdit()
        self.product_info_display.setReadOnly(True)
        self.product_info_display.setPlaceholderText("Select an order to view product info...")
        sidebar.addWidget(self.product_info_display)

        sidebar.addStretch()
        return sidebar

    def populate_orders(self):
        self.clear_layout(self.available_orders_layout)
        self.clear_layout(self.accepted_orders_layout)

        # Add available orders (from orders list)
        for order in self.g.getOrders():
            if order is None:
                continue

            button = QPushButton(f"{order.name} - {order.purchaseProduct.name} x{order.purchasedAmount}")
            button.clicked.connect(lambda checked, o=order: self.view_order(o))
            self.available_orders_layout.addWidget(button)

        # Add accepted orders (from acceptedOrders list)
        for order in self.g.getAcceptedOrders():
            if order is None:
                continue

            button = QPushButton(f"{order.name} (Accepted) - {order.purchaseProduct.name} x{order.purchasedAmount}")
            button.clicked.connect(lambda checked, o=order: self.view_order(o))
            self.accepted_orders_layout.addWidget(button)

    def view_order(self, order):
        if order is None:
            self.selected_order = None
            self.details_label.setText("Select an order to view details.")
            self.accept_button.setEnabled(False)
            self.truck_combo.clear()
            self.truck_combo.setEnabled(False)
            return

        self.selected_order = order
        product = order.purchaseProduct
        destination = order.orderDestination

        # Get travel time from GameState.destinations
        travel_time = self.g.destinations.travelTimes.get(destination, "Unknown")

        # Display Text for product
        product_info = (
            f"Name: {product.name}\n"
            f"Price: ${product.price:.2f}\n"
            f"Stock: {product.quantity}\n"
            f"Production Cost: ${product.productionCost:.2f}\n"
            f"Description: {product.description}"
        )
        self.product_info_display.setText(product_info)

        # Display text for order
        info = (
            f"Name: {order.name}\n"
            f"Product: {product.name}\n"
            f"Amount: {order.purchasedAmount}\n"
            f"Destination: {destination}\n"
            f"Travel Time: {travel_time} days\n"
            f"Price: ${order.orderPrice:.2f}\n"
            f"EXP: {order.expReward}\n"
            f"Status: {'Accepted' if order.accepted else 'Available'}"
        )
        self.details_label.setText(info)


        if not order.accepted:
            self.accept_button.setEnabled(True)
            self.truck_combo.setEnabled(True)
            self.populate_truck_combo()
        else:
            self.accept_button.setEnabled(False)
            self.truck_combo.setEnabled(False)


    def populate_truck_combo(self):
        self.truck_combo.clear()
        trucks = self.g.trucks.trucks
        for truck in trucks:
            if truck and truck.status == 0:
                self.truck_combo.addItem(f"Truck {truck.truckID}", truck)

        if self.truck_combo.count() == 0:
            self.truck_combo.addItem("No available trucks", None)
            self.accept_button.setEnabled(False)


    def accept_order(self):
        if self.selected_order is None:
            return

        truck = self.truck_combo.currentData()
        if truck is None:
            QMessageBox.warning(self, "No Truck", "No truck available to assign.")
            return

        # Get destination and travel time
        destination = self.selected_order.orderDestination
        travel_time = self.g.destinations.travelTimes.get(destination, 0)
        product = self.selected_order.purchaseProduct.name
        product_amount = self.selected_order.purchasedAmount

        # Assign truck
        truck.loadTruck(product, product_amount)
        truck.startDelivery(destination, travel_time)
        self.selected_order.assignedTruck = truck

        # Sell product (reduce stock)
        sellErr = self.selected_order.purchaseProduct.sell(self.selected_order.purchasedAmount)

        if sellErr != 1:
            QMessageBox.warning(self, "Order Error", "Not enough product stock to accept order")
            return
        
        # Move to accepted orders
        success = self.g.acceptOrder(self.selected_order)
        if not success:
            QMessageBox.warning(self, "Order Error", "Failed to accept the order.")
            return

        # Refresh UI
        self.populate_orders()
        self.product_info_display.setText("")
        self.view_order(self.selected_order)

        message = f"Accepted Order: {self.selected_order}"
        self.g.messageLog.add_message(message)

        
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def refresh_orders_view(self):
        self.populate_orders()
        self.selected_order = None
        self.details_label.setText("Select an order to view details.")
        self.accept_button.setEnabled(False)
        self.truck_combo.clear()
        self.truck_combo.setEnabled(False)
