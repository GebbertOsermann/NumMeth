import sys
import numpy as np
import numexpr as ne
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QRadioButton, QButtonGroup, QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout)

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
		equation_label = QLabel("Equation:", self)

		self.equation_edit = QLineEdit(self)
		self.equation_edit.setText("x*tanh(x)-1=0")

		borders_label = QLabel("Borders:", self)

		a_label = QLabel("a:", self)

		self.a_edit = QLineEdit(self)
		self.a_edit.setText("-2")

		b_label = QLabel("b:", self)

		self.b_edit = QLineEdit(self)
		self.b_edit.setText("2")

		precision_box = QGroupBox("Select Precision:")
		eps_layout = QVBoxLayout()
		self.radio1 = QRadioButton("1e-4", self)
		self.radio1.setChecked(True)
		self.radio2 = QRadioButton("1e-6", self)
		self.radio3 = QRadioButton("1e-8", self)
		eps_layout.addWidget(self.radio1)
		eps_layout.addWidget(self.radio2)
		eps_layout.addWidget(self.radio3)
		precision_box.setLayout(eps_layout)

		self.radiogroup = QButtonGroup(self)
		self.radiogroup.addButton(self.radio1)
		self.radiogroup.addButton(self.radio2)
		self.radiogroup.addButton(self.radio3)
		self.radiogroup.buttonClicked.connect(self.PrecisionChange)
		self.PrecisionChange()

		self.buildGraph = QPushButton("Build Graph",self)
		self.buildGraph.clicked.connect(self.BuildGraph)

		self.solveEquation = QPushButton("Solve Equation",self)
		self.solveEquation.clicked.connect(self.FindRoot)

		result_label = QLabel("Results:", self)

		self.result_box = QTextEdit(self)
		self.result_box.setReadOnly(True)
		self.result_box.setPlaceholderText("Results will appear here...")

		self.fig = Figure(figsize=(5, 5), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.ax = self.fig.add_subplot(111)

		left_layout = QVBoxLayout()
		eq_row = QHBoxLayout()
		eq_row.addWidget(equation_label)
		eq_row.addWidget(self.equation_edit)
		left_layout.addLayout(eq_row)

		borders_row = QHBoxLayout()
		borders_row.addWidget(borders_label)
		borders_row.addSpacing(6)
		borders_row.addWidget(a_label)
		borders_row.addWidget(self.a_edit)
		borders_row.addSpacing(6)
		borders_row.addWidget(b_label)
		borders_row.addWidget(self.b_edit)
		borders_row.addStretch()
		left_layout.addLayout(borders_row)

		left_layout.addSpacing(8)
		left_layout.addWidget(self.buildGraph)
		left_layout.addSpacing(6)
		left_layout.addWidget(precision_box)
		left_layout.addWidget(self.solveEquation)
		left_layout.addWidget(result_label)
		left_layout.addWidget(self.result_box)

		left_container = QWidget()
		left_container.setLayout(left_layout)
		left_container.setMaximumWidth(320)

		main_layout = QHBoxLayout()
		main_layout.addWidget(left_container)
		main_layout.addWidget(self.canvas, 1)
		self.setLayout(main_layout)

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
		x = np.linspace(a, b, 100) #Creating an array with 100 points from a to b for graph
		y = self.f(x)

		self.ax.clear()
		self.ax.set_title(f"f(x) = x*tanh(x)-1")
		self.ax.grid(True)
		self.ax.plot(x, y)
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)
		self.canvas.draw()

	def f(self, x):
		return x*np.tanh(x)-1

	def derivative(self, x):
		return (self.f(x + 1e-5) - self.f(x - 1e-5)) / (2 * (1e-5))

	def FindRoot(self):
		root_intervals = self.ShorteningRootIntervals()
		res1 = self.IterationMethod(root_intervals)
		res2 = self.DichotomyMethod(root_intervals)
		res3 = self.NewtonsMethod(root_intervals)
		self.result_box.clear()
		self.result_box.append(f"Intervals with roots: {root_intervals}")
		self.result_box.append(f"\nRoots found using Iteration Method:\n{res1}")
		self.result_box.append(f"\nRoots found using Dichotomy Method:\n{res2}")
		self.result_box.append(f"\nRoots found using Newton's Method:\n{res3}")

	def PrecisionChange(self):
		if self.radio1.isChecked():
			self.precision = 1e-4
		elif self.radio2.isChecked():
			self.precision = 1e-6
		else:
			self.precision = 1e-8

	def ShorteningRootIntervals(self):
		#Shortens intervals with roots
		step = 1 #First step
		current_intervals = [(float(self.a_edit.text()), float(self.b_edit.text()))] #Borders

		for i in range(2): #Two times shorts root intervals. First time step = 1.0, second step = 0.1
			new_intervals = []
			for (l, r) in current_intervals:
				a1 = l
				while a1 < r:
					a2 = min(a1 + step, r) #Using min so it wouldn't go out of bonds
					if self.f(a1) * self.f(a2) < 0: #Finds intervals on which sign changes
						new_intervals.append((a1, a2)) #New interval adds to list
					elif self.f(a1) == 0:
						new_intervals.append((a1, a1))
					elif self.f(a2) == 0:
						new_intervals.append((a2, a2))
					a1 = a2
			current_intervals = new_intervals #Updating list for new cycle
			step /= 10 #Shortens step from 1 to 0.1

		return [(round(l, 2), round(r, 2)) for (l, r) in current_intervals]

	def IterationMethod(self, intervals):
		# digits = max(0, int(-np.log10(self.precision)))
		roots = []
		step = 0.01
		while step >= self.precision:
			new_intervals = []
			current_roots = []
			for (l, r) in intervals:
				a1 = l
				while a1 < r:
					a2 = min(a1 + step, r)
					if self.f(a1) * self.f(a2) < 0:
						new_intervals.append((a1, a2))
						current_roots.append((a1 + a2) / 2)
						# current_roots.append(round(((a1 + a2) / 2), digits))
					elif self.f(a1) == 0:
						new_intervals.append((a1, a1))
						current_roots.append((a1 + a1) / 2)
 						# current_roots.append(round(((a1 + a1) / 2), digits))
					elif self.f(a2) == 0:
						new_intervals.append((a2, a2))
						current_roots.append((a2 + a2) / 2)
 						# current_roots.append(round(((a2 + a2) / 2), digits))
					a1 = a2
			intervals = new_intervals
			roots = current_roots
			step /= 10
		return roots

	def DichotomyMethod(self, intervals):
		# digits = max(0, int(-np.log10(self.precision)))
		roots = []
		for (l, r) in intervals:
			while abs(r - l) > self.precision:
				c = (l + r) / 2 #Creates new point in the center of interval
				if self.f(l) * self.f(c) < 0: #Finds which half contains root
					r = c
				else:
					l = c
			roots.append((l + r) / 2)
 			# roots.append(round(((l + r) / 2), digits))
		return roots

	def NewtonsMethod(self, intervals):
		# digits = max(0, int(-np.log10(self.precision)))
		roots = []
		for (l, r) in intervals:
			x = l + self.precision
			for i in range(50):
				x_new = x - self.f(x) / self.derivative(x)
				if abs(x_new - x) < self.precision or abs(self.f(x_new)) < self.precision:
					x = x_new
					break
				x = x_new
			roots.append(float(x))
 			# roots.append(round(float(x), digits))
		return roots

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())