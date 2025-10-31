import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QButtonGroup, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.InitializeUI()

	def InitializeUI(self):
		self.setFixedSize(900, 600)
		self.setWindowTitle("Numerical methods for calculating integrals")
		self.SetUpWindow()
		self.show()

	def SetUpWindow(self):

		integral_label = QLabel("Select Integral:")
		self.integrals_box = QComboBox()
		self.integrals_box.addItems([
			"1/(sqrt(x**2+1))",
			"cos(x)/(x+1)",
			"1/(1.5*x**2+0.7)"
			])

		self.integral_funcs = [
		lambda x: 1.0/np.sqrt(x**2 + 1.0),
		lambda x: np.cos(x)/(x + 1.0),
		lambda x: 1.0/(1.5*x**2 + 0.7)
		]
		self.integral = self.integral_funcs[self.integrals_box.currentIndex()]
		self.solve = False

		integral_selection = QHBoxLayout()
		integral_selection.addWidget(integral_label)
		integral_selection.addWidget(self.integrals_box)

		self.integrals_box.currentIndexChanged.connect(self.IntegralChange)

		intervals_label = QLabel("Specify the interval:")
		a_label = QLabel("a:")
		self.a_edit = QLineEdit(self)
		self.a_edit.setText("0.2")
		b_label = QLabel("b:")
		self.b_edit = QLineEdit(self)
		self.b_edit.setText("1.2")
		intervals_layout = QHBoxLayout()
		intervals_layout.addWidget(intervals_label)
		intervals_layout.addWidget(a_label)
		intervals_layout.addWidget(self.a_edit)
		intervals_layout.addWidget(b_label)
		intervals_layout.addWidget(self.b_edit)

		self.buildGraph = QPushButton("Build Graph")
		self.buildGraph.clicked.connect(self.BuildGraph)

		self.fig = Figure(figsize=(5, 5), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self)

		self.ax = self.fig.add_subplot(111)

		divisions_box = QGroupBox("Select number of interval divisions:")
		division_layout = QVBoxLayout()
		self.radio1 = QRadioButton("10", self)
		self.radio1.setChecked(True)
		self.radio2 = QRadioButton("20", self)
		self.radio3 = QRadioButton("50", self)
		self.radio4 = QRadioButton("100", self)
		self.radio5 = QRadioButton("1000", self)
		division_layout.addWidget(self.radio1)
		division_layout.addWidget(self.radio2)
		division_layout.addWidget(self.radio3)
		division_layout.addWidget(self.radio4)
		division_layout.addWidget(self.radio5)
		divisions_box.setLayout(division_layout)

		self.division_group = QButtonGroup()
		self.division_group.addButton(self.radio1)
		self.division_group.addButton(self.radio2)
		self.division_group.addButton(self.radio3)
		self.division_group.addButton(self.radio4)
		self.division_group.addButton(self.radio5)
		self.division_group.buttonClicked.connect(self.DivisionChange)
		self.DivisionChange()

		method_box = QGroupBox("Select solution method:")
		method_layout = QVBoxLayout()
		self.method1 = QRadioButton("Rectangle", self)
		self.method1.setChecked(True)
		self.method2 = QRadioButton("Trapezoid", self)
		self.method3 = QRadioButton("Monte-Carlo", self)
		method_layout.addWidget(self.method1)
		method_layout.addWidget(self.method2)
		method_layout.addWidget(self.method3)
		method_box.setLayout(method_layout)

		self.method_group = QButtonGroup()
		self.method_group.addButton(self.method1)
		self.method_group.addButton(self.method2)
		self.method_group.addButton(self.method3)
		self.method_group.buttonClicked.connect(self.MethodChange)
		self.method = "Rectangle"

		self.find_integral = QPushButton("Find Integral")
		self.find_integral.clicked.connect(self.FindIntegral)

		result_label = QLabel("Results:", self)

		self.result_box = QTextEdit(self)
		self.result_box.setReadOnly(True)
		self.result_box.setPlaceholderText("Results will appear here...")

		left_layout = QVBoxLayout()
		left_layout.addLayout(integral_selection)
		left_layout.addLayout(intervals_layout)
		left_layout.addWidget(self.buildGraph)
		left_layout.addSpacing(6)
		left_layout.addWidget(divisions_box)
		left_layout.addWidget(method_box)
		left_layout.addWidget(self.find_integral)
		left_layout.addWidget(result_label)
		left_layout.addWidget(self.result_box)
		left_container = QWidget()
		left_container.setLayout(left_layout)
		left_container.setMaximumWidth(320)

		main_layout = QHBoxLayout()
		main_layout.addWidget(left_container)
		main_layout.addWidget(self.canvas, 1)
		self.setLayout(main_layout)

	def IntegralChange(self):
		index = self.integrals_box.currentIndex()
		self.integral = self.integral_funcs[index]
		border_a = ("0.2", "0.6", "1.4")
		border_b = ("1.2", "1.4", "2.6")
		self.a_edit.setText(border_a[index])
		self.b_edit.setText(border_b[index])

	def DivisionChange(self):
		checked = self.division_group.checkedButton()
		divisions = {
			self.radio1: 10,
			self.radio2: 20,
			self.radio3: 50,
			self.radio4: 100,
			self.radio5: 1000,
		}
		self.division = divisions.get(checked)

	def MethodChange(self, button):
		self.method = button.text()

	def f(self, x):
		return self.integral(x)

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
		pad = 0.3
		a1 = a - 0.3
		b1 = b + 0.3
		x = np.linspace(a1, b1, 100)
		y = self.f(x)

		self.ax.clear()
		self.ax.set_title(f"f(x) = {self.integrals_box.currentText()}")
		self.ax.grid(True)
		self.ax.plot(x, y)
		self.ax.axvline(a, color = "red", linestyle="--", linewidth=1.2)
		self.ax.axvline(b, color = "red", linestyle="--", linewidth=1.2)
		self.ax.axhline(0, color="black", linewidth=1.0)
		self.ax.axvline(0, color="black", linewidth=1.0)
		if self.solve:
			if self.method=="Rectangle":
				step = (float(self.b_edit.text()) - float(self.a_edit.text())) / self.division
				for m, h in zip(self.mids, self.heights):
					a0 = m - 0.5 * step
					y0 = min(0, h)
					height = abs(h)
					rect = patches.Rectangle((a0, y0), step, height, linewidth=0.1, edgecolor='black', facecolor='green', alpha=0.45)
					self.ax.add_patch(rect)
			if self.method=="Trapezoid":
				step = (float(self.b_edit.text()) - float(self.a_edit.text())) / self.division
				for i in range(self.division):
					verts = [(a, 0.0), (a, self.f(a)), (a+step, self.f(a+step)), (a+step, 0.0)]
					trapezoid = patches.Polygon(verts, closed=True, linewidth=0.1, edgecolor='black', facecolor='green', alpha=0.45)
					self.ax.add_patch(trapezoid)
					a += step
			if self.method == "Monte-Carlo":
				rect = patches.Rectangle((a, 0), (b - a), (self.y_max - 0), linewidth=1.0, edgecolor='blue', facecolor='none', linestyle='--')
				self.ax.add_patch(rect)
				self.ax.scatter(self.x_dots[self.hits], self.y_dots[self.hits], s=8, alpha=0.6)
				self.ax.scatter(self.x_dots[~self.hits], self.y_dots[~self.hits], s=8, alpha=0.6)
		self.canvas.draw()
		self.solve = False

	def FindIntegral(self):
		self.solve = True
		res1 = self.RectangleMethod()
		res2 = self.TrapezoidMethod()
		res3 = self.MonteCarlo()
		self.BuildGraph()
		self.result_box.clear()
		self.result_box.append(f"Interval {float(self.a_edit.text())} - {float(self.b_edit.text())} with {self.division} divisions")
		self.result_box.append(f"\nIntegral found using Rectangle Method:\n{res1}")
		self.result_box.append(f"\nIntegral found using Trapezoid Method:\n{res2}")
		self.result_box.append(f"\nIntegral found using Monte-Carlo Method:\n{res3}")

	def RectangleMethod(self):
		a = float(self.a_edit.text())
		b = float(self.b_edit.text())
		step = (b - a) / self.division
		s = 0
		self.mids = []
		self.heights = []
		for i in range(self.division):
			rect = a + step / 2
			s += self.f(rect) * step
			self.mids.append(rect)
			self.heights.append(self.f(rect))
			a += step
		return s

	def TrapezoidMethod(self):
		a = float(self.a_edit.text())
		b = float(self.b_edit.text())
		step = (b - a) / self.division
		s = 0
		for i in range(self.division):
			s += 0.5 * (self.f(a) + self.f(a+step)) * step
			a += step
		return s

	def FindMaxValue(self):
		a = float(self.a_edit.text())
		b = float(self.b_edit.text())
		xs = np.linspace(a, b, 100000)
		y = np.array([self.f(x) for x in xs])
		return y.max()

	def MonteCarlo(self):
		a = float(self.a_edit.text())
		b = float(self.b_edit.text())		
		self.y_max = self.FindMaxValue()
		self.x_dots = np.random.uniform(a, b, self.division)
		self.y_dots = np.random.uniform(0, self.y_max, self.division)
		dots = np.array([self.f(x) for x in self.x_dots])
		self.hits = (self.y_dots <= dots)
		count = np.count_nonzero(self.hits)
		s = (count/self.division) * ((b-a)*self.y_max)
		return s

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec())