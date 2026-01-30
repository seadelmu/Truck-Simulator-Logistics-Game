import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QTextEdit, QMessageBox,
                             QGroupBox, QComboBox)
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import project.database as database
import project.game as game
import project.objects as obj
import scenes.startScreen as start
import scenes.gameScreen as gs
import scenes.orderView as ov
import scenes.productView as pv
import scenes.truckView as tv


"""
App
Main intialization of app instance
"""
class App(QWidget):
    # The main application window that manages the screens.
    
    def __init__(self):
        super().__init__()
        
        self.game_state = game.GameState()
        print("GameState singleton instantiated at App start.")
        
        self.init_ui()
        self.init_screens()
        self.init_connections()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def init_ui(self):
        """Sets up the main window properties."""
        self.setWindowTitle("Game Interface")
        self.setGeometry(100, 100, 800, 600)

    def init_screens(self):
        """Initializes the different screens and the stacked widget."""
        self.stacked_widget = QStackedWidget()
        self.start_screen = start.StartScreen()
        self.game_screen = gs.GameScreen()
        self.truck_view_screen = tv.TruckView()
        self.product_view_screen = pv.ProductView()
        self.order_view_screen = ov.OrderView()
        
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.game_screen)
        self.stacked_widget.addWidget(self.truck_view_screen)
        self.stacked_widget.addWidget(self.product_view_screen) # Add to stack
        self.stacked_widget.addWidget(self.order_view_screen)

    def init_connections(self):
        """Connects the signals from each screen to their handlers."""
        self.start_screen.start_button.clicked.connect(self.show_game_screen)
        self.game_screen.switch_to_truck_view.connect(self.show_truck_view_screen)
        self.game_screen.switch_to_product_view.connect(self.show_product_view_screen) # New Connection
        self.game_screen.switch_to_order_view.connect(self.show_order_view_screen)
        self.truck_view_screen.switch_to_game_screen.connect(self.show_game_screen)
        self.product_view_screen.switch_to_game_screen.connect(self.show_game_screen) # New Connection
        self.order_view_screen.switch_to_game_screen.connect(self.show_game_screen)

    def show_start_screen(self):
        """Switches the view back to the StartScreen."""
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def show_game_screen(self):
        """Switches the view to the GameScreen and updates player info."""
        self.game_screen.update_player_info()
        self.stacked_widget.setCurrentWidget(self.game_screen)

    def show_truck_view_screen(self):
        """Switches the view to the TruckView screen and updates its content."""
        self.truck_view_screen.update_player_info()
        self.truck_view_screen.update_truck_buttons()
        self.stacked_widget.setCurrentWidget(self.truck_view_screen)
        
    def show_product_view_screen(self):
        """
        Switches the view to the ProductView screen and updates its content.
        """
        self.product_view_screen.update_player_info()
        self.product_view_screen.update_product_buttons()
        self.product_view_screen.reset_view()
        self.stacked_widget.setCurrentWidget(self.product_view_screen)

    def show_order_view_screen(self):
        self.order_view_screen.refresh_orders_view()
        self.stacked_widget.setCurrentWidget(self.order_view_screen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())