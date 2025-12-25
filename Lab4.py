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
		self.setWindowTitle("Lagrange Polynomial for function interpolation")
		self.SetUpWindow()
		self.show()

	def SetUpWindow(self):
		func_label = QLabel("Function:")
		self.func_edit = QLineEdit(self)
		self.func_edit.setText("sin(x)")

		borders_group = QGroupBox("Set borders:")

		xmin_label = QLabel("x min:")
		self.xmin_edit = QLineEdit(self)
		self.xmin_edit.setText("-15")

		xmax_label = QLabel("x max:")
		self.xmax_edit = QLineEdit(self)
		self.xmax_edit.setText("5")

		a_label = QLabel("a:")
		self.a_edit = QLineEdit(self)
		self.a_edit.setText("-15")

		b_label = QLabel("b:")
		self.b_edit = QLineEdit(self)
		self.b_edit.setText("5")

		self.build_graph = QPushButton("Build function")
		self.build_graph.clicked.connect(self.BuildGraph)
		self.polynomial_graph = QPushButton("Build Lagrange Polynomial")
		self.polynomial_graph.clicked.connect(self.BuildPolynomial)

		self.fig = Figure(figsize=(5, 5), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.ax = self.fig.add_subplot(111)

		func_layout = QHBoxLayout()
		func_layout.addWidget(func_label)
		func_layout.addWidget(self.func_edit)

		up_layout = QHBoxLayout()
		up_layout.addWidget(xmin_label)
		up_layout.addWidget(self.xmin_edit)
		up_layout.addWidget(xmax_label)
		up_layout.addWidget(self.xmax_edit)

		down_layout = QHBoxLayout()
		down_layout.addWidget(a_label)
		down_layout.addWidget(self.a_edit)
		down_layout.addWidget(b_label)
		down_layout.addWidget(self.b_edit)

		group_layout = QVBoxLayout()
		group_layout.addLayout(up_layout)
		group_layout.addLayout(down_layout)

		borders_group.setLayout(group_layout)

		left_layout = QVBoxLayout()
		left_layout.addLayout(func_layout)
		left_layout.addSpacing(6)
		left_layout.addWidget(borders_group)
		left_layout.addWidget(self.build_graph)
		left_layout.addWidget(self.polynomial_graph)
		left_layout.addStretch(1)

		left_container = QWidget()
		left_container.setLayout(left_layout)
		left_container.setMinimumWidth(320)
		
		main_layout = QHBoxLayout()
		main_layout.addWidget(left_container)
		main_layout.addWidget(self.canvas, 1)
		self.setLayout(main_layout)

	def f(self, x):
		# return 2*(x*x)-1
		# return np.exp(x)
		return np.sin(x)

	def BuildGraph(self):
		try:
			xmin = float(self.xmin_edit.text())
			xmax = float(self.xmax_edit.text())
		except ValueError:
			QMessageBox.warning(self, "Error", "'xmin' and 'xmax' must be numbers", QMessageBox.StandardButton.Ok)
			return
		if xmin >= xmax:
			QMessageBox.warning(self, "Error", "'xmin' must be lower than 'xmax'", QMessageBox.StandardButton.Ok)
			return
		x = np.linspace(xmin, xmax, 100)
		y = self.f(x)

		self.ax.clear()
		self.ax.set_title(f"f(x) = sin(x)")
		self.ax.grid(True)
		self.ax.plot(x, y)
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)
		self.canvas.draw()

	def LagrangePolynomial(self, x, x_nodes, y_nodes):
		n = len(x_nodes)
		L = np.zeros_like(x, dtype=float)

		for i in range(n):
			li = np.ones_like(x, dtype=float)
			for j in range(n):
				if i != j:
					li *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
			L += y_nodes[i] * li
		return L

	def BuildPolynomial(self):
		xmin = float(self.xmin_edit.text())
		xmax = float(self.xmax_edit.text())
		a = float(self.a_edit.text())
		b = float(self.b_edit.text())
		h = (b - a) / 10
		x = np.linspace(xmin, xmax, 400)
		x_nodes = np.array([a + i * h for i in range(11)])
		y_nodes = self.f(x_nodes)
		y_lagrange = self.LagrangePolynomial(x, x_nodes, y_nodes)
		self.ax.clear()
		self.ax.grid(True)
		self.ax.plot(x, self.f(x), label="f(x)")
		self.ax.plot(x, y_lagrange, "--", label="Lagrange polynomial")
		self.ax.scatter(x_nodes, y_nodes, color="red", zorder=5, label="Interpolation nodes")
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)

		self.canvas.draw()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())