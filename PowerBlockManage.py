#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 11:03:45 2019

@author: gamma-dna
"""
import time, os, sys, libtiepie, serial, visa
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5.QtWidgets import QGridLayout, QFrame, QLabel, QPushButton, QLineEdit, QApplication


class PowerBlock(object):
    
    
    def __init__(self):
        
        super(PowerBlock, self).__init__()
        
        self.initUI
        
    def initUI(self):
        
        oImage = QImage('/home/gamma-dna/.config/spyder/dna.jpg')
        sImage = oImage.scaled(QSize(900, 515))
        palette = QPalette
        palette.setBrush(QPalette.Window, QBrush(sImage))
        
        hline = QFrame()
        hline.setFrameShape(QFrame.Hline)
        hline.setFrameShadow(QFrame.Sunken)
        
        header_1 = QLabel()
        header_1.setText(u'Введите уровни каналов')
        header_1.setFont(QFont('Decorative', 14, 70))
        
        header_2 = QLabel()
        header_2.setText('Gate')
        header_2.setFont(QFont('Decorative', 14, 70))
        
        header_3 = QLabel()
        header_3.setText('Drain')
        header_3.setFont(QFont('Decorative', 14, 70))
        
        header_4 = QLabel()
        header_4.setText(u'Канал №1')
        header_4.setFont(QFont('Decorative', 14, 70))
        
        header_5 = QLabel()
        header_5.setText(u'Канал №2')
        header_5.setFont(QFont('Decorative', 14, 70))
        
        header_6 = QLabel()
        header_6.setText(u'Канал №3')
        header_6.setFont(QFont('Decorative', 14, 70))
        
        header_7 = QLabel()
        header_7.setText(u'Канал №4')
        header_7.setFont(QFont('Decorative', 14, 70))
        
        enter_btn = QPushButton(u'Ввод')
        enter_btn.setAutoDefault(True)
        enter_btn.setStyleSheet('background-color: #7fc7ff')
        enter_btn.setFont(QFont('Decorative', 14, 70))
        enter_btn.clicked.connect(self.enter)
        
        exit_btn = QPushButton(u'Ввод')
        exit_btn.setAutoDefault(True)
        exit_btn.setStyleSheet('background-color: #7fc7ff')
        exit_btn.setFont(QFont('Decorative', 14, 70))
        exit_btn.clicked.connect(self.exit)
        
        measure_btn = QPushButton(u'Ввод')
        measure_btn.setAutoDefault(True)
        measure_btn.setStyleSheet('background-color: #7fc7ff')
        measure_btn.setFont(QFont('Decorative', 14, 70))
        measure_btn.clicked.connect(self.exit)
        
        grid = QGridLayout()
        grid.addWidget(header_1, 0, 0)
        grid.addWidget(header_2, 0, 1)
        grid.addWidget(header_3, 0, 2)
        grid.addWidget(header_4, 1, 0)
        grid.addWidget(header_5, 2, 0)
        grid.addWidget(header_6, 3, 0)
        grid.addWidget(header_7, 4, 0)
        

if __name__ == '__main__':
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    data = PowerBlock
    app.exec_()
    sys.exit(0)