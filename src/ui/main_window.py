import sys
from pathlib import Path

import pandas as pd
from PyQt5 import QtWidgets, QtCore

from src.ui.table_model import PandasTableModel
from src.transform import transform_data
from src.analytics import analyze_sales


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DataFlow — Sales Analytics")
        self.resize(1100, 700)

        self.df = None
        self.table_model = None

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        self.title = QtWidgets.QLabel("DataFlow — Sales Analytics")
        self.title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1E88E5;
        """)
        self.main_layout.addWidget(self.title)

        self.upload_button = QtWidgets.QPushButton("Загрузить CSV")
        self.upload_button.setFixedHeight(50)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.upload_button.clicked.connect(self.load_csv)
        self.main_layout.addWidget(self.upload_button)

        self.table = QtWidgets.QTableView()
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.main_layout.addWidget(self.table)

        self.status_label = QtWidgets.QLabel(
            "CSV-файл пока не загружен"
        )
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        self.analyze_button = QtWidgets.QPushButton("Анализировать")
        self.analyze_button.setFixedHeight(50)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.run_analysis)
        self.main_layout.addWidget(self.analyze_button)

        self.results_label = QtWidgets.QLabel("")
        self.results_label.setStyleSheet("""
            font-size: 17px;
            padding: 12px;
        """)
        self.main_layout.addWidget(self.results_label)

    def load_csv(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите CSV-файл",
            "",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)

            required_columns = {
                "order_id",
                "product",
                "category",
                "price",
                "quantity",
                "order_date"
            }

            missing_columns = required_columns - set(df.columns)

            if missing_columns:
                raise ValueError(
                    "Отсутствуют столбцы: "
                    + ", ".join(sorted(missing_columns))
                )

            if df.empty:
                raise ValueError("CSV-файл не содержит данных.")

            self.df = df
            self.table_model = PandasTableModel(df)
            self.table.setModel(self.table_model)
            self.table.resizeColumnsToContents()

            self.status_label.setText(
                f"Файл: {Path(file_path).name} | "
                f"Строк: {len(df)} | "
                f"Столбцов: {len(df.columns)}"
            )

            self.results_label.clear()
            self.analyze_button.setEnabled(True)

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка загрузки",
                str(error)
            )

    def run_analysis(self):
        if self.df is None:
            return

        try:
            cleaned_df = transform_data(self.df.copy())
            stats = analyze_sales(cleaned_df)

            self.results_label.setText(
                f"Заказов: {stats['orders']}  |  "
                f"Выручка: {stats['revenue']:,.2f}  |  "
                f"Средний чек: {stats['average_order']:,.2f}  |  "
                f"Продано единиц: {stats['products_sold']}"
            )

            self.status_label.setText(
                f"Обработано строк: {len(self.df)} | "
                f"Корректных: {len(cleaned_df)} | "
                f"Удалено: {len(self.df) - len(cleaned_df)}"
            )

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка анализа",
                str(error)
            )


def run_app():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
