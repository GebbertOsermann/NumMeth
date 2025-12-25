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
		self.setWindowTitle("Numerical solution of ordinary differential equations")
		self.SetUpWindow()
		self.show()

	def SetUpWindow(self):
		func_label = QLabel("Function y':")
		self.func_edit = QLineEdit(self)
		self.func_edit.setText("(y*y-y)/x")
		self.func_edit.setReadOnly(True)

		borders_group = QGroupBox("Set initial conditions:")

		x0_label = QLabel("x0:")
		self.x0_edit = QLineEdit(self)
		self.x0_edit.setText("1")

		y_x0_label = QLabel("y(x0):")
		self.y_x0_edit = QLineEdit(self)
		self.y_x0_edit.setText("0.5")

		a_label = QLabel("a:")
		self.a_edit = QLineEdit(self)
		self.a_edit.setText("1")

		b_label = QLabel("b:")
		self.b_edit = QLineEdit(self)
		self.b_edit.setText("4")

		h_label = QLabel("h:")
		self.h_edit = QLineEdit(self)
		self.h_edit.setText("0.1")

		method_box = QGroupBox("Select method")
		method_layout = QVBoxLayout()
		self.radio1 = QRadioButton("Euler Method", self)
		self.radio1.setChecked(True)
		self.radio2 = QRadioButton("Runge–Kutta 4", self)
		method_layout.addWidget(self.radio1)
		method_layout.addWidget(self.radio2)
		method_box.setLayout(method_layout)

		self.method_group = QButtonGroup()
		self.method_group.addButton(self.radio1)
		self.method_group.addButton(self.radio2)
		self.method_group.buttonClicked.connect(self.MethodChange)
		self.MethodChange()

		self.build_graph = QPushButton("Build function")
		self.build_graph.clicked.connect(self.BuildGraph)

		self.fig = Figure(figsize=(5, 5), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.ax = self.fig.add_subplot(111)

		func_layout = QHBoxLayout()
		func_layout.addWidget(func_label)
		func_layout.addWidget(self.func_edit)

		up_layout = QHBoxLayout()
		up_layout.addWidget(x0_label)
		up_layout.addWidget(self.x0_edit)
		up_layout.addWidget(y_x0_label)
		up_layout.addWidget(self.y_x0_edit)

		down_layout = QHBoxLayout()
		down_layout.addWidget(a_label)
		down_layout.addWidget(self.a_edit)
		down_layout.addWidget(b_label)
		down_layout.addWidget(self.b_edit)

		h_layout = QHBoxLayout()
		h_layout.addWidget(h_label)
		h_layout.addWidget(self.h_edit)

		group_layout = QVBoxLayout()
		group_layout.addLayout(up_layout)
		group_layout.addLayout(down_layout)
		group_layout.addLayout(h_layout)

		borders_group.setLayout(group_layout)

		left_layout = QVBoxLayout()
		left_layout.addLayout(func_layout)
		left_layout.addSpacing(6)
		left_layout.addWidget(borders_group)
		left_layout.addWidget(method_box)
		left_layout.addWidget(self.build_graph)
		left_layout.addStretch(1)

		left_container = QWidget()
		left_container.setLayout(left_layout)
		left_container.setMinimumWidth(320)
		
		main_layout = QHBoxLayout()
		main_layout.addWidget(left_container)
		main_layout.addWidget(self.canvas, 1)
		self.setLayout(main_layout)

	def MethodChange(self):
		checked = self.method_group.checkedButton()
		if checked == self.radio1:
			self.method = 1
		else:
			self.method = 2

	def f(self, x, y):
		return (y * y - y) / x

	def exact_solution(self, x, x0, y0):
		C = (1 - 1 / y0) / x0
		return 1 / (1 - C * x)

	def BuildGraph(self):
		try:
			a = float(self.a_edit.text())
			b = float(self.b_edit.text())
			x0 = float(self.x0_edit.text())
			y0 = float(self.y_x0_edit.text())
		except ValueError:
			QMessageBox.warning(self, "Error", "'a' and 'b' must be numbers", QMessageBox.StandardButton.Ok)
			return
		if a >= b:
			QMessageBox.warning(self, "Error", "'a' must be lower than 'b'", QMessageBox.StandardButton.Ok)
			return
		x, y = self.Solve()

		x_exact = np.linspace(a, b, 400)
		y_exact = self.exact_solution(x_exact, x0, y0)

		self.ax.clear()
		self.ax.set_title(f"y(x) = (y*y-y)/x")
		self.ax.grid(True)
		self.ax.plot(x, y, '-', label="Euler method")
		self.ax.plot(x_exact, y_exact, '-', label="Exact solution")
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)
		self.canvas.draw()

	def Solve(self):
		x0 = float(self.x0_edit.text())
		y0 = float(self.y_x0_edit.text())
		a = float(self.a_edit.text())
		b = float(self.b_edit.text())
		h = float(self.h_edit.text())

		x_vals = [x0]
		y_vals = [y0]

		x = x0
		y = y0

		while x < b:
			if self.method == 1:
				y = y + h * self.f(x, y)
				x = x + h
				x_vals.append(x)
				y_vals.append(y)

			else:
				k1 = self.f(x, y)
				k2 = self.f(x + h/2, y + h*k1/2)
				k3 = self.f(x + h/2, y + h*k2/2)
				k4 = self.f(x + h, y + h*k3)

				y = y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
				x = x + h

				x_vals.append(x)
				y_vals.append(y)

		return np.array(x_vals), np.array(y_vals)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())

