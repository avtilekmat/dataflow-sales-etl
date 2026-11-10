
from PyQt5 import QtWidgets, QtCore

from src.history import get_analysis_history


class HistoryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DataFlow — История анализов")
        self.resize(1100, 650)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("История анализов")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #1E88E5;
        """)
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Файл",
            "Дата анализа",
            "Исходных",
            "Корректных",
            "Удалено",
            "Выручка",
            "Средний чек"
        ])

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.refresh_button = QtWidgets.QPushButton(
            "Обновить историю"
        )
        self.refresh_button.setFixedHeight(45)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.refresh_button.clicked.connect(self.load_history)
        layout.addWidget(self.refresh_button)

        self.load_history()

    def load_history(self):
        try:
            records = get_analysis_history()

            self.table.setRowCount(len(records))

            for row_index, record in enumerate(records):
                values = [
                    record["id"],
                    record["filename"],
                    record["analyzed_at"],
                    record["total_rows"],
                    record["valid_rows"],
                    record["removed_rows"],
                    record["total_revenue"],
                    record["average_order"]
                ]

                for col_index, value in enumerate(values):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setFlags(
                        item.flags() & ~QtCore.Qt.ItemIsEditable
                    )
                    self.table.setItem(row_index, col_index, item)

            self.table.resizeColumnsToContents()

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить историю:\n{error}"
            )
