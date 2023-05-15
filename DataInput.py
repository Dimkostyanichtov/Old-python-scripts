#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:58:56 2018

@author: gamma-dna
"""
#Библиотека для виджетов эксперимента

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QGridLayout, QHBoxLayout, QDesktopWidget,
                             QVBoxLayout, QLabel, QAction, QFileDialog, QMessageBox, QComboBox)
from PyQt5.QtGui import QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QSize, Qt
import os



class DataInput(QWidget):
    
    
    def __init__(self):
        
        super(DataInput, self).__init__()
        
        self.initUI()
        
    
    def initUI(self):
        
        self.ex_event = False
                
        oImage = QImage('/home/gamma-dna/.config/spyder/dna.jpg')
        sImage = oImage.scaled(QSize(550, 455))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        
        self.header1 = QLabel(self)
        self.header1.setText(u'Информация об эксперименте: ')
        self.header1.setFont(QFont('Decorative', 14, 70))
        
        self.header2 = QLabel(self)
        self.header2.setText(u'Параметры процесса: ')
        self.header2.setFont(QFont('Decorative', 14, 70))
        
        self.empty = QLabel(self)
        self.empty.setText('')

        self.nameLabel = QLabel(self)
        self.nameLabel.setText(u'Эксперимент проводит: ')
        self.nameLabel.setFont(QFont('Decorative', 12, 60))
        self.nameLine = QLineEdit(self)
        
        self.expnameLabel = QLabel(self)
        self.expnameLabel.setText(u'Наименование эксперимента: ')
        self.expnameLabel.setFont(QFont('Decorative', 12, 60))
        self.expnameLine = QLineEdit(self)
       
        self.expnumbLabel = QLabel(self)
        self.expnumbLabel.setText(u'№ эксперимента: ')
        self.expnumbLabel.setFont(QFont('Decorative', 12, 60))
        self.expnumbLine = QLineEdit(self)

        self.filenameLabel = QLabel(self)
        self.filenameLabel.setText(u'''Выберите файл с данными
об устройствах: ''')
        self.filenameLabel.setFont(QFont('Decorative', 12, 60))
        self.filenameLine = QLineEdit(self)
        self.filenameLine.setText('/home/gamma-dna/.config/spyder/firstprob.json')
        
        self.savenameLabel = QLabel(self)
        self.savenameLabel.setText(u'''Выберите файл для сохранения: ''')
        self.savenameLabel.setFont(QFont('Decorative', 12, 60))
        self.savenameLine = QLineEdit(self)
        self.savenameLine.setText('/home/gamma-dna/.config/spyder/firstprobes.json')
        
        self.delayLabel = QLabel(self)
        self.delayLabel.setText(u'''Введите время задержки 
мобилизации (в минутах): ''')
        self.delayLabel.setFont(QFont('Decorative', 12, 60))
        self.delayLine = QLineEdit(self)
        self.delayLine.setFixedSize(50, 30)
        
        self.timeLabel = QLabel(self)
        self.timeLabel.setText(u'''Введите время полимеризации
(в секундах): ''')
        self.timeLabel.setFont(QFont('Decorative', 12, 60))
        self.timeLine = QLineEdit(self)
        self.timeLine.setFixedSize(50, 30)
          
        openFile = QAction(QIcon('/home/gamma-dna/.config/spyder/openicon.png'), 'Open', self)
        openFile.setStatusTip('Open file')
        openFile.triggered.connect(self.showDialog)
        
        chbtn = QPushButton(self)
        chbtn.setIcon(QIcon('/home/gamma-dna/.config/spyder/openicon.png'))
        chbtn.setIconSize(QSize(20, 15))
        chbtn.clicked.connect(self.showDialog)
        
        chbtns = QPushButton(self)
        chbtns.setIcon(QIcon('/home/gamma-dna/.config/spyder/SaveIcon.png'))
        chbtns.setIconSize(QSize(20, 15))
        chbtns.clicked.connect(self.saveDialog)
        
        btn = QPushButton(u'Запуск', self)
        btn.setAutoDefault(True)
        btn.setStyleSheet("background-color: #7fc7ff")
        btn.setFont(QFont('Decorative', 12, 65))
        btn.clicked.connect(self.saving) 

        mainwindow = QVBoxLayout()
        self.setLayout(mainwindow)
        
        vertical1 = QHBoxLayout()
        vertical1.addWidget(self.header1)
        self.setLayout(vertical1)
        
        grid1 = QGridLayout()
        grid1.addWidget(self.nameLabel, 1, 0)
        grid1.addWidget(self.nameLine, 1, 1)
        grid1.addWidget(self.expnameLabel, 2, 0)
        grid1.addWidget(self.expnameLine, 2, 1)
        grid1.addWidget(self.expnumbLabel, 3, 0)
        grid1.addWidget(self.expnumbLine, 3, 1)
        grid1.addWidget(self.filenameLabel, 4, 0)
        grid1.addWidget(self.filenameLine, 4, 1)
        grid1.addWidget(self.savenameLabel, 5, 0)
        grid1.addWidget(self.savenameLine, 5, 1)
        grid1.addWidget(chbtn, 4, 2)
        grid1.addWidget(chbtns, 5, 2)
        
        grid2 = QGridLayout()
        grid2.addWidget(self.delayLabel, 0, 0)
        grid2.addWidget(self.delayLine, 0, 1)
        grid2.addWidget(self.empty, 0, 2)
        grid2.addWidget(self.timeLabel, 1, 0)
        grid2.addWidget(self.timeLine, 1, 1)
        
        vertical2 = QHBoxLayout()
        vertical2.addWidget(self.header2)
        self.setLayout(vertical1)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        
        mainwindow.addLayout(vertical1) 
        mainwindow.addLayout(grid1)
        mainwindow.addStretch(1)
        mainwindow.addLayout(vertical2)
        mainwindow.addLayout(grid2)
        mainwindow.addStretch(1)
        mainwindow.addLayout(hbox)
        
        self.setLayout(hbox)
        self.setLayout(grid1)
        self.setToolTip(u'Пожалуйста введите информацию о проводимом эксперименте')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setFixedSize(550, 455)
        self.center()
        self.setWindowTitle(u'Ввод данных')
        self.show()        
            
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    
    def showDialog(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/gamma-dna/.config/spyder')[0]
        self.filenameLine.setText(fname)
        
        
    def saveDialog(self):
        
        put = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Save file', put)[0]
        self.savenameLine.setText(fname)
    
    
    def saving(self):
        
        if (len(self.nameLine.text()) == 0 or len(self.expnameLine.text()) == 0 or len(self.expnumbLine.text()) == 0 or len(self.filenameLine.text()) == 0 or
len(self.savenameLine.text()) == 0 or len(self.delayLine.text()) == 0 or len(self.timeLine.text()) == 0):
            reply = QMessageBox.critical(self, 'Message', u'Заполните пустые поля!!!')
            reply
            
        else:
            self.myname = self.nameLine.text()
            self.expname = self.expnameLine.text()
            self.expnumb = self.expnumbLine.text()
            self.filename = self.filenameLine.text()
            self.savename = self.savenameLine.text()
            self.ex_event = True
            self.close()   
    
        
    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()
            
        elif e.key() == Qt.Key_Return:
            self.saving()        