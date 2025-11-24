import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QButtonGroup, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.InitializeUI()

	def InitializeUI(self):
		self.setFixedSize(900, 600)
		self.setWindowTitle("Least squares method for linear regression")
		self.SetUpWindow()
		self.show()

	def SetUpWindow(self):

		x_label = QLabel("X:")
		y_label = QLabel("Y:")
		self.x_edit = QLineEdit(self)
		self.x_edit.setText("1 2 3 4 5 6 7 8")
		self.y_edit = QLineEdit(self)
		self.y_edit.setText("521 308 240 204 183 175 159 152")

		self.build_regression = QPushButton("Build linear regression")
		self.build_regression.clicked.connect(self.BuildRegression)

		self.fig = Figure(figsize=(5, 5), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.ax = self.fig.add_subplot(111)

		x_layout = QHBoxLayout()
		x_layout.addWidget(x_label)
		x_layout.addWidget(self.x_edit)

		y_layout = QHBoxLayout()
		y_layout.addWidget(y_label)
		y_layout.addWidget(self.y_edit)

		dots_layout = QVBoxLayout()
		dots_layout.addLayout(x_layout)
		dots_layout.addLayout(y_layout)

		dots_group = QGroupBox("Input dots coordinates")
		dots_group.setLayout(dots_layout)

		left_layout = QVBoxLayout()
		left_layout.addWidget(dots_group)
		left_layout.addWidget(self.build_regression)
		left_layout.addStretch(1)

		left_container = QWidget()
		left_container.setLayout(left_layout)
		left_container.setMinimumWidth(320)

		main_layout = QHBoxLayout()
		main_layout.addWidget(left_container)
		main_layout.addWidget(self.canvas, 1)
		self.setLayout(main_layout)

	def BuildRegression(self):
		try:
			x_cords = [float(val) for val in self.x_edit.text().split()]
			y_cords = [float(val) for val in self.y_edit.text().split()]
		except ValueError:
			QMessageBox.warning(self, "Error", "'x' and 'y' must be numbers", QMessageBox.StandardButton.Ok)
			return
		if len(x_cords) != len(y_cords):
			QMessageBox.warning(self, "Error", "'x' and 'y' must have the same number of coords", QMessageBox.StandardButton.Ok)
			return

		k, b = self.least_squares(x_cords, y_cords)
		x_line = [x_cords[0], x_cords[-1]]
		y_line = [k * x_cords[0] + b, k * x_cords[-1] + b]

		self.ax.clear()
		self.ax.grid(True)
		self.ax.scatter(x_cords, y_cords, s=20, alpha=0.8)
		self.ax.plot(x_line, y_line, color="red", linewidth=2)
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)
		self.canvas.draw()

	def least_squares(self, x, y):
		n = len(x)
		sum_x = sum(x)
		sum_y = sum(y)
		sum_xy = sum(x[i] * y[i] for i in range(n))
		sum_x2 = sum(x[i] * x[i] for i in range(n))

		k = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
		b = (sum_y - k * sum_x) / n

		return k, b


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())