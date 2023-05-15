#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:33:38 2018

@author: gamma-dna
"""
# Библиотека для работы с измерительным стендом
# При написании скриптов желательно подключать первым насос
# Автор Д.К. Товмаченко

import json, sys, io, datetime, visa, os, time, commands, subprocess, serial, yaml
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QGridLayout, QHBoxLayout, QDesktopWidget, QMainWindow, QFrame, QProgressBar,
                             QVBoxLayout, QLabel, QAction, QFileDialog, QMessageBox, QApplication, QTextBrowser, QComboBox, QDialog)
from PyQt5.QtGui import QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QSize, Qt, QCoreApplication, QThread, pyqtSignal



class Equipment_Exceptions(Exception):
    
    pass 



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
        sImage = oImage.scaled(QSize(900, 485))
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
        
        self.experimentnameLabel = QLabel(self)
        self.experimentnameLabel.setText(u'Наименование эксперимента: ')
        self.experimentnameLabel.setFont(QFont('Decorative', 12, 60))
        self.experimentnameLine = QLineEdit(self)
       
        self.experimentnumberLabel = QLabel(self)
        self.experimentnumberLabel.setText(u'№ эксперимента: ')
        self.experimentnumberLabel.setFont(QFont('Decorative', 12, 60))
        self.experimentnumberLine = QLineEdit(self)

        self.filenameLabel = QLabel(self)
        self.filenameLabel.setText(u'''Выберите файл с данными
об устройствах: ''')
        self.filenameLabel.setFont(QFont('Decorative', 12, 60))
        self.filenameLine = QLineEdit(self)
        self.filenameLine.setText('/home/gamma-dna/.config/spyder/firstprob.json')
        
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
        self.delayLine.setFixedSize(60, 30)
        
        self.timeLabel = QLabel(self)
        self.timeLabel.setText(u'''Введите время полимеризации
(в секундах): ''')
        self.timeLabel.setFont(QFont('Decorative', 12, 60))
        self.timeLine = QLineEdit(self)
        self.timeLine.setFixedSize(60, 30)
        
        self.textBrowser = QTextBrowser(self)
        
        self.textLabel = QLabel(self)
        self.textLabel.setText(u'Ход эксперимента: ')
        self.textLabel.setFont(QFont('Decorative', 12, 60))
        
        self.hline = QFrame()
        self.hline.setFrameShape(QFrame.HLine)
        self.hline.setFrameShadow(QFrame.Sunken)
        
        self.comboLabel = QLabel(self)
        self.comboLabel.setText(u'Выберите последовательность: ')
        self.comboLabel.setFont(QFont('Decorative', 12, 60))
        self.combo = QComboBox(self)
        self.combo.addItems([' #1', ' #2'])
        self.combo.setFont(QFont('Decorative', 12, 60))
        self.combo.setFixedSize(60, 30)
        
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
        
        exitbtn = QPushButton(u'Выход', self)
        exitbtn.setAutoDefault(True)
        exitbtn.setStyleSheet("background-color: #7fc7ff")
        exitbtn.setFont(QFont('Decorative', 12, 65))
        exitbtn.clicked.connect(self.exit_form)
        
        self.stopbtn = QPushButton(u'Стоп', self)
        self.stopbtn.setAutoDefault(True)
        self.stopbtn.setStyleSheet("background-color: #7fc7ff")
        self.stopbtn.setFont(QFont('Decorative', 12, 65))
        self.stopbtn.clicked.connect(self.stop_thread)
        self.stopbtn.setDisabled(True)

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
        hbox3.addWidget(exitbtn)
        hbox3.addStretch(1)
        hbox3.addWidget(self.questbtn)
        
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
        grid2.addWidget(self.comboLabel, 2, 0)
        grid2.addWidget(self.combo, 2, 1)
        
        mainwindow.addLayout(mainwindow_top)
        mainwindow_top.addLayout(mainwindow_left)
        mainwindow_top.addLayout(mainwindow_right)
        mainwindow.addLayout(mainwindow_down)
        
        mainwindow_left.addLayout(hbox1) 
        mainwindow_left.addLayout(grid1)
        mainwindow_left.addWidget(self.empty)
        mainwindow_left.addLayout(hbox2)
        mainwindow_left.addLayout(grid2)
        
        mainwindow_right.addWidget(self.textLabel)
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
        self.setFixedSize(900, 485)
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
        
        
    def showHelp(self):
        
        my_dialog = QDialog()
        my_dialog.setFixedSize(510, 190)
        my_dialog.setWindowTitle(u'Справка')
        helptext = QLabel(u'''
 Данная программа служит для управления проведением эксперимента.
 Кнопка "ЗАПУСК" инициирует скрипт, информация о протекнии
 которого будет отображаться в окне "Ход эксперимента". Кнопка
 "СТОП" инициализирует остановку скрипта, однако её использование
 нежелательно ввиду того, что прерывание скрипта может повлечь
 неправильную работу стенда в дальнейшем, использовать её стоит
 только в случае явной необходимости. После её использования 
 желательно перезапустить экспериментальный стенд. Кнопка "ВЫХОД"
 завершает приложение. Кроме того, следует внимательно выбирать 
 файл с данными об устройствах. 
            ''',my_dialog)
        helptext.setFont(QFont('Decorative', 10))
        my_dialog.exec_() 
        
        
    def saveDialog(self):
        
        put = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Save file', put)[0]
        self.savenameLine.setText(fname)
    
    
    def saving(self):
        
        
        if (len(self.nameLine.text()) == 0 or len(self.experimentnameLine.text()) == 0 or len(self.experimentnumberLine.text()) == 0 or len(self.filenameLine.text()) == 0 or
len(self.savenameLine.text()) == 0 or len(self.delayLine.text()) == 0 or len(self.timeLine.text()) == 0):
            reply = QMessageBox.critical(self, 'Message', u'Заполните пустые поля!!!')
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
    
        
    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()
            
        elif e.key() == Qt.Key_Return:
            self.saving()  
            
            
    def setProgressValue(self, value):
        
        self.progress.setValue(value)
        
        
    def delay_started(self, mode):
        
        if mode == 'delay':
            self.processname.setText(u'Задержка мобилизации.')
            self.processname.show()
            self.progress.show()
        
        if mode == 'time':
            self.processname.setText(u'Полимеризация.')
            self.processname.show()
            self.progress.show()
        
        
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
        self.stopbtn.setDisabled(True)
        self.progress.hide()
        self.processname.hide()
       
        
    def stop_thread(self):
        
        self.stopbtn.setDisabled(False)
        self.thread.terminate()
        self.thread.quit()


    def exit_form(self):
        
        self.close()
    
        
    def script_started(self):
        
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressValue)
        self.thread.delay_mode.connect(self.delay_started)
        self.thread.end_delay.connect(self.delay_ended)
        self.thread.text_browser_append.connect(self.setTextBrowserValue)
        self.thread.finished.connect(self.setEnable)
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
            self.textBrowser.setText(u'Обработка запущена.')
            
            if self.combo.currentText().strip() == '#1':
                self.thread.start()
                
            elif self.combo.currentText().strip() == '#2':
                self.textBrowser.append(' #2')
                self.textBrowser.append(u'Обработка завершена.')
                self.btn.setDisabled(False)
                
        else:
            self.textBrowser.append(u'Ошибка! Что-то пошло не так!')




class MyThread(QThread):
    
    
    change_value = pyqtSignal(int)
    delay_mode = pyqtSignal(str)
    end_delay = pyqtSignal(str)
    text_browser_append = pyqtSignal(str)
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
        
        self.start_delay('delay')
        
        #instrument1 = Device()
        #instrument2 = Device()
        instrument3 = Device()
        #instrument4 = Device()

        #instrument1.initialize_device(self.filename)
        #instrument2.initialize_device(self.filename)
        instrument3.initialize_device(self.filename)
        #instrument4.initialize_device(self.filename)
        
        #self.text_browser_append.emit(instrument1.instrument_connect('Pump'))
        #self.text_browser_append.emit(instrument2.instrument_connect('Generator'))
        self.text_browser_append.emit(instrument3.instrument_connect('Oscilophone'))
        #self.text_browser_append.emit(instrument4.instrument_connect('Microscope'))
        
        #self.text_browser_append.emit(instrument1.pump("/1V300M1000O5M1000A3000M1000A0R\r", 25))
        #self.text_browser_append.emit(instrument2.generator_output('1', 'SIN', '2', '200', '1', '40'))
        #self.text_browser_append.emit(instrument2.generator_output('2', 'SQU', '2', '400', '0.5', '40'))
        #self.text_browser_append.emit(instrument2.generator_reset('1', 12))
        #self.text_browser_append.emit(instrument2.generator_reset('2', 0))
        self.text_browser_append.emit(instrument3.oscilophone_write(data.savename, data.myname, data.expname, data.expnumb, 10))
        #self.text_browser_append.emit(instrument4.micro())
        
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



class Device(object):
    
    
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
        
        if len(self.rm.list_resources()) == 0:
            raise Equipment_Exceptions('''Can't find any devices, please check
                                       is there any devices connected!''')
            answer = u'Не удаётся найти устройства, пожалуйста проверьте, подключены ли устройства!'
            sys.exit()
        
        elif instrument == 'Microscope':
            output = subprocess.check_output('lsusb')
            if 'Bus 001 Device 022: ID 0547:6901 Anchor Chips, Inc.' in output:
                self.instr_idn = 'UCMOS09000KPB'
                answer = u'Устройство UCMOS09000KPB подключено!'
            
        else:
            for i in range(len(self.rm.list_resources())):
                instr_name = self.rm.list_resources()[i].encode('ascii')
                self.instr = self.rm.open_resource(instr_name)
                
                try:
                    self.instr.write('*CLS')
                    time.sleep(0.05)
                except visa.VisaIOError:
                    raise Equipment_Exceptions('Device not found!')
                    answer = u'Устройство не обнаружено!'
                    sys.exit()
                except Exception:
                    raise Equipment_Exceptions('Replug device!')
                    answer = u'Переподключите устройство!'
                    sys.exit()
                
                self.instr.write('/1ZR\r')
                if instrument == 'Pump':
                    time.sleep(18)
                self.instr_idn = self.instr.query('*IDN?').strip().replace('/0@', 'AMFLSPone').replace('/0O', 'AMFLSPone')
                time.sleep(0.05)
                
                if self.instr_idn == self.instr_data[instrument]['IDN'].strip():
                    answer = u'Устройство ' + '"' + self.instr_idn + '"' + u' подключено!'
                    break
                
                elif (i + 1) == len(self.rm.list_resources()) and self.instr_idn != self.instr_data[instrument]['IDN']:
                    self.instr.close()
                    raise Equipment_Exceptions('Device ' + '"' + instrument + '"' + ' not found!')
                    sys.exit()
                
                elif self.instr_idn != self.instr_data[instrument]['IDN']:
                    self.instr.close()
                    continue 
            
            return answer

    
    def instrument_disconnect(self):
        
        #self.ser.close()
        self.instr.close()
        answer = u'Устройство ' + '"' + self.instr_idn + '"' + u' отключено!'
        
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
            raise Equipment_Exceptions('Wrong device!')
            answer = u'Неправильное устройство!'
            sys.exit()
                
        dispdat_1 = []
        dispdat_2 = []
        exposed_time = 0
        dispdat_1_list = []
        dispdat_2_list = []
        
        self.instr.write('CHAN1:DATA:POIN DMAX')
        time.sleep(0.05)
        self.instr.write('CHAN2:DATA:POIN DMAX')
        time.sleep(0.05)
        self.instr.write('ACQ:WRAT MWAV')
        time.sleep(0.05)
        self.instr.write('AUT')
        time.sleep(2)
        self.instr.write('CHAN1:STAT ON')
        time.sleep(0.05)
        self.instr.write('CHAN2:STAT ON')
        time.sleep(0.05)
        start_time = time.time()
        while exptime > exposed_time:
            exposed_time = time.time() - start_time
            dispdat_1.append(self.instr.query('CHAN1:DATA?').split(','))
            dispdat_2.append(self.instr.query('CHAN2:DATA?').split(','))
            continue
        for index, value in enumerate(dispdat_1):
            for indexj, valuej in enumerate(dispdat_1[index]):
                dispdat_1[index][indexj] = round(float(valuej), 6)
                dispdat_2[index][indexj] = round(float(dispdat_2[index][indexj]), 6)
                dispdat_1_list.append(valuej)
                dispdat_2_list.append(valuej)
        fig, ax = plt.subplots()
        y = list(range(1, (len(dispdat_1_list)+1)))
        ax.plot(y, dispdat_1_list, color = 'red', label = u'Осциллограф')
        ax.set_xlabel(u'Напряжение')
        ax.set_ylabel(u'Ток')
        plt.grid(True)
        ax.legend()
        plt.show()
        fig1, ax1 = plt.subplots()
        y1 = list(range(1, (len(dispdat_2_list)+1)))
        ax1.plot(y1, dispdat_2_list, color = 'red', label = u'Осциллограф')
        ax1.set_xlabel(u'Напряжение')
        ax1.set_ylabel(u'Ток')
        plt.grid(True)
        ax1.legend()
        plt.show()
        
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
        
        to_yaml = {'Channel 1 data': dispdat1, 'Channel 2 data': dispdat2}
        with open(dirn + '/' + writefilename + '.yaml', 'w') as outfile:
            outfile.write('description: Секвенирование олига VB15. Обеднение нуклеотидов в 100 раз.\n' + 'sequenceLength: 177\n' + 
                          'bridge: "ACTGACTGACTGACTGACTGACTGA"\n' + 'aDelays:\n')
            yaml.dump(to_yaml, outfile, default_flow_style=False)
            
        return answer

    
    def oscilophone_fft(self):
        
        self.operation_id = 'oscil_fft'
        
        return
    
    
    def oscilophone_output(self):
        
        self.operation_id = 'oscil_output'
        
        return
    
    
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
        
        return u'Идёт подача раствора.'
    
    
    def dac_level(self, level):
        
        self.ser = serial.Serial(self.instr_idn, timeout=1)
        self.ser.write(level)
        proverka = self.ser.read(100)
        if proverka == 'Error':
            answer = u'Введена неправильная команда!!!'
        elif proverka == 'Ok':
            self.ser.write('0010')
            answer = u'Уровень задан'
            
        return answer
            
            
            
if __name__ == '__main__': 
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    data = DataInput()
    app.exec_()