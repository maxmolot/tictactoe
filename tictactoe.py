#!/usr/bin/python3

"""
Creator: maxmolot@gmail.com
This is how I learned Python3-PyQt5
"""

"""
Bugs:
	set board unclickable after click
Possible Features:
	menubar
TODO:
	clean up (messy code, unused variables)
	find better way to emulate do-while loop in python
"""


import sys
import random
import time
from PyQt5.QtWidgets import (QWidget, QGridLayout, 
	QPushButton, QApplication, QMainWindow,
	QAction, QMenu, QMenuBar, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from PyQt5.QtCore import QSize, QTimer, QEventLoop, pyqtSignal
import numpy as np

#game logic
class TicTacToe():
	isClosed = False
	
	def __init__(self):
		app = QApplication(sys.argv)
		self.initBoard()
		self.timer = QTimer()
		self.w = Window(self.board)
		self.w.resetSignal.connect(self.reset)
		self.closed = False
		self.run()
		sys.exit(app.exec_())
		
	def initBoard(self):
		board = []
		size = QSize(475, 300)
		layout = [['','',''],['','',''],['','','']]

		for row in layout:
			subArray = []
			for entry in row:
				button = MyButton()
				button.setFixedSize(size)
				button.setIconSize(size)
				button.setStyleSheet("background-color: white;")
				subArray.append(button)
			board.append(subArray)
		self.board = board
		

	def run(self):
		self.isWinner = False;
		self.moves = 0
		num = 0.4#random.random()
		if(num < 0.5):
			while (not self.isWinner and self.moves != 9):
				loop = QEventLoop()
				self.w.moveDone.connect(loop.quit)
				loop.exec_()
				self.moves += 1
				self.isWinner = self.checkWinner()
				self.w.repaint()
				if not self.isWinner and self.moves != 9:
					self.oMove()
					self.moves += 1
				self.isWinner = self.checkWinner()
		else: 		
			while (not self.isWinner and self.moves != 9):
				self.oMove()
				self.moves += 1
				self.isWinner = self.checkWinner()
				self.w.repaint()
				if not self.isWinner and self.moves != 9:
					loop = QEventLoop()
					self.w.moveDone.connect(loop.quit)
					loop.exec_()
					self.moves += 1
					self.w.repaint()
					self.isWinner = self.checkWinner()
		self.w.raiseWinner(' ')
		
	def oMove(self):
		time.sleep(0.4)
		moved = False
		if (self.goodMove('o')):
			moved = True
		elif (self.goodMove('x')):
			moved = True
		while(not moved):
			randRow = random.choice(self.board)
			randEntry = random.choice(randRow)
			if(randEntry.type == 'w'):
				randEntry.changeIcon('o')
				moved = True
			
	
	def goodMove(self, token):
		#check rows
		for row in self.board:
			if ( self.checkGood(row, token) ):
				return True
		#check column
		transposedBoard = np.transpose(self.board)
		for column in transposedBoard:
			if( self.checkGood(column, token) ):
				return True
		#check diag
		length = 0
		diagonal = []
		secondDiag = []
		try:
			length = len(self.board)
		except IndexError:
			print('for some reason the dimension of the board is 0')
			
		for i in range(0, length):
			diagonal.append(self.board[i][i])
		if (self.checkGood(diagonal, token)) :
			return True
		
		for i in range(0, length):
			j = length - 1 - i 
			secondDiag.append(self.board[i][j])
		if (self.checkGood(secondDiag, token)):
			return True
		return False
		
	def checkGood(self, array, token):
		tokenCounter = 0
		otherCounter = 0
		wCounter = 0
		for entry in array:
			if entry.type == token:
				tokenCounter += 1
			elif entry.type == 'w':
				wCounter += 1
			elif entry.type != token:
				otherCounter += 1 
		if (tokenCounter == len(array) - 1 and otherCounter == 0):
			for entry in array:
				if(entry.type == 'w'):
					entry.changeIcon('o')
			return True
		return False 
			
	def checkWinner(self):
		#check rows
		for row in self.board:
			if ( self.checkSame(row) ):
				return True
		#check column
		transposedBoard = np.transpose(self.board)
		for column in transposedBoard:
			if( self.checkSame(column) ):
				return True
		#check diag
		length = 0
		diagonal = []
		secondDiag = []
		try:
			length = len(self.board)
		except IndexError:
			print('for some reason the dimension of the board is 0')
			
		for i in range(0, length):
			diagonal.append(self.board[i][i])
		if (self.checkSame(diagonal)) :
			return True
		
		for i in range(0, length):
			j = length - 1 - i 
			secondDiag.append(self.board[i][j])
		if (self.checkSame(secondDiag)):
			return True
			
	def checkSame(self, array):
		xCounter = 0
		oCounter = 0
		wCounter = 0
		for entry in array:
			if entry.type == 'x':
				xCounter += 1
			elif entry.type == 'o':
				oCounter += 1
			else:
				wCounter += 1
		if (wCounter == 0 and oCounter == 0):
			self.w.raiseWinner('x')
			return True
		elif (wCounter == 0 and xCounter == 0):
			self.w.raiseWinner('o')
			return True 
			
	def reset(self):
		for row in self.board:
			for entry in row:
				entry.changeIcon(' ')
		self.run()
#create a new button with attribute type
class MyButton(QPushButton):
	
	moveDone = pyqtSignal()
	
	def __init__(self):
		super().__init__()
		self.type = 'w' #w is for white
		self.oPixmap = QPixmap('O.png')
		self.xPixmap = QPixmap('X.png')
		self.oIcon = QIcon(self.oPixmap)
		self.xIcon = QIcon(self.xPixmap)
		
	def changeIcon(self, icon):
		if icon == 'o' :
			self.setIcon(self.oIcon)
			self.type = 'o'
			self.setEnabled(False)
		elif icon == 'x':
			self.setIcon(self.xIcon)
			self.type = 'x'
			self.setEnabled(False)
		else:
			self.setIcon(QIcon())
			self.type = 'w'
			self.setEnabled(True)

		
#create central widget 
class MyWidget(QWidget):
	
	moveDone = pyqtSignal()
	resetSignal = pyqtSignal()
	def __init__(self, board):
		super().__init__()
		self.clicked = False
		self.oPixmap = QPixmap('o.png')
		self.xPixmap = QPixmap('x.png')
		self.oIcon = QIcon(self.oPixmap)
		self.xIcon = QIcon(self.xPixmap)

		self.initWid(board)

	def initWid(self, board):
		grid = QGridLayout()

		columnNum = 0
		for row in board:
			rowNum = 0
			for entry in row:
				entry.clicked.connect(self.changeToX)
				grid.addWidget(entry, rowNum, columnNum)
				rowNum += 1
			columnNum += 1
		
		self.board = board
		self.setLayout(grid)

	def changeToX(self):
		button = self.sender()
		button.changeIcon('x')
		self.moveDone.emit()
		
	def raiseWinner(self, winner):
		self.setStyleSheet("background-color: white;")
		box = MyMessageBox()
		#box.setTitle('Winner Winner Chicken Dinner')
		if (winner == 'o' or winner == 'x'):
			box.setText(winner + ' Wins!')
		else:
			box.setText("Cat's Game!")
		okButton = QMessageBox.Ok
		closeButton = QMessageBox.Close
		box.setStandardButtons(okButton | closeButton)
		box.closeMessageSignal.connect(self.reset)

		if box.exec_() == QMessageBox.Close:
			sys.exit()
		else:
			self.reset()
			
	def reset(self):
		self.resetSignal.emit()
		
class MyMessageBox(QMessageBox):

	closeMessageSignal = pyqtSignal()
	def __init__(self):
		super().__init__()
		
	def closeEvent(self, event):
		self.closeMessageSignal.emit()
		
#create main window, unchangeable size
class Window(QMainWindow):
	moveDone = pyqtSignal()
	resetSignal = pyqtSignal()
	def __init__(self, board):
		super().__init__()
		self.initUI(board)
		
	def initUI(self, board):
		width = 1500
		height = 1000
		self.setStyleSheet("background-color: black;")
		self.resize(width, height)
		self.setMaximumSize(width, height)
		self.setMinimumSize(width, height)
		self.setWindowTitle('Tic Tac Toe')
		self.wid = MyWidget(board)
		self.wid.moveDone.connect(self.moved)
		self.wid.resetSignal.connect(self.reset)
		self.setCentralWidget(self.wid)
		self.board = self.wid.board
		self.setWindowIcon(QIcon('tictactoe.png'))
		self.show()
       
	def moved(self):
		self.moveDone.emit()
		
	def closeEvent(self, event):
		sys.exit()
		event.accept()
		
	def raiseWinner(self, winner):
		self.wid.raiseWinner(winner)
	
	def reset(self):
		self.resetSignal.emit()
		
if __name__ == '__main__':
	tictactoe = TicTacToe()
	#tictactoe.run()
