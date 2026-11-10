
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.stats_label = QtWidgets.QLabel("Анализ ещё не выполнен")
        self.stats_label.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            padding: 12px;
        """)
        self.layout.addWidget(self.stats_label)

        self.figure = Figure(figsize=(9, 5))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas)

    def update_dashboard(self, df, stats):
        self.stats_label.setText(
            f"Заказов: {stats['orders']}  |  "
            f"Выручка: {stats['revenue']:,.2f}  |  "
            f"Средний чек: {stats['average_order']:,.2f}  |  "
            f"Продано единиц: {stats['products_sold']}"
        )

        self.figure.clear()

        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        category_sales = (
            df.groupby("category")["total_price"]
            .sum()
            .sort_values(ascending=False)
        )

        ax1.bar(category_sales.index, category_sales.values)
        ax1.set_title("Выручка по категориям")
        ax1.tick_params(axis="x", rotation=20)

        daily_sales = (
            df.groupby("order_date")["total_price"]
            .sum()
            .sort_index()
        )

        ax2.plot(daily_sales.index, daily_sales.values, marker="o")
        ax2.set_title("Выручка по дням")
        ax2.tick_params(axis="x", rotation=30)

        self.figure.tight_layout()
        self.canvas.draw()
