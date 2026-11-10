
import sys
from pathlib import Path

import pandas as pd
from PyQt5 import QtWidgets, QtCore

from src.ui.table_model import PandasTableModel
from src.ui.dashboard import Dashboard
from src.transform import transform_data
from src.analytics import analyze_sales


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DataFlow — Sales Analytics")
        self.resize(1200, 850)

        self.df = None
        self.table_model = None

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(15)

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
        self.main_layout.addWidget(self.table, stretch=2)

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

        self.dashboard = Dashboard()
        self.dashboard.hide()
        self.main_layout.addWidget(self.dashboard, stretch=3)

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

            missing = required_columns - set(df.columns)

            if missing:
                raise ValueError(
                    "Отсутствуют столбцы: "
                    + ", ".join(sorted(missing))
                )

            if df.empty:
                raise ValueError("CSV-файл пуст.")

            self.df = df
            self.table_model = PandasTableModel(df)
            self.table.setModel(self.table_model)
            self.table.resizeColumnsToContents()

            self.dashboard.hide()
            self.analyze_button.setEnabled(True)

            self.status_label.setText(
                f"Файл: {Path(file_path).name} | "
                f"Строк: {len(df)} | "
                f"Столбцов: {len(df.columns)}"
            )

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
            if cleaned_df.empty:
                raise ValueError(
                    "После очистки не осталось корректных строк."
                )

            stats = analyze_sales(cleaned_df)

            self.dashboard.update_dashboard(cleaned_df, stats)
            self.dashboard.show()

            self.status_label.setText(
                f"Исходных строк: {len(self.df)} | "
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
