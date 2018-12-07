import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from math import floor, pi, exp
from PyQt5 import QtGui, QtCore, QtWidgets

############
# Gokay Gas
# 150150107
# 18.10.2018
############

class Window(QtWidgets.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("Filtering & Geometric Transforms")
		self.setWindowState(QtCore.Qt.WindowMaximized)
    
		self.Img = None
		self.outputImg = None
		self.isInputOpen = False

		mainMenu = self.menuBar()

		fileMenu = mainMenu.addMenu('&File')

		# file menu actions

		openAction = QtWidgets.QAction("Open", self)
		openAction.triggered.connect(self.open_image)

		saveAction = QtWidgets.QAction("Save", self)
		saveAction.triggered.connect(self.save_image)

		exitAction = QtWidgets.QAction("Exit", self)
		exitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)

		createTriangulationAction = QtWidgets.QAction("Create Triangulation", self)
		createTriangulationAction.triggered.connect(self.create_triangulation)

		morphAction = QtWidgets.QAction("Morph", self)
		morphAction.triggered.connect(self.morph)

		fileMenu.addAction(openAction)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(exitAction)

		self.toolBar = self.addToolBar("ToolBar")
		self.toolBar.addAction(createTriangulationAction)
		self.toolBar.addAction(morphAction)

		# central image that will keep the widgets of the images.
		self.centralwidget = QtWidgets.QWidget(self)
		# horizontal layout for the 3 columns
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
		self.horizontalLayout.setSpacing(10)
		# input image widget
		self.widget = QtWidgets.QWidget(self.centralwidget)
		self.widget.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		# vertical layout to divide images and plots
		self.VerticalLayout1 = QtWidgets.QVBoxLayout(self.widget)
		self.VerticalLayout1.setContentsMargins(10, 0, 10, 0)
		self.VerticalLayout1.setSpacing(0)
		self.horizontalLayout.addWidget(self.widget)
		# target image widget
		self.widget_2 = QtWidgets.QWidget(self.centralwidget)
		self.widget_2.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		# vertical layout to divide images and plots
		self.VerticalLayout2 = QtWidgets.QVBoxLayout(self.widget_2)
		self.VerticalLayout2.setContentsMargins(10, 0, 10, 0)
		self.VerticalLayout2.setSpacing(0)
		self.horizontalLayout.addWidget(self.widget_2)
		# output image widget
		self.widget_3 = QtWidgets.QWidget(self.centralwidget)
		self.widget_3.setStyleSheet("border:1px solid rgb(200, 200, 200);")
		# vertical layout to divide images and plots
		self.VerticalLayout3 = QtWidgets.QVBoxLayout(self.widget_3)
		self.VerticalLayout3.setContentsMargins(10, 0, 10, 0)
		self.VerticalLayout3.setSpacing(0)
		self.horizontalLayout.addWidget(self.widget_3)
		self.setCentralWidget(self.centralwidget)
		
		self.show()


	def open_image(self):
		# Image
		self.Img = cv2.imread("input.png")

		R, C, B = self.Img.shape
		qImg = QtGui.QImage(self.Img.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		
		#pix = QtGui.QPixmap('color1.png')
		self.label = QtWidgets.QLabel(self.centralwidget)
		pix = QtGui.QPixmap(qImg)
		self.label.setPixmap(pix)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setStyleSheet("border:0px")
		
		self.horizontalLayout.addWidget(self.label)

	def save_image(self):
		cv2.imwrite("./output-image.png", self.outputImg)

	def create_triangulation(self):
		return NotImplementedError

	def morph(self):
		return NotImplementedError

def main():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

main()
