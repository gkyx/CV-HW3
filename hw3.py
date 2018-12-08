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
		self.Img2 = None
		self.outputImg = None
		self.isInputOpen = False
		self.isTargetOpen = False

		mainMenu = self.menuBar()

		fileMenu = mainMenu.addMenu('&File')

		# file menu actions

		openInputAction = QtWidgets.QAction("Open Input", self)
		openInputAction.triggered.connect(self.open_input_image)

		openTargetAction = QtWidgets.QAction("Open Target", self)
		openTargetAction.triggered.connect(self.open_target_image)

		saveAction = QtWidgets.QAction("Save the Output", self)
		saveAction.triggered.connect(self.save_image)

		exitAction = QtWidgets.QAction("Exit", self)
		exitAction.triggered.connect(QtCore.QCoreApplication.instance().quit)

		createTriangulationAction = QtWidgets.QAction("Create Triangulation", self)
		createTriangulationAction.triggered.connect(self.create_triangulation)

		morphAction = QtWidgets.QAction("Morph", self)
		morphAction.triggered.connect(self.morph)

		fileMenu.addAction(openInputAction)
		fileMenu.addAction(openTargetAction)
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


	def open_input_image(self):
		if not self.isInputOpen:
			# Image
			self.Img = cv2.imread("input.png")

			R, C, B = self.Img.shape
			qImg = QtGui.QImage(self.Img.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()

			self.label = QtWidgets.QLabel(self.centralwidget)
			pix = QtGui.QPixmap(qImg)
			self.label.setPixmap(pix)
			self.label.setAlignment(QtCore.Qt.AlignCenter)
			self.label.setStyleSheet("border:0px")

			self.VerticalLayout1.addWidget(self.label)
			self.isInputOpen = True

	def open_target_image(self):
		if not self.isTargetOpen:			
			# Image
			self.Img2 = cv2.imread("target.png")

			R, C, B = self.Img2.shape
			qImg = QtGui.QImage(self.Img2.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()

			self.label2 = QtWidgets.QLabel(self.centralwidget)
			pix2 = QtGui.QPixmap(qImg)
			self.label2.setPixmap(pix2)
			self.label2.setAlignment(QtCore.Qt.AlignCenter)
			self.label2.setStyleSheet("border:0px")

			self.VerticalLayout2.addWidget(self.label2)
			self.isTargetOpen = True

	def save_image(self):
		cv2.imwrite("./output-image.png", self.outputImg)

	# Check if a point is inside a rectangle
	def rect_contains(self, rect, point) :
		if point[0] < rect[0] :
			return False
		elif point[1] < rect[1] :
			return False
		elif point[0] > rect[2] :
			return False
		elif point[1] > rect[3] :
			return False
		return True

	# Draw a point
	def draw_point(self, img, p, color ) :
		cv2.circle( img, p, 3, color, cv2.FILLED, cv2.LINE_AA, 0 )
	
	
	# Draw delaunay triangles
	def draw_delaunay(self, img, subdiv, delaunay_color) :
	
		triangleList = subdiv.getTriangleList()
		size = img.shape
		r = (0, 0, size[1], size[0])
	
		for t in triangleList :
		
			pt1 = (t[0], t[1])
			pt2 = (t[2], t[3])
			pt3 = (t[4], t[5])
	
			if self.rect_contains(r, pt1) and self.rect_contains(r, pt2) and self.rect_contains(r, pt3) :
			
				cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
				cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
				cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
 

	def create_triangulation(self):
		copyOfImg1 = self.Img.copy()

		inputSize = self.Img.shape
		targetSize = self.Img2.shape

		rect1 = (0,0,inputSize[1], inputSize[0])
		rect2 = (0,0,targetSize[1], targetSize[0])

		subdiv1 = cv2.Subdiv2D(rect1)
		subdiv2 = cv2.Subdiv2D(rect2)

		points1 = []
		points2 = []

		with open("inputPoints.txt") as file:
			for line in file:
				x, y = line.split(',')
				points1.append((int(x), int(y)))
		
		with open("targetPoints.txt") as file:
			for line in file:
				x, y = line.split(',')
				points2.append((int(x), int(y)))

		for point in points1:
			subdiv1.insert(point)
		
		for point in points2:
			subdiv2.insert(point)

		self.draw_delaunay(self.Img, subdiv1, (255, 255, 255))
		self.draw_delaunay(self.Img2, subdiv2, (255, 255, 255))
		self.draw_delaunay(copyOfImg1, subdiv2, (255, 255, 255))

		for point in points1:
			self.draw_point(self.Img, point, (0, 255, 255))
		
		for point in points2:
			self.draw_point(self.Img2, point, (0, 255, 255))
		
		for point in points2:
			self.draw_point(copyOfImg1, point, (0, 255, 255))

		R, C, B = self.Img.shape
		qImg = QtGui.QImage(self.Img.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		pix = QtGui.QPixmap(qImg)
		self.label.setPixmap(pix)

		R, C, B = self.Img2.shape
		qImg2 = QtGui.QImage(self.Img2.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		pix2 = QtGui.QPixmap(qImg2)
		self.label2.setPixmap(pix2)

		R, C, B = copyOfImg1.shape
		qImg3 = QtGui.QImage(copyOfImg1.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		
		self.label3 = QtWidgets.QLabel(self.centralwidget)
		pix3 = QtGui.QPixmap(qImg3)
		self.label3.setPixmap(pix3)
		self.label3.setAlignment(QtCore.Qt.AlignCenter)
		self.label3.setStyleSheet("border:0px")
		self.VerticalLayout3.addWidget(self.label3)

	def morph(self):
		return NotImplementedError

def main():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

main()
