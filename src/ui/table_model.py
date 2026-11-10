import pandas as pd
from PyQt5 import QtCore


class PandasTableModel(QtCore.QAbstractTableModel):
    def __init__(self, dataframe):
        super().__init__()
        self.df = dataframe

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.df)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            value = self.df.iat[index.row(), index.column()]

            if pd.isna(value):
                return ""

            return str(value)

        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.df.columns[section])

            return str(section + 1)

        return None
