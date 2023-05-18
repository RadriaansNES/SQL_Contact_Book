import sys # access to exit
from PyQt5.QtWidgets import QApplication
from .views import Window

# Main app function loop
def main():
    # create application
    app = QApplication(sys.argv)
    # Create the main window
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())