from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

## create model for contacts table
class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        # create model 'tablemodel'
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Job", "Email")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel
    
    # method to add contact to db
    def addContact(self, data):
        rows = self.model.rowCount() # count rows, affix to bottom
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data): # reinserts every item in model
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll() # submits changes, then reloads
        self.model.select()

    # model to delete contacts from db
    def deleteContact(self, row):
        self.model.removeRow(row) # same principal as above
        self.model.submitAll()
        self.model.select()

    # model to del all
    def clearContacts(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit) # use manual submit to cache all rows enabling us to modify all fields 
        self.model.removeRows(0, self.model.rowCount()) # above
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange) # caveat to revert to original values
        self.model.select()