import sys # access to exit
from PyQt5.QtWidgets import QApplication
from .views import Window
from .database import createConnection

# Main app function loop
def main():
    # create application
    app = QApplication(sys.argv)
    # connect to database
    if not createConnection("contacts.sqlite"):
        sys.exit(1)
    # Create the main window
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())