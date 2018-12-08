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
		self.subdiv1 = None
		self.subdiv2 = None
		self.affineTransCoeffs = []
		self.points1 = None
		self.points2 = None
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
		
			p1 = (t[0], t[1])
			p2 = (t[2], t[3])
			p3 = (t[4], t[5])
	
			if self.rect_contains(r, p1) and self.rect_contains(r, p2) and self.rect_contains(r, p3) :
			
				cv2.line(img, p1, p2, delaunay_color, 1, cv2.LINE_AA, 0)
				cv2.line(img, p2, p3, delaunay_color, 1, cv2.LINE_AA, 0)
				cv2.line(img, p3, p1, delaunay_color, 1, cv2.LINE_AA, 0)
 

	def create_triangulation(self):
		triangulationOutputImg = self.Img.copy()
		triangulatedInput = self.Img.copy()
		triangulatedTarget = self.Img2.copy()

		inputSize = triangulatedInput.shape
		targetSize = triangulatedTarget.shape

		rect1 = (0,0,inputSize[1], inputSize[0])
		rect2 = (0,0,targetSize[1], targetSize[0])

		self.subdiv1 = cv2.Subdiv2D(rect1)
		self.subdiv2 = cv2.Subdiv2D(rect2)

		self.points1 = []
		self.points2 = []

		with open("inputPoints.txt") as file:
			for line in file:
				x, y = line.split(',')
				self.points1.append((int(x), int(y)))
		
		with open("targetPoints.txt") as file:
			for line in file:
				x, y = line.split(',')
				self.points2.append((int(x), int(y)))

		for point in self.points1:
			self.subdiv1.insert(point)
		
		for point in self.points2:
			self.subdiv2.insert(point)

		self.draw_delaunay(triangulatedInput, self.subdiv1, (255, 255, 255))
		self.draw_delaunay(triangulatedTarget, self.subdiv2, (255, 255, 255))
		self.draw_delaunay(triangulationOutputImg, self.subdiv2, (255, 255, 255))

		for point in self.points1:
			self.draw_point(triangulatedInput, point, (0, 255, 255))
		
		for point in self.points2:
			self.draw_point(triangulatedTarget, point, (0, 255, 255))
		
		for point in self.points2:
			self.draw_point(triangulationOutputImg, point, (0, 255, 255))

		R, C, B = triangulatedInput.shape
		qImg = QtGui.QImage(triangulatedInput.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		pix = QtGui.QPixmap(qImg)
		self.label.setPixmap(pix)

		R, C, B = triangulatedTarget.shape
		qImg2 = QtGui.QImage(triangulatedTarget.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		pix2 = QtGui.QPixmap(qImg2)
		self.label2.setPixmap(pix2)

		R, C, B = triangulationOutputImg.shape
		qImg3 = QtGui.QImage(triangulationOutputImg.data, C, R, 3 * C, QtGui.QImage.Format_RGB888).rgbSwapped()
		
		self.label3 = QtWidgets.QLabel(self.centralwidget)
		pix3 = QtGui.QPixmap(qImg3)
		self.label3.setPixmap(pix3)
		self.label3.setAlignment(QtCore.Qt.AlignCenter)
		self.label3.setStyleSheet("border:0px")
		self.VerticalLayout3.addWidget(self.label3)

	def morph(self):
		self.affineTransformEstimation(self.subdiv1, self.subdiv2)

	def affineTransformEstimation(self, sd1, sd2):
		inputTriangles = sd1.getTriangleList()
		targetTriangles = sd2.getTriangleList()
		for i in range(len(inputTriangles)):
			
			inputPoint1 = (inputTriangles[i][0], inputTriangles[i][1])
			inputPoint2 = (inputTriangles[i][2], inputTriangles[i][3])
			inputPoint3 = (inputTriangles[i][4], inputTriangles[i][5])

			targetPoint1 = (targetTriangles[i][0], targetTriangles[i][1])
			targetPoint2 = (targetTriangles[i][2], targetTriangles[i][3])
			targetPoint3 = (targetTriangles[i][4], targetTriangles[i][5])
			
			mArray = np.array([[inputPoint1[0], inputPoint1[1], 1, 0 ,0 ,0],[0, 0, 0, inputPoint1[0], inputPoint1[1], 1],[inputPoint2[0], inputPoint2[1], 1, 0 ,0 ,0], [0, 0, 0, inputPoint2[0], inputPoint2[1], 1], [inputPoint3[0], inputPoint3[1], 1, 0 ,0 ,0], [0, 0, 0, inputPoint3[0], inputPoint3[1], 1]])
			invMArray = np.linalg.inv(mArray)

			bArray = np.array([targetPoint1[0], targetPoint1[1], targetPoint2[0], targetPoint2[1], targetPoint3[0], targetPoint3[1]])

			self.affineTransCoeffs.append(invMArray.dot(bArray))


	def isInTriangle(self, point, triangle):
		p1 = (triangle[0], triangle[1])
		p2 = (triangle[2], triangle[3])
		p3 = (triangle[4], triangle[5])

		# test the first edge
		# edge equation is y = mx + c
		if (p1[0] - p2[0]) == 0:
			if (p1[0] == point[0]):
				return True # on the edge
			elif not (np.sign(p3[1] - (m * p3[0]) - c) == np.sign(point[1] - (m * point[0]) - c)):
				return False # cannot be in the triangle
		else:
			m = (p1[1] - p2[1]) / (p1[0] - p2[0])
			c = p1[1] - (m * p1[0])
			if np.sign(point[1] - (m * point[0]) - c) == 0:
				return True # on the edge
			elif not (np.sign(p3[1] - (m * p3[0]) - c) == np.sign(point[1] - (m * point[0]) - c)):
				return False # cannot be in the triangle
		
		# test the second edge
		if (p1[0] - p3[0]) == 0:
			if (p1[0] == point[0]):
				return True # on the edge
			elif not (np.sign(p2[1] - (m * p2[0]) - c) == np.sign(point[1] - (m * point[0]) - c)):
				return False # cannot be in the triangle
		else:
			m = (p1[1] - p3[1]) / (p1[0] - p3[0])
			c = p1[1] - (m * p1[0])
			if np.sign(point[1] - (m * point[0]) - c) == 0:
				return True # on the edge
			elif not (np.sign(p2[1] - (m * p2[0]) - c) == np.sign(point[1] - (m * point[0]) - c)):
				return False # cannot be in the triangle
		
		# test the third edge
		if (p2[0] - p3[0]) == 0:
			if (p2[0] == point[0]):
				return True # on the edge
			elif not (np.sign(p1[1] - (m * p1[0]) - c) == np.sign(point[1] - (m * point[0]) - c)):
				return False # cannot be in the triangle
		else:
			m = (p2[1] - p3[1]) / (p2[0] - p3[0])
			c = p2[1] - (m * p2[0])
			if np.sign(point[1] - (m * point[0]) - c) == 0:
				return True # on the edge
			elif not (np.sign(p1[1] - (m * p1[0]) - c) == np.sign(point[1] - (m * point[0]) - c)):
				return False # cannot be in the triangle
		return True

def main():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

main()
