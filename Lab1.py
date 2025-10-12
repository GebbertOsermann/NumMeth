import sys
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit)

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.InitializeUI()

	def InitializeUI(self):
		self.setFixedSize(900, 526)
		self.setWindowTitle("Numerical solution of nonlinear equations")
		self.setUpWindow()
		self.BuildGraph()
		self.show()

	def setUpWindow(self):
		equation_label = QLabel("Equation: x * tanh(x)-1=0", self)
		equation_label.move(20, 15)

		borders_label = QLabel("Borders:", self)
		borders_label.move(20, 45)

		a_label = QLabel("a:", self)
		a_label.move(20, 69)

		self.a_edit = QLineEdit(self)
		self.a_edit.setText("-2")
		self.a_edit.resize(40, 24)
		self.a_edit.move(34, 65)

		b_label = QLabel("b:", self)
		b_label.move(85, 69)

		self.b_edit = QLineEdit(self)
		self.b_edit.setText("2")
		self.b_edit.resize(40, 24)
		self.b_edit.move(99, 65)

		self.buildGraph = QPushButton("Build Graph",self)
		self.buildGraph.resize(345, 30)
		self.buildGraph.move(20, 95)
		self.buildGraph.clicked.connect(self.BuildGraph)

		self.solveEquation = QPushButton("Solve Equation",self)
		self.solveEquation.resize(345, 30)
		self.solveEquation.move(20, 125)
		self.solveEquation.clicked.connect(self.FindRoot)

		result_label = QLabel("Results:", self)
		result_label.move(20, 160)

		self.result_box = QTextEdit(self)
		self.result_box.setReadOnly(True)
		self.result_box.resize(345, 336)
		self.result_box.move(20, 180)
		self.result_box.setPlaceholderText("Results will appear here...")

		self.fig = Figure(figsize=(5, 5), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)
		self.canvas.move(386, 15)

		self.ax = self.fig.add_subplot(111)

	def BuildGraph(self):
		try:
			a = float(self.a_edit.text())
			b = float(self.b_edit.text())
		except ValueError:
			QMessageBox.warning(self, "Error", "'a' and 'b' must be numbers", QMessageBox.StandardButton.Ok)
			return
		if a >= b:
			QMessageBox.warning(self, "Error", "'a' must be lower than 'b'", QMessageBox.StandardButton.Ok)
			return
		x = np.linspace(a, b, 100)
		y = self.f(x)

		self.ax.clear()
		self.ax.set_title("f(x) = x * tanh(x) - 1")
		self.ax.grid(True)
		self.ax.plot(x, y)
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)
		self.canvas.draw()

	def f(self, x):
		return x * np.tanh(x) - 1

	def FindRoot(self):
		root_intervals = self.ShorteningRootIntervals()
		res1 = self.IterationMethod(root_intervals)
		res2 = self.DichotomyMethod(root_intervals)
		self.result_box.clear()
		self.result_box.append(f"Intervals with roots: {root_intervals}")
		self.result_box.append(f"\nRoots found using Iteration Method:\n{res1}")
		self.result_box.append(f"\nRoots found using Dichotomy Method:\n{res2}")
		self.result_box.append(f"\nRoots found using Newton's Method:\nWIP")

	def ShorteningRootIntervals(self):
		step = 1
		current_intervals = [(float(self.a_edit.text()), float(self.b_edit.text()))]

		for i in range(2):
			new_intervals = []
			for (l, r) in current_intervals:
				a1 = l
				while a1 < r:
					a2 = min(a1 + step, r)
					if self.f(a1) * self.f(a2) < 0:
						new_intervals.append((a1, a2))
					elif self.f(a1) == 0:
						new_intervals.append((a1, a1))
					elif self.f(a2) == 0:
						new_intervals.append((a2, a2))
					a1 = a2
			current_intervals = new_intervals
			step /= 10

		return [(round(l, 2), round(r, 2)) for (l, r) in current_intervals]

	def IterationMethod(self, intervals):
		step = 0.0001
		roots = []
		for (l, r) in intervals:
			a1 = l
			while a1 < r:
				a2 = min(a1 + step, r)
				if self.f(a1) * self.f(a2) < 0:
					roots.append((a1 + a2) / 2)
					break
				elif self.f(a1) == 0:
					roots.append(a1)
					break
				elif self.f(a2) == 0:
					roots.append(a2)
					break
				a1 = a2
		return roots

	def DichotomyMethod(self, intervals):
		roots = []
		for i in range(8):
			new_intervals = []
			for (l, r) in intervals:
				c = (r + l) / 2
				if self.f(l) * self.f(c) < 0:
					new_intervals.append((l, c))
				elif self.f(c) == 0:
					roots.append(c)
				elif self.f(c) * self.f(r) < 0:
					new_intervals.append((c, r))
			intervals = new_intervals
		for (l, r) in intervals:
			roots.append((l + r) / 2)
		return roots

	def NewtonsMethod(self, intervals):
		roots = []

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())