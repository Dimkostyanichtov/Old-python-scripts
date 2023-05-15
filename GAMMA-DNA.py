#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:33:38 2018

@author: gamma-dna
"""
# Библиотека для работы с измерительным стендом
# При написании скриптов желательно подключать первым насос
# Автор Д.К. Товмаченко

import json, sys, io, datetime, visa, os, time, commands, subprocess, serial, yaml, libtiepie, pickle#, bitstring
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QGridLayout, QHBoxLayout, QDesktopWidget, QMainWindow, QFrame, QProgressBar,
                             QVBoxLayout, QLabel, QAction, QFileDialog, QMessageBox, QApplication, QTextBrowser, QComboBox, QDialog)
from PyQt5.QtGui import QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QSize, Qt, QCoreApplication, QThread, pyqtSignal



# Класс для обработки исключений
class Equipment_Exceptions(Exception):
    
    pass 



# Класс для GUI скрипта
class DataInput(QWidget):
    
    
    def __init__(self):
        
        super(DataInput, self).__init__()
        
        self.initUI()
        
    
    def initUI(self):
        
        self.mode = ''
        self.execute_event = False
                
        self.statusbar = QMainWindow()
        self.statusbar.statusBar().showMessage('ok')
                
        oImage = QImage('/home/gamma-dna/.config/spyder/dna.jpg')
        sImage = oImage.scaled(QSize(1000, 755))
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
        self.nameLine.setText('Username')
        
        self.experimentnameLabel = QLabel(self)
        self.experimentnameLabel.setText(u'Наименование эксперимента: ')
        self.experimentnameLabel.setFont(QFont('Decorative', 12, 60))
        self.experimentnameLine = QLineEdit(self)
        self.experimentnameLine.setText('Experiment')
       
        self.experimentnumberLabel = QLabel(self)
        self.experimentnumberLabel.setText(u'№ эксперимента: ')
        self.experimentnumberLabel.setFont(QFont('Decorative', 12, 60))
        self.experimentnumberLine = QLineEdit(self)
        self.experimentnumberLine.setText('1')

        self.filenameLabel = QLabel(self)
        self.filenameLabel.setText(u'''Выберите файл с данными
об устройствах: ''')
        self.filenameLabel.setFont(QFont('Decorative', 12, 60))
        self.filenameLine = QLineEdit(self)
        self.filenameLine.setText('/home/gamma-dna/.config/spyder/Devises.json')
        
        self.savenameLabel = QLabel(self)
        self.savenameLabel.setText(u'Выберите файл для сохранения: ')
        self.savenameLabel.setFont(QFont('Decorative', 12, 60))
        self.savenameLine = QLineEdit(self)
        self.savenameLine.setText('/home/gamma-dna/.config/spyder/firstprobes.json')
        
        self.delayLabel = QLabel(self)
        self.delayLabel.setText(u'''Введите время задержки 
мобилизации (в минутах): ''')
        self.delayLabel.setFont(QFont('Decorative', 12, 60))
        self.delayLine = QLineEdit(self)
        self.delayLine.setFixedSize(50, 30)
        self.delayLine.setText('1')
        self.delayLine.setAlignment(Qt.AlignCenter)
        
        self.timeLabel = QLabel(self)
        self.timeLabel.setText(u'''Введите время полимеризации
(в секундах): ''')
        self.timeLabel.setFont(QFont('Decorative', 12, 60))
        self.timeLine = QLineEdit(self)
        self.timeLine.setFixedSize(50, 30)
        self.timeLine.setText('10')
        self.timeLine.setAlignment(Qt.AlignCenter)
        
        self.textBrowser = QTextBrowser(self)
        
        self.textLabel = QLabel(self)
        self.textLabel.setText(u'Ход эксперимента: ')
        self.textLabel.setFont(QFont('Decorative', 12, 60))
        
        self.hline = QFrame()
        self.hline.setFrameShape(QFrame.HLine)
        self.hline.setFrameShadow(QFrame.Sunken)
        
        self.comboLabel = QLabel(self)
        self.comboLabel.setText(u'Выберите действие: ')
        self.comboLabel.setFont(QFont('Decorative', 14, 70))
        self.combo = QComboBox(self)
        self.combo.addItems([u'         Подключение', u'          Отключение', u'       Продувка ячейки', u'       Промывка ячейки', '                  #1', u'      Измерение уровня', u' Выставление уровней БП'])
        self.combo.setFont(QFont('Decorative', 12, 60))
        self.combo.setFixedSize(230, 30)
        
        self.progress = QProgressBar(self)
        self.progress.resize(200, 70)
        self.progress.hide()
        
        self.processname = QLabel(self)
        self.processname.setFont(QFont('Decorative', 10, 60))
        self.processname.hide()
          
        openFile = QAction(QIcon('/home/gamma-dna/.config/spyder/openicon.png'), 'Open', self)
        openFile.setStatusTip('Open file')
        openFile.triggered.connect(self.showDialog)
        
        chbtn = QPushButton(self)
        chbtn.setIcon(QIcon('/home/gamma-dna/.config/spyder/openicon.png'))
        chbtn.setIconSize(QSize(20, 15))
        chbtn.clicked.connect(self.showDialog)
        chbtn.setStyleSheet("background-color: white")
        
        self.questbtn = QPushButton(self)
        self.questbtn.setIcon(QIcon('/home/gamma-dna/.config/spyder/QuestionIcon.webp'))
        self.questbtn.setIconSize(QSize(20, 15))
        self.questbtn.setStyleSheet("background-color: white")
        self.questbtn.clicked.connect(self.showHelp)
        
        savebtn = QPushButton(self)
        savebtn.setIcon(QIcon('/home/gamma-dna/.config/spyder/SaveIcon.png'))
        savebtn.setIconSize(QSize(20, 15))
        savebtn.clicked.connect(self.saveDialog)
        savebtn.setStyleSheet("background-color: white")
        
        self.btn = QPushButton(u'Запуск', self)
        self.btn.setAutoDefault(True)
        self.btn.setStyleSheet("background-color: #7fc7ff")
        self.btn.setFont(QFont('Decorative', 12, 65))
        self.btn.clicked.connect(self.saving) 
        
        self.exitbtn = QPushButton(u'Выход', self)
        self.exitbtn.setAutoDefault(True)
        self.exitbtn.setStyleSheet("background-color: #7fc7ff")
        self.exitbtn.setFont(QFont('Decorative', 12, 65))
        self.exitbtn.clicked.connect(self.exit_form)
        
        self.stopbtn = QPushButton(u'Стоп', self)
        self.stopbtn.setAutoDefault(True)
        self.stopbtn.setStyleSheet("background-color: #7fc7ff")
        self.stopbtn.setFont(QFont('Decorative', 12, 65))
        self.stopbtn.clicked.connect(self.stop_thread)
        self.stopbtn.setDisabled(True)
        
        self.clsbtn = QPushButton(u'Очистить', self)
        self.clsbtn.setFont(QFont('Decorative', 12, 60))
        self.clsbtn.clicked.connect(self.clear)
        
        self.pointLabel = QLabel(self)
        self.pointLabel.setText(u'Выберите рабочую точку: ')
        self.pointLabel.setFont(QFont('Decorative', 12, 60))
        self.point = QComboBox(self)
        self.point.addItems(['     0 V', '   0,5 V', '  0,75 V', '   1,0 V', '  1,25 V', '   1,5 V', '  1,75 V', '   2,0 V'])
        self.point.setFont(QFont('Decorative', 12, 60))
        self.point.setFixedSize(85, 30)

        mainwindow = QVBoxLayout()
        mainwindow_left = QVBoxLayout()
        mainwindow_right = QVBoxLayout()
        mainwindow_top = QHBoxLayout()
        mainwindow_down = QVBoxLayout()
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.header1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.header2)
        
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn)
        hbox3.addWidget(self.stopbtn)
        hbox3.addWidget(self.exitbtn)
        hbox3.addStretch(1)
        hbox3.addWidget(self.questbtn)
        
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.textLabel)
        hbox4.addStretch(1)
        hbox4.addWidget(self.clsbtn)
        
        header_1 = QLabel()
        header_1.setText(u'Введите уровни каналов:')
        header_1.setFont(QFont('Decorative', 14, 70))
        
        hbox5 = QHBoxLayout()
        hbox5.addWidget(header_1)
        
        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.comboLabel)
        hbox6.addWidget(self.combo)
        hbox6.addStretch(1)
        
        header_gate = QLabel()
        header_gate.setText(' Gate')
        header_gate.setFont(QFont('Decorative', 12, 60))
        
        header_drain = QLabel()
        header_drain.setText(' Drain')
        header_drain.setFont(QFont('Decorative', 12, 60))
        
        header_ch1 = QLabel()
        header_ch1.setText(u'Канал №1')
        header_ch1.setFont(QFont('Decorative', 12, 60))
        self.drain_1 = QLineEdit(self)
        self.drain_1.setText('0')
        self.drain_1.setFixedSize(50, 30)
        self.drain_1.setAlignment(Qt.AlignCenter)
        self.gate_1 = QLineEdit(self)
        self.gate_1.setText('0')
        self.gate_1.setFixedSize(50, 30)
        self.gate_1.setAlignment(Qt.AlignCenter)
        
        header_ch2 = QLabel()
        header_ch2.setText(u'Канал №2')
        header_ch2.setFont(QFont('Decorative', 12, 60))
        self.drain_2 = QLineEdit(self)
        self.drain_2.setText('0')
        self.drain_2.setFixedSize(50, 30)
        self.drain_2.setAlignment(Qt.AlignCenter)
        self.gate_2 = QLineEdit(self)
        self.gate_2.setText('0')
        self.gate_2.setFixedSize(50, 30)
        self.gate_2.setAlignment(Qt.AlignCenter)
        
        header_ch3 = QLabel()
        header_ch3.setText(u'Канал №3')
        header_ch3.setFont(QFont('Decorative', 12, 60))
        self.drain_3 = QLineEdit(self)
        self.drain_3.setText('0')
        self.drain_3.setFixedSize(50, 30)
        self.drain_3.setAlignment(Qt.AlignCenter)
        self.gate_3 = QLineEdit(self)
        self.gate_3.setText('0')
        self.gate_3.setFixedSize(50, 30)
        self.gate_3.setAlignment(Qt.AlignCenter)
        
        header_ch4 = QLabel()
        header_ch4.setText(u'Канал №4')
        header_ch4.setFont(QFont('Decorative', 12, 60))
        self.drain_4 = QLineEdit(self)
        self.drain_4.setText('0')
        self.drain_4.setFixedSize(50, 30)
        self.drain_4.setAlignment(Qt.AlignCenter)
        self.gate_4 = QLineEdit(self)
        self.gate_4.setText('0')
        self.gate_4.setFixedSize(50, 30)
        self.gate_4.setAlignment(Qt.AlignCenter)
        
        grid1 = QGridLayout()
        grid1.addWidget(self.nameLabel, 1, 0)
        grid1.addWidget(self.nameLine, 1, 1)
        grid1.addWidget(self.experimentnameLabel, 2, 0)
        grid1.addWidget(self.experimentnameLine, 2, 1)
        grid1.addWidget(self.experimentnumberLabel, 3, 0)
        grid1.addWidget(self.experimentnumberLine, 3, 1)
        grid1.addWidget(self.filenameLabel, 4, 0)
        grid1.addWidget(self.filenameLine, 4, 1)
        grid1.addWidget(self.savenameLabel, 5, 0)
        grid1.addWidget(self.savenameLine, 5, 1)
        grid1.addWidget(chbtn, 4, 2)
        grid1.addWidget(savebtn, 5, 2)
        
        grid2 = QGridLayout()
        grid2.addWidget(self.delayLabel, 0, 0)
        grid2.addWidget(self.delayLine, 0, 1)
        grid2.addWidget(self.empty, 0, 2)
        grid2.addWidget(self.timeLabel, 1, 0)
        grid2.addWidget(self.timeLine, 1, 1)
        grid2.addWidget(self.pointLabel, 2, 0)
        grid2.addWidget(self.point, 2, 1)
        grid2.addWidget(self.empty, 3, 1)
        
        grid3 = QGridLayout()
        grid3.addWidget(self.empty, 0, 0)
        grid3.addWidget(self.empty, 0, 1)
        grid3.addWidget(header_gate, 0, 2)
        grid3.addWidget(self.empty, 0, 3)
        grid3.addWidget(header_drain, 0, 4)
        grid3.addWidget(self.empty, 0, 5)
        grid3.addWidget(header_ch1, 1, 0)
        grid3.addWidget(header_ch2, 2, 0)
        grid3.addWidget(header_ch3, 3, 0)
        grid3.addWidget(header_ch4, 4, 0)
        grid3.addWidget(self.empty, 1, 1)
        grid3.addWidget(self.empty, 2, 1)
        grid3.addWidget(self.empty, 3, 1)
        grid3.addWidget(self.empty, 4, 1)
        grid3.addWidget(self.gate_1, 1, 2)
        grid3.addWidget(self.gate_2, 2, 2)
        grid3.addWidget(self.gate_3, 3, 2)
        grid3.addWidget(self.gate_4, 4, 2)
        grid3.addWidget(self.empty, 1, 3)
        grid3.addWidget(self.empty, 2, 3)
        grid3.addWidget(self.empty, 3, 3)
        grid3.addWidget(self.empty, 4, 3)
        grid3.addWidget(self.drain_1, 1, 4)
        grid3.addWidget(self.drain_2, 2, 4)
        grid3.addWidget(self.drain_3, 3, 4)
        grid3.addWidget(self.drain_4, 4, 4)
        grid3.addWidget(self.empty, 5, 0)
        
        mainwindow.addLayout(mainwindow_top)
        mainwindow_top.addLayout(mainwindow_left)
        mainwindow_top.addLayout(mainwindow_right)
        mainwindow.addLayout(mainwindow_down)
        
        mainwindow_left.addLayout(hbox1) 
        mainwindow_left.addLayout(grid1)
        mainwindow_left.addWidget(self.empty)
        mainwindow_left.addLayout(hbox2)
        mainwindow_left.addLayout(grid2)
        mainwindow_left.addLayout(hbox5)
        mainwindow_left.addLayout(grid3)
        mainwindow_left.addLayout(hbox6)
        
        mainwindow_right.addLayout(hbox4)
        mainwindow_right.addWidget(self.textBrowser)
        mainwindow_right.addWidget(self.processname)
        mainwindow_right.addWidget(self.progress)
        
        mainwindow_down.addWidget(self.hline)
        mainwindow_down.addStretch(1)
        mainwindow_down.addLayout(hbox3)
        mainwindow_down.addStretch(1)
        
        self.setLayout(mainwindow)
        self.setToolTip(u'Пожалуйста введите информацию о проводимом эксперименте')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setFixedSize(1000, 755)
        self.center()
        self.setWindowTitle('GAMMA-DNA')
        self.show()        
            
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    
    def showDialog(self):
        
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/gamma-dna/.config/spyder')[0]
        self.filenameLine.setText(fname)
       
        
    def clear(self):
        
        self.textBrowser.setText('')
        
        
    def showHelp(self):
        
        helpfile = open('/home/gamma-dna/.config/spyder/helptext')        
        helptext = helpfile.read()
        dialog = QDialog()
        dialog.setFixedSize(550, 250)
        dialog.setWindowTitle(u'Справка')
        text = QTextBrowser(dialog)
        text.setFixedSize(550, 250)
        text.setText(helptext)
        text.setFont(QFont('Decorative', 12))
        dialog.exec_() 
        
        
    def saveDialog(self):
        
        put = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Save file', put)[0]
        self.savenameLine.setText(fname)
        
    
    def saving(self):
        
        self.execute_event = False
        
        if (len(self.nameLine.text()) == 0 or len(self.experimentnameLine.text()) == 0 or len(self.experimentnumberLine.text()) == 0 or len(self.filenameLine.text()) == 0 or
len(self.savenameLine.text()) == 0 or len(self.delayLine.text()) == 0 or len(self.timeLine.text()) == 0):
            reply = QMessageBox.critical(self, u'Ошибка!', u'Заполните пустые поля!')
            self.stopbtn.setDisabled(True)
            self.btn.setDisabled(False)
            self.exitbtn.setDisabled(False)
            reply
            
        elif float(self.delayLine.text()) == 0.0 or float(self.delayLine.text()) < 0.0:
            reply = QMessageBox.critical(self, u'Ошибка!', u'''Значение задержки мобилизации 
должно быть больше 0!''')
            self.stopbtn.setDisabled(True)
            self.btn.setDisabled(False)
            self.exitbtn.setDisabled(False)
            reply
        
        elif float(self.timeLine.text()) == 0.0 or float(self.timeLine.text()) < 0.0:
            reply = QMessageBox.critical(self, u'Ошибка!', u'''Значение задержки полимеризации 
должно быть больше 0!''')
            self.stopbtn.setDisabled(True)
            self.btn.setDisabled(False)
            self.exitbtn.setDisabled(False)
            reply
        
        elif (float(self.drain_1.text()) < -30.0 or float(self.drain_1.text()) > 30.0 or float(self.drain_2.text()) < -30.0 or float(self.drain_2.text()) > 30.0 or
float(self.drain_3.text()) < -30.0 or float(self.drain_3.text()) > 30.0 or float(self.drain_4.text()) < -30.0 or float(self.drain_4.text()) > 30.0):
            reply = QMessageBox.critical(self, u'Ошибка!', u'''Значение напряжения на Drain должно
быть в диапазоне [-30; 30]!''')
            self.stopbtn.setDisabled(True)
            self.btn.setDisabled(False)
            self.exitbtn.setDisabled(False)
            reply
        
        elif (float(self.gate_1.text()) < -2.5 or float(self.gate_1.text()) > 2.5 or float(self.gate_2.text()) < -2.5 or float(self.gate_2.text()) > 2.5 or
float(self.gate_3.text()) < -2.5 or float(self.gate_3.text()) > 2.5 or float(self.gate_4.text()) < -2.5 or float(self.gate_4.text()) > 2.5):
            reply = QMessageBox.critical(self, u'Ошибка!', u'''Значение напряжения на Gate должно
быть в диапазоне [-2,5; 2,5]!''')
            self.stopbtn.setDisabled(True)
            self.btn.setDisabled(False)
            self.exitbtn.setDisabled(False)
            reply
 
        else:
            
            self.myname = self.nameLine.text()
            self.experimentname = self.experimentnameLine.text()
            self.experimentnumber = self.experimentnumberLine.text()
            self.filename = self.filenameLine.text()
            self.savename = self.savenameLine.text()
            self.delay = float(self.delayLine.text())
            self.time = float(self.timeLine.text())
            
            try:
                
                dirn = os.path.dirname(self.filename)  
                if dirn == '':
                    dirn = os.getcwd()
                name = os.path.basename(self.filename)
                name = os.path.splitext(name)[0]
                with io.open(dirn + '/' + name + '.json', 'r') as outfile:
                    outfile.read()
                    
            except IOError:
                
                with open(dirn + '/' + name + '.json', 'w') as f:
                    f
                
            try:
                
                dirn = os.path.dirname(self.savename)  
                if dirn == '':
                    dirn = os.getcwd()
                save = os.path.basename(self.savename)
                save = os.path.splitext(save)[0]
                with io.open(dirn + '/' + save + '.json', 'r') as outfile:
                    outfile.read()
                    
            except IOError:
                
                with open(dirn + '/' + save + '.json', 'w') as f:
                    pass
                    
                with open(dirn + '/' + save + '.yaml', 'w') as f:
                    pass
                
            self.execute_event = True
            self.script_started() 
    
        
    def connect(self):
        
        self.instrument1 = Device()
        #self.instrument2 = Device()
        #self.instrument3 = Device()
        #self.instrument4 = Device()
        self.instrument5 = Device()
        self.instrument6 = Device()
        self.instrument7 = Device()
        
        self.instrument1.initialize_device(self.filename)
        #self.instrument2.initialize_device(self.filename)
        #self.instrument3.initialize_device(self.filename)
        #self.instrument4.initialize_device(self.filename)
        self.instrument5.initialize_device(self.filename)
        self.instrument6.initialize_device(self.filename)
        self.instrument7.initialize_device(self.filename)
        
        step_1 = self.instrument1.instrument_connect('Pump')
        self.setTextBrowserValue(step_1[0])
        if step_1[1] == True:
            1#raise Equipment_Exceptions('Error!') 
        #step_2 = self.instrument2.instrument_connect('Generator')
        #self.setTextBrowserValue(step_2[0])
        #if step_2[1] == True:
            #1#raise Equipment_Exceptions('Error!') 
        #step_3 = self.instrument3.instrument_connect('Oscilophone')
        #self.setTextBrowserValue(step_3[0])
        #if step_3[1] == True:
           # 1#raise Equipment_Exceptions('Error!') 
        #step_4 = self.instrument4.instrument_connect('Microscope')
        #self.setTextBrowserValue(step_4[0])
        #if step_4[1] == True:
           # 1#raise Equipment_Exceptions('Error!') 
        step_5 = self.instrument5.instrument_connect('Amplifier')
        self.setTextBrowserValue(step_5[0])
        if step_5[1] == True:
            1#raise Equipment_Exceptions('Error!') 
        step_6 = self.instrument6.instrument_connect('TiePie')
        self.setTextBrowserValue(step_6[0])
        if step_6[1] == True:
            1#raise Equipment_Exceptions('Error!')
        step_7 = self.instrument7.instrument_connect('Power Source')
        self.setTextBrowserValue(step_7[0])
        if step_7[1] == True:
            1#raise Equipment_Exceptions('Error!')
        
        
    def disconnect(self):
        
        try:
            answer = self.instrument1.instrument_disconnect()
            if answer != None:
                self.setTextBrowserValue(answer)
            #answer = self.instrument2.instrument_disconnect()
            #if answer != None:
            #    self.setTextBrowserValue(answer)
            #answer = self.instrument3.instrument_disconnect()
            #if answer != None:
            #    self.setTextBrowserValue(answer)
            #answer = self.instrument4.instrument_disconnect()
            #if answer != None:
            #    self.setTextBrowserValue(answer)
            answer = self.instrument5.instrument_disconnect()
            if answer != None:
                self.setTextBrowserValue(answer)
            answer = self.instrument6.instrument_disconnect()
            if answer != None:
                self.setTextBrowserValue(answer)
            answer = self.instrument7.instrument_disconnect()
            if answer != None:
                self.setTextBrowserValue(answer)
        except visa.InvalidSession:
            self.setTextBrowserValue(u'Устройства не активны! Выполните действие "ПОДКЛЮЧИТЬ"!')
        except AttributeError:
            self.setTextBrowserValue(u'Устройства не активны! Выполните действие "ПОДКЛЮЧИТЬ"!')
        
        
    def promivka(self):
        
        try:
            self.instrument1.pump('/1V200M1000O4M1000A3000M1000O5M1000A0R\r', 40)
            self.setTextBrowserValue(u'Раствор подан.')
        except visa.InvalidSession:
            self.setTextBrowserValue(u'Насос не активен! Выполните действие "ПОДКЛЮЧИТЬ"!')
        except AttributeError:
            self.setTextBrowserValue(u'Насос не активен! Выполните действие "ПОДКЛЮЧИТЬ"!')
        
        
    def produvka(self):
        
        try:
            self.instrument1.pump('/1V200M1000O3M1000A3000M1000O5M1000A0R\r', 40)
            self.setTextBrowserValue(u'Продувка проведена.')
        except visa.InvalidSession:
            self.setTextBrowserValue(u'Насос не активен! Выполните действие "ПОДКЛЮЧИТЬ"!')
        except AttributeError:
            self.setTextBrowserValue(u'Насос не активен! Выполните действие "ПОДКЛЮЧИТЬ"!')


    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()
            
        elif e.key() == Qt.Key_Return:
            self.saving()
            
            
    def to_amplify(self):
        
        try:
            self.setTextBrowserValue(self.instrument5.amplification(self.point.currentText().split()))
        except AttributeError:
            self.textBrowser.append(u'Блок ЦАП не подключен!')
            self.stop_thread()
            
            
    def set_power(self):
        
        try:
            self.setTextBrowserValue(self.instrument7.power_source(self.drain_1.currentText().split(), self.drain_2.currentText().split(),
                                                                  self.drain_3.currentText().split(), self.drain_4.currentText().split(),
                                                                  self.gate_1.currentText().split(), self.gate_2.currentText().split(),
                                                                  self.gate_3.currentText().split(), self.gate_4.currentText().split()))
        except AttributeError:
            self.textBrowser.append(u'Блок питания не подключен!')
            self.stop_thread()
        
    def setProgressValue(self, value):
        
        self.progress.setValue(value)
        
    
    def determined_delay(self):
        
        self.my_dialog = QDialog()
        self.my_dialog.setWindowTitle(u'Задержка')
        self.my_dialog.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.WindowMinimizeButtonHint|Qt.WindowMaximizeButtonHint)
        mydialog_vlayout = QVBoxLayout()
        mydialog_hlayout = QHBoxLayout()
        mydialog_h1layout = QHBoxLayout()
        mylabel = QLabel()
        mylabel.setText(u'Введите время задержки: ')
        mylabel.setFont(QFont('Decorative', 12, 60))
        self.myline = QLineEdit()
        self.myline.setFixedSize(70, 30)
        self.myline.setAlignment(Qt.AlignCenter)
        self.myprogress = QProgressBar(self)
        self.myprogress.resize(200, 70)
        self.myprogress.hide()
        self.mybtn = QPushButton(u'Продолжить', self)
        self.mybtn.setAutoDefault(True)
        self.mybtn.setStyleSheet("background-color: #7fc7ff")
        self.mybtn.setFont(QFont('Decorative', 12, 65))
        self.mybtn.setFixedSize(140, 40)
        self.mybtn.clicked.connect(self.determined_delay_execute)
        mydialog_vlayout.addLayout(mydialog_hlayout)
        mydialog_hlayout.addWidget(mylabel)
        mydialog_hlayout.addWidget(self.myline)
        mydialog_hlayout.addStretch(1)
        mydialog_vlayout.addWidget(self.myprogress)
        mydialog_vlayout.addLayout(mydialog_h1layout)
        mydialog_hlayout.addStretch(1)
        mydialog_h1layout.addWidget(self.mybtn)
        mydialog_hlayout.addStretch(1)
        self.my_dialog.setLayout(mydialog_vlayout)     
        self.my_dialog.exec_()
    
    
    def determined_delay_execute(self):

        self.myprogress.show()
        value = float(self.myline.text())
        if value <=0:
            reply = QMessageBox.critical(self, u'Ошибка!', u'Заполните пустые поля!')
            reply
        else:
            percent = 0
            self.mybtn.hide()          
            while percent < 100:
                time.sleep(1)
                percent += (1/(value*60))*100
                self.myprogress.setValue(percent)
            self.my_dialog.close()
        
        
    def delay_started(self, mode):
        
        if mode == 'delay':
            self.processname.setText(u'Задержка мобилизации.')
            self.processname.show()
            self.progress.show()
        
        if mode == 'time':
            self.processname.setText(u'Полимеризация.')
            self.processname.show()
            self.progress.show()
        
    def tie_pie(self):
        
        try:
            answer = self.instrument6.tiepie_write_csv(1e5, 5000, 16, 4, 3, self.savename)
        except AttributeError:
            answer = u'Подключите TiePie!'
        return(answer)

    
    def delay_ended(self, mode):
        
        if mode == 'delay':
            self.textBrowser.append('Мобилизация завершена!')
            self.progress.hide()
            self.processname.hide()
        
        elif mode == 'time':
            self.textBrowser.append(u'Полимеризация завершена!')
            self.progress.hide()
            self.processname.hide()
    
    
    def setTextBrowserValue(self, value):
        
        self.textBrowser.append(value)
    
    
    def setEnable(self):
        
        self.textBrowser.append(u'Обработка завершена.')
        self.btn.setDisabled(False)
        self.exitbtn.setDisabled(False)
        self.stopbtn.setDisabled(True)
        self.progress.hide()
        self.processname.hide()
       
        
    def stop_thread(self):
        
        self.stopbtn.setDisabled(True)
        self.btn.setDisabled(False)
        self.exitbtn.setDisabled(False)
        self.thread.terminate()


    def exit_form(self):
        
        self.close()
    
        
    def script_started(self):
        
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressValue)
        self.thread.delay_mode.connect(self.delay_started)
        self.thread.end_delay.connect(self.delay_ended)
        self.thread.set_power.connect(self.set_power)
        self.thread.text_browser_append.connect(self.setTextBrowserValue)
        self.thread.finished.connect(self.setEnable)
        self.thread.stop.connect(self.stop_thread)
        self.thread.connect.connect(self.connect)
        self.thread.disconnect.connect(self.disconnect)
        self.thread.promivka.connect(self.promivka)
        self.thread.produvka.connect(self.produvka)
        self.btn.setDisabled(True)
        self.stopbtn.setDisabled(False)
        self.thread.delay = self.delay 
        self.thread.time = self.time 
        self.thread.filename = self.filename
        self.thread.savename = self.savename
        self.thread.myname = self.myname
        self.thread.experimentname = self.experimentname
        self.thread.experimentnumber = self.experimentnumber
        
        if self.execute_event == True:
            
            self.btn.setDisabled(True)
            self.exitbtn.setDisabled(True)
            self.stopbtn.setDisabled(False)
            self.textBrowser.append(u'Обработка запущена')
            if self.combo.currentText().strip() == u'Подключение':
                self.thread.number = 1
                self.thread.start()
            elif self.combo.currentText().strip() == u'Отключение':
                self.thread.number = 2
                self.thread.start()
            elif self.combo.currentText().strip() == u'Промывка ячейки':
                self.thread.number = 3
                self.thread.start()
            elif self.combo.currentText().strip() == u'Продувка ячейки':
                self.thread.number = 4
                self.thread.start()
            elif self.combo.currentText().strip() == 'Выставление уровней БП':
                self.thread.number = 5
                self.thread.start()
            elif self.combo.currentText().strip() == '#1':
                self.thread.number = 6
            elif self.combo.currentText().strip() == u'Измерение уровня':
                #self.determined_delay()
                self.setTextBrowserValue(self.to_amplify())
                time.sleep(1)
                self.setTextBrowserValue(self.tie_pie())
                self.textBrowser.append(u'Обработка завершена!')
                self.stop_thread()
            
        else:
            self.textBrowser.append(u'Ошибка! Что-то пошло не так!')




# Класс для запуска скриптов в отдельных потоках
class MyThread(QThread):
    
    
    change_value = pyqtSignal(int)
    delay_mode = pyqtSignal(str)
    end_delay = pyqtSignal(str)
    text_browser_append = pyqtSignal(str)
    stop = pyqtSignal()
    connect = pyqtSignal()
    disconnect = pyqtSignal()
    promivka = pyqtSignal()
    produvka = pyqtSignal()
    set_power = pyqtSignal()
    number = 0
    time = 0
    delay = 0
    filename = ''
    savename = ''
    myname = ''
    experimentname = ''
    experimentnumber = ''
    
    
    def __init__(self, parent=None):
        
        QThread.__init__(self, parent)
   
    
    def run(self):
        
        if self.number == 1:
            self.connect.emit()
        
        elif self.number == 2:
            self.disconnect.emit()
        
        elif self.number == 3:
            self.promivka.emit()
            
        elif self.number == 4:
            self.produvka.emit()
        
        elif self.number == 5:
            self.set_power.emit()
            
        elif self.number == 6:
            
            #instrument1 = Device()
            #instrument2 = Device()
            instrument3 = Device()
            #instrument4 = Device()
        
            #instrument1.initialize_device(self.filename)
            #instrument2.initialize_device(self.filename)
            instrument3.initialize_device(self.filename)
            #instrument4.initialize_device(self.filename)
        
            #step_1 = instrument1.instrument_connect('Pump')
            #self.text_browser_append.emit(step_1[0])
            #if step_1[1] == True:
             #   self.stop.emit()
            #step_2 = instrument2.instrument_connect('Generator')
            #self.text_browser_append.emit(step_2[0])
            #if step_2[1] == True:
             #   self.stop.emit()
            step_3 = instrument3.instrument_connect('Oscilophone')
            self.text_browser_append.emit(step_3[0])
            if step_3[1] == True:
                self.stop.emit()
            #step_4 = instrument4.instrument_connect('Microscope')
            #self.text_browser_append.emit(step_4[0])
            
            #self.start_delay('delay')
        
            #self.text_browser_append.emit(u'Подача раствора.')
            #self.text_browser_append.emit(instrument1.pump("/1V300M1000O4M1000V150A2400M1000O5A0R\r", 25))
            #self.text_browser_append.emit(instrument2.generator_output('1', 'SIN', '2', '200', '1', '40'))
            #self.text_browser_append.emit(instrument2.generator_output('2', 'SQU', '2', '400', '0.5', '40'))
            self.text_browser_append.emit(instrument3.oscilophone_write(self.savename, self.myname, self.experimentname, self.experimentnumber, 10))
            #instrument2.generator_reset('1', 10)
            #instrument2.generator_reset('2', 0)
            #instrument4.microscope()
        
            #self.start_delay('time')
            
            #self.text_browser_append.emit(instrument1.instrument_disconnect())
            #self.text_browser_append.emit(instrument2.instrument_disconnect())
            self.text_browser_append.emit(instrument3.instrument_disconnect())

        
    def start_delay(self, mode):
        
        if mode == 'delay':
            
            self.delay_mode.emit('delay')
            percent = 0
            while percent < 100:
                time.sleep(1)
                percent += (1/(self.delay*60))*100
                self.change_value.emit(percent)
            self.end_delay.emit('delay')

            
        elif mode == 'time':
            
            self.delay_mode.emit('time')
            percent = 0
            while percent < 100:
                time.sleep(1)
                percent += (1/self.time)*100
                self.change_value.emit(percent)
            self.end_delay.emit('time')



# Класс для работы с устройствами через COM-порт и USB-порт
class Device(object):
    
    
    instr_idn = None
    
    
    def __init__(self):
        

        self.rm = visa.ResourceManager()
        self.instr = None
        
        super(Device, self).__init__()

    
    def initialize_device(self, filename):
        
            with io.open(filename, 'r', encoding = 'utf8') as fn:
                self.instr_data = json.load(fn)
            answer = u'Устройство инициализировано.'
            
            return answer
        
    
    
    
    def instrument_connect(self, instrument):   
        
        error_code = False
        answer = u'Устройство ' + instrument + u' не обнаружено!'
        
        if instrument == 'Microscope':
            
            output = subprocess.check_output('lsusb')
            if 'Anchor Chips, Inc.' in output:
                self.instr_idn = 'UCMOS09000KPB'
                answer = u'Устройство "UCMOS09000KPB" подключено!'
            else:
                answer = u'Устройство ' + '"' + instrument + '"' + u' не обнаружено!'
                error_code = True
                
        elif instrument == 'Amplifier':
            for i in range(len(self.rm.list_resources())):
                instr_name = self.rm.list_resources()[i].encode('ascii')
                try:
                    self.ser = serial.Serial(instr_name.replace('ASRL', '').replace('::INSTR', '').strip(), timeout=1)
                    time.sleep(0.05)
                    self.ser.write(b'A\x00\x00')
                    time.sleep(0.05)
                    self.ser.write(b'B\x00\x00')
                    echo = self.ser.read(2)
                    time.sleep(0.05)
                    if echo == 'Ok' or echo == 'Er' or echo == '3':
                        self.instr_idn = u'Блок ЦАП'
                        answer = u'Блок ЦАП подключен!'
                        break
                    else:
                        answer = u'Блок ЦАП не найден!'
                except serial.SerialException:
                    answer = u'Блок ЦАП не найден!'
        
        elif instrument == 'Power Source':
            for i in range(len(self.rm.list_resources())):
                instr_name = self.rm.list_resources()[i].encode('ascii')
                try:
                    self.power_source = serial.Serial(instr_name.replace('ASRL', '').replace('::INSTR', '').strip(), timeout=1)
                    time.sleep(0.05)
                    self.power_source.write('Name\r')
                    time.sleep(0.05)
                    echo = self.power_source.read(30)
                    time.sleep(0.05)
                    if echo == 'Power Source':
                        self.instr_idn = u'Блок питания'
                        answer = u'Блок питания подключен!'
                        break
                    else:
                        answer = u'Блок питания не найден!'
                except serial.SerialException:
                    answer = u'Блок питания не найден!'
        
        elif instrument == 'TiePie':
            libtiepie.device_list.update()
            self.scp = None
            
            for item in libtiepie.device_list:
                if item.can_open(libtiepie.DEVICETYPE_OSCILLOSCOPE):
                    self.scp = item.open_oscilloscope()
                    if self.scp.measure_modes & libtiepie.MM_STREAM:
                        self.instr_idn = 'TiePie'
                        answer = u'Устройство "TiePie" подключено!'
                        break
                    else:
                        self.scp = None
                        answer = u'Устройство "TiePie" не обнаружено!'
                        error_code = True
            
        else:
            for i in range(len(self.rm.list_resources())):
                instr_name = self.rm.list_resources()[i].encode('ascii')
                time.sleep(0.05)
                
                try: 
                    self.instr = self.rm.open_resource(instr_name)
                except Exception:
                    answer = u'Переподключите устройство!'
                    error_code = True
                    continue
                
                try:
                    self.instr.write('*CLS')
                    time.sleep(0.05)
                except visa.VisaIOError:
                    answer = u'Устройство не обнаружено!'
                    error_code = True
                except Exception:
                    answer = u'Устройство не обнаружено!'
                    error_code = True

                try:
                    self.instr.write(b'/1ZR\r')
                except Exception:
                    continue
                if instrument == 'Pump':
                    time.sleep(13)
                self.instr_idn = self.instr.query('*IDN?').strip().replace('/0@', 'AMFLSPone').replace('/0O', 'AMFLSPone')
                
                if self.instr_idn == self.instr_data[instrument]['IDN'].strip():
                    answer = u'Устройство ' + '"' + self.instr_idn + '"' + u' подключено!'
                    time.sleep(0.05)
                    break
                
                elif (i + 1) == len(self.rm.list_resources()) and self.instr_idn != self.instr_data[instrument]['IDN']:
                    answer = u'Устройство ' + '"' + instrument + '"' + u' не обнаружено!'
                    self.instr_idn = None
                    self.instr.close()
                    error_code = True
                
                elif self.instr_idn != self.instr_data[instrument]['IDN']:
                    self.instr.close()
                    continue
            
        return [answer, error_code]

    
    def instrument_disconnect(self):
        
        if self.instr_idn == None:
            answer = u'Устройство не подключалось!'
        elif self.instr_idn == 'TiePie':
            del self.scp
            answer = u'Устройство "TiePie" успешно отключено!'
        elif self.instr_idn == 'UCMOS09000KPB':
            answer = u'Устройство "UCMOS09000KPB" успешно отключено!'
        elif self.instr_idn == u'Блок ЦАП':
            self.ser.close()
            answer = u'Усилтель успешно отключен'
        else:
            self.instr.close()
            answer = u'Устройство ' + '"' + self.instr_idn + '"' + u' успешно отключено!'
        
        return answer


    def oscilophone_write(self, writefilename, myname, expname, expnumb, exptime):
        
        self.operation_id = 'oscil_write'
        
        try:
             idn = self.instr.query('*IDN?').strip()
        except visa.VisaIOError:
            raise Equipment_Exceptions('Device not found!')
            sys.exit()
        
        if idn != 'Rohde&Schwarz,HMO1002,032269937,05.886':
            self.instr.close()
            answer = u'Неправильное устройство!'
            sys.exit()
                
        dispdat_1 = []
        dispdat_2 = []
        exposed_time = 0
        dispdat_1_list = []
        #dispdat_2_list = []
        
        self.instr.write('CHAN1:DATA:POIN DMAX')
        time.sleep(0.05)
        self.instr.write('CHAN2:DATA:POIN DMAX')
        time.sleep(0.05)
        self.instr.write('ACQ:WRAT MWAV')
        time.sleep(0.05)
        self.instr.write('AUT')
        time.sleep(3)
        self.instr.write('AUT')
        time.sleep(3)
        self.instr.write('CHAN1:STAT ON')
        time.sleep(0.5)
        #self.instr.write('CHAN2:STAT ON')
        #time.sleep(0.05)
        start_time = time.time()
        while exptime > exposed_time:
            exposed_time = time.time() - start_time
            dispdat_1.append(self.instr.query('CHAN1:DATA?').split(','))
            #dispdat_2.append(self.instr.query('CHAN2:DATA?').split(','))
            continue
        for i in xrange(len(dispdat_1)):
            for j in range(len(dispdat_1[i])):
                dispdat_1[i][j] = round(float(dispdat_1[i][j]), 6)
                #dispdat_2[i][j] = round(float(dispdat_2[i][j]), 6)
                dispdat_1_list.append(dispdat_1[i][j])
                #dispdat_2_list.append(dispdat_2[i][j])
        fig, ax = plt.subplots()
        y = list(range(1, (len(dispdat_1_list)+1)))
        ax.plot(y, dispdat_1_list, color = 'red', label = u'Осциллограф')
        ax.set_xlabel(u'Напряжение')
        ax.set_ylabel(u'Ток')
        plt.grid(True)
        ax.legend()
        plt.show()
        #fig1, ax1 = plt.subplots()
        #y1 = list(range(1, (len(dispdat_2_list)+1)))
        #ax1.plot(y1, dispdat_2_list, color = 'red', label = u'Осциллограф')
        #ax1.set_xlabel(u'Напряжение')
        #ax1.set_ylabel(u'Ток')
        #plt.grid(True)
        #ax1.legend()
        #plt.show()
        
        dirn = os.path.dirname(writefilename)
        name = os.path.basename(writefilename)
        writefilename = os.path.splitext(name)[0]
        json_string = {'Research data': {
                                         'Reserach conducted by: ': myname,
                                         'Date:': datetime.datetime.today().strftime('%Y.%m.%d.%H.%M.%S'),
                                         'Test name': expname,
                                         'Test number: ': expnumb
                                                  },
                       'Experimental data': {
                                             'Channel 1 data: ': dispdat_1,
                                             'Channel 2 data: ': dispdat_2
                                                    },
                       }
        with io.open(dirn + '/' + writefilename + '.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(json_string,
                              indent=4, sort_keys=False,
                              separators=(',', ': '), ensure_ascii = True)
            outfile.write(unicode(str_))   
        
        to_yaml = {'Channel 1 data': dispdat_1, 'Channel 2 data': dispdat_2}
        with open(dirn + '/' + writefilename + '.yaml', 'w') as outfile:
            outfile.write('description: Секвенирование олига VB15. Обеднение нуклеотидов в 100 раз.\n' + 'sequenceLength: 177\n' + 
                          'bridge: "ACTGACTGACTGACTGACTGACTGA"\n' + 'aDelays:\n')
            yaml.dump(to_yaml, outfile, default_flow_style=False)
            
        answer = u'Измерения произведены!'
            
        return answer
    
    
    def generator_output(self, chan_num, wave_type, wave_amp, wave_freq, wave_phas, wave_set):
        
        self.operation_id = 'gen_output'
        
        try:
            self.instr.write('*CLS')
            time.sleep(0.05)
        except Exception:
            raise Equipment_Exceptions('Replug device!')
            answer = u'Неправильное устройство!'
            sys.exit()
        
        try:
             idn = self.instr.query('*IDN?').strip()
             time.sleep(0.05)
        except visa.VisaIOError:
            raise Equipment_Exceptions('Device not found!')
            sys.exit()
        
        if idn != 'TEKTRONIX,AFG1022,1828695,SCPI:99.0 FV:V1.2.4':
            self.instr.close()
            answer = u'Неправильное устройство!'
            raise Equipment_Exceptions('Wrong device!')
            sys.exit()
            
        self.instr.write('SOUR' + chan_num + ':FUNC:SHAP ' + wave_type)
        time.sleep(0.05)
        self.instr.write('SOUR' + chan_num + ':FREQ:FIX ' + wave_freq + 'Hz')
        time.sleep(0.05)
        self.instr.write('SOUR' + chan_num + ':VOLT:LEV:IMM:AMPL ' + wave_amp + 'Vpp')
        time.sleep(0.05)
        self.instr.write('SOUR' + chan_num + ':PHAS:ADJ ' + wave_phas)
        time.sleep(0.05)
        self.instr.write('SOUR' + chan_num + ':VOLT:LEV:IMM:OFFS ' + wave_set + 'mV')
        time.sleep(0.05)
        self.instr.write('OUTPUT' + chan_num + ':STAT ON')
        time.sleep(0.05)
        
        answer = u'Сигнал по каналу ' + chan_num + u' сгенерирован!'
    
        return answer
    
    
    def generator_reset(self, chan_num, timer):
        
        self.operation_id = 'gen_reset'
        
        time.sleep(timer)
        self.instr.write('OUTPUT' + chan_num + ':STAT OFF')
        time.sleep(0.05)
    
    
    def microscope(self):
        
        (exitcode, stdoutput) = commands.getstatusoutput('/usr/local/MIImageView/miimageview')
    
    
    def pump(self, command, timer):
        
        self.operation_id = 'pump'
        self.instr.write('b' + command)
        time.sleep(timer)
        answer = u'Раствор подан.'
        
        return answer
    
    def tiepie_write_csv(self, frequency, length, resol, range_value, times, writefilename):
        
        dirn = os.path.dirname(writefilename)
        name = os.path.basename(writefilename)
        writefilename = os.path.splitext(name)[0]
        
        libtiepie.device_list.update()
        self.scp = None
        
        for item in libtiepie.device_list:
            if item.can_open(libtiepie.DEVICETYPE_OSCILLOSCOPE):
                self.scp = item.open_oscilloscope()
                if self.scp.measure_modes & libtiepie.MM_STREAM:
                    break
                else:
                    self.scp = None
        
        if self.scp: 
            self.scp.measure_mode = libtiepie.MM_STREAM
            self.scp.sample_frequency = frequency
            self.scp.record_length = length
            self.scp.resolution = resol
                
            for ch in self.scp.channels:
                ch.enabled = True
                ch.range = range_value
                ch.coupling = libtiepie.CK_DCV
            
            self.scp.start()
            
            csv_file = open(dirn + '/' + writefilename + '.csv', 'w')
            
            try:
                csv_file.write('Sample')
                for i in range(len(self.scp.channels)):
                    csv_file.write(';Ch' + str(i + 1))
                csv_file.write(os.linesep)
                
                sample = 0
                for chunk in range(times):
                    while not (self.scp.is_data_ready or self.scp.is_data_overflow):
                        time.sleep(0.01)

                    if self.scp.is_data_overflow:
                        answer = 'Data overflow!'
                        break

                    data = self.scp.get_data()

                    for i in range(len(data[0])):
                        csv_file.write(str(sample + i))
                        for j in range(len(data)):
                            csv_file.write(';' + str(data[j][i]))
                        csv_file.write(os.linesep)

                    sample += len(data[0])

            finally:
                csv_file.close()

            self.scp.stop()
            answer = u'Измерение произведено!'
        
        else:
            answer = u'Цифровой регистратор не найден!'
            
        return answer
    
    def tiepie_write_dat(self, frequency, length, resol, range_value, times, writefilename):
        
        dirn = os.path.dirname(writefilename)
        name = os.path.basename(writefilename)
        writefilename = os.path.splitext(name)[0]
        
        libtiepie.device_list.update()
        self.scp = None
        
        json_string = {'description': 'VB15 olig sequencing. Nucleotide depletion by 100 times.',
                       'sequenceLength': '177', 
                       'bridge': '"ACTGACTGACTGACTGACTGACTGA"',
                       'aDelays': '',
                       'Binary file': dirn + '/' + writefilename + '.dat'
                       }
        with io.open(dirn + '/' + writefilename + '.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(json_string,
                              indent=4, sort_keys=False,
                              separators=(',', ': '), ensure_ascii = True)
            outfile.write(unicode(str_))   
        
        for item in libtiepie.device_list:
            if item.can_open(libtiepie.DEVICETYPE_OSCILLOSCOPE):
                self.scp = item.open_oscilloscope()
                if self.scp.measure_modes & libtiepie.MM_STREAM:
                    break
                else:
                    self.scp = None
        
        if self.scp: 
            self.scp.measure_mode = libtiepie.MM_STREAM
            self.scp.sample_frequency = frequency
            self.scp.record_length = length
            self.scp.resolution = resol
                
            for ch in self.scp.channels:
                ch.enabled = True
                ch.range = range_value
                ch.coupling = libtiepie.CK_DCV
            
            self.scp.start()
            
            with open(dirn + '/' + writefilename + '.dat', 'wb') as outfile:
                
                for chunk in range(times):
                    while not (self.scp.is_data_ready or self.scp.is_data_overflow):
                        time.sleep(0.01)

                    if self.scp.is_data_overflow:
                        answer = 'Data overflow!'
                        break
                    
                    data = self.scp.get_data()
                    #for i in xrange(len(data)):
                        #for j in xrange(len(data[i])):
                         #   data[i][j] = bitstring.BitArray(float=data[i][j], length=32)
                    pickle.dump(data, outfile)

            self.scp.stop()
            answer = u'Измерение произведено!'
        
        else:
            answer = u'Цифровой регистратор не найден!'
            
        return answer
        
    
    def amplification(self, level):
        
        answer = u'Усилитель не подключен!!!\t'
        if level == '     0 V':
            self.ser.write(b'A\x80\xe0')
            answer = u'Задан уровень 0 В!'
        elif level == '   0,5 V':
            self.ser.write(b'A\x87\x5e')
            answer = u'Задан уровень 0,5 В!'
        elif level == '  0,75 V':
            self.ser.write(b'A\x8a\x9d')
            answer = u'Задан уровень 0,75 В!'
        elif level == '   1,0 V':
            self.ser.write(b'A\x8d\xdc')
            answer = u'Задан уровень 1,0 В!'
        elif level == '  1,25 V':
            self.ser.write(b'A\x91\x1b')
            answer = u'Задан уровень 1,25 В!'
        elif level == '   1,5 V':
            self.ser.write(b'A\x95\x5a')
            answer = u'Задан уровень 1,5 В!'
        elif level == '  1,75 V':
            self.ser.write(b'A\x97\x99')
            answer = u'Задан уровень 1,75 В!'
        elif level == '   2,0 V':
            self.ser.write(b'A\x9a\xd8')
            answer = u'Задан уровень 2,0 В!'
            
        return answer
    
    
    def power_source(self, gate_1, gate_2, gate_3, gate_4, drain_1, drain_2, drain_3, drain_4):
        
        answer = []
        
        self.power_source.write('SD1V32699' + str(float((drain_1*1000)/60)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SD2V32701' + str(float((drain_2*1000)/60)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SD3V32768' + str(float((drain_3*1000)/60)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SD4V32768' + str(float((drain_4*1000)/60)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SG1V38769' + str(float(gate_1/457)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SG2V32851' + str(float(gate_2/457)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SG3V32804' + str(float(gate_3/457)) + '\r')
        answer.append(self.power_source.read(30))
        self.power_source.write('SG4V32784' + str(float(gate_4/457)) + '\r')
        answer.append(self.power_source.read(30))



# Запуск программы            
if __name__ == '__main__': 
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    data = DataInput()
    app.exec_()
    sys.exit(0)