from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QAbstractItemView,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox
)
from .model import ContactsModel
from PyQt5.QtCore import Qt

## Set parameters to main window
class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(1500, 1000)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        # create instance of subsections;
        self.contactsModel = ContactsModel()
        self.setupUI()
    
    #setting up main window 
    def setupUI(self):
        # create table view with abstract item view so complete row selected
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model) # connect model with table view
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 300)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        # add buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog) # adding add dialog
        self.deleteButton = QPushButton("Delete") 
        self.deleteButton.clicked.connect(self.deleteContact) # add delete dialog i.e. connect clicked signal to delete contact slot
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContacts) # delete all button connectiont
        # add vertical display w buttons
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    # method to run add dialog
    def openAddDialog(self):
        dialog = AddDialog(self) # instance
        if dialog.exec() == QDialog.Accepted: # check for acceptance, upon pass, calls add contact 
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    # method to delete
    def deleteContact(self):
        row = self.table.currentIndex().row() #get current index of row, if 0, void, otherwise continue
        if row < 0:
            return

        messageBox = QMessageBox.warning( # simple warning 
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row) # delete

    # method to del all
    def clearContacts(self):
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearContacts()

## create contact dialog
class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    # setup contact dialog gui - inherting from Qdialog
    def setupUI(self):
        # line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.jobField = QLineEdit()
        self.jobField.setObjectName("Job")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        # create data fields form
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Job:", self.jobField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)
        # add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    # method to accept provided data
    def accept(self):
        # init empty list to hold input data
        self.data = []
        # loop over provided fields for input
        for field in (self.nameField, self.jobField, self.emailField):
            # check for all data forms filled
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return
            # add data on succesful loop
            self.data.append(field.text())

        if not self.data:
            return

        super().accept()