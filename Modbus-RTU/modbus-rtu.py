import sys
from serial import Serial
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from main_ui import Modbus_UI
from modbus import ModbusCmd,char_to_int16
from crc import crc16

ONESECOND = 50

class Modbus_RTU(Modbus_UI):
	def __init__(self):
		super().__init__()
		self.initSys()		

	def initSys(self):
		self.ser = Serial()
		self._find_port()
		self.is_com_open = False
		self._close_ser()
		#-----------------------
		self.tmrSer = QTimer()
		self.tmrSer.setInterval(20)
		self.tmrSer.timeout.connect(self.timeout_event)
		self.tmrSer.start()
		self.read_time = 0
		self.write_time = 0
		self.writemore_time = 0
		#-----------------------
		self.combtn.clicked.connect(self.opencom)
		self.scanbtn.clicked.connect(self.scancom)
		self.write_btn.clicked.connect(self.write06h)
		self.read_btn.clicked.connect(self.read03h)
		self.wm_btn.clicked.connect(self.write10h)
	
	def opencom(self):
		if not self.is_com_open:
			self._open_ser()
		else:
			self._close_ser()
	def scancom(self):
		self._close_ser()	
		self._find_port()
	def receive_data(self, rx_buff):
		crc = crc16()
		if len(rx_buff) >= 7 and crc.calcrc(rx_buff):
			if rx_buff[1] == 0x03 and len(rx_buff) == rx_buff[2]+5:
				self.rectxt_r.setText(' '.join([('%02X' % i) for i in rx_buff]))
				value = char_to_int16(rx_buff[3], rx_buff[4])
				self.dishex.setText('十六进制显示：%4X' % value)
				self.disten.setText('十进制显示：%5d' % value)
				self.status_r.setText("读通讯状态： 读通讯正常")
				self.read_time = 0
			elif rx_buff[1] == 0x06 and len(rx_buff) == 8:
				self.rectxt_w.setText(' '.join([('%02X' % i) for i in rx_buff]))
				self.status_w.setText("写通讯状态： 写通讯正常")
				self.write_time = 0
			elif rx_buff[1] == 0x10 and len(rx_buff) == 8:
				self.rectxt_m.setText(' '.join([('%02X' % i) for i in rx_buff]))
				self.status_m.setText("写通讯状态： 写通讯正常")
				self.writemore_time = 0

	def timeout_event(self):
		if not self.is_com_open:
			return
		#----------------------
		try:
			num = self.ser.inWaiting()
		except:
			self._close_ser()
			QMessageBox.about(self,'提示','串口丢失，请检查端口')
			return

		if num > 0:
			bytes = self.ser.read(num)
			self.rx_buff.extend(bytes)
			self.receive_data(self.rx_buff)
		#----------------------
		if self.read_time > 0: 
			self.read_time -= 1
			if self.read_time == 0:
				self.status_r.setText("读通讯状态： 通讯超时，请检查通讯参数和地址设置")
		if self.write_time > 0: 
			self.write_time -= 1
			if self.write_time == 0:
				self.status_w.setText("写通讯状态： 通讯超时，请检查通讯参数和地址设置")
		if self.writemore_time > 0: 
			self.writemore_time -= 1
			if self.writemore_time == 0:
				self.status_m.setText("写通讯状态： 通讯超时，请检查通讯参数和地址设置")

	def read03h(self):
		address = self._get_address()
		if address == None: return
		regadd = self._get_regadd('read')
		if regadd == None: return
		value = self._get_regvalue('read')
		if value == None: return
		send = ModbusCmd().cmd03(address, regadd, value)
		self.rx_buff = []
		self.ser.write(send)
		self.sendtxt_r.setText(' '.join([('%02X' % i) for i in send]))
		self.status_r.setText("读通讯状态： 串口已经开启，可以进行通讯")
		self.read_time = ONESECOND

	def write06h(self):
		address = self._get_address()
		if address == None: return
		regadd = self._get_regadd('write')
		if regadd == None: return
		value = self._get_regvalue('write')
		if value == None: return

		send = ModbusCmd().cmd06(address, regadd, value)
		self.rx_buff = []
		self.ser.write(send)		
		self.sendtxt_w.setText(' '.join([('%02X' % i) for i in send]))
		self.status_w.setText("写通讯状态： 串口已经开启，可以进行通讯")
		self.write_time = ONESECOND

	def write10h(self):
		address = self._get_address()
		if address == None: return
		regadd = self._get_regadd('writemore')
		if regadd == None: return
		value = self._get_regvalue('writemore')
		if value == None: return
		value_list = self._get_valuelist()
		if value_list == None: return
		# print(value, len(value_list), value_list)
		if value != len(value_list):
			QMessageBox.about(self,'提示','发送的数据长度有错误！\n---放弃本次操作---')
			return
		send = ModbusCmd().cmd10(address, regadd, value, value_list)
		self.rx_buff = []
		self.ser.write(send)		
		self.sendtxt_m.setText(' '.join([('%02X' % i) for i in send]))
		self.status_m.setText("写通讯状态： 串口已经开启，可以进行通讯")
		self.writemore_time = ONESECOND	
	#----------------------------------------------------------------
	#----------------------------------------------------------------	
	def _find_port(self):
		port_list = list(comports())
		self.combox.clear()
		self.combox.addItems([port[0] for port in port_list])
	def _open_ser(self):
		try:
			self.ser.port = self.combox.currentText()
			self.ser.baudrate = self.baudbox.currentText()
			self.ser.bytesize = int(self.bitbox.currentText())
			self.ser.parity = self.crcbox.currentText()[0]
			self.ser.stopbits = int(self.stopbox.currentText())
			self.ser.open()			
		except:
			self._close_ser()
			QMessageBox.about(self,'提示','打开串口出错！')
			return
		self.is_com_open = True		
		self._dis_ser_par(True)
	#获取协议地址
	def _get_address(self):
		try: 
			add = int(self.devaddtxt.text())
			if add > 255:
				QMessageBox.about(self,'提示','设备地址超出范围！\n---放弃本次操作---')
				return None
			return add
		except:
			return 0	
	#获取控件的数据
	def _get_regadd(self, col):
		if col == 'read': handle = self.regadd_r
		elif col == 'write': handle = self.regadd_w
		elif col == 'writemore': handle = self.regadd_m
		else: return None
		try:
			add = int(handle.text())
			if add > 65535:
				QMessageBox.about(self,'提示','寄存器地址设置有误！\n---放弃本次操作---')
				return None
			return add
		except:
			QMessageBox.about(self,'提示','寄存器地址设置有误！\n---放弃本次操作---')
			return None	
	#获取写入的值
	def _get_regvalue(self, col):
		if col == 'read': handle = self.regval_r
		elif col == 'write': handle = self.regval_w
		elif col == 'writemore': handle = self.regval_m
		else: return None
		try:
			value = int(handle.text())
			if value > (65535 if col=='write' else 100):
				QMessageBox.about(self,'提示','设定值设置有误！\n-放弃本次操作-')
				return None
			return value
		except:
			QMessageBox.about(self,'提示','设定值设置有误！\n-放弃本次操作-')
			return None	
	#获取10指令的数据
	def _get_valuelist(self):
		indata = self.inputtxt_m.text()
		ls = indata.split('/')
		if ls[0] == '': 
			del ls[0]
		if len(ls) > 0 and ls[-1] == '':
			del ls[-1]

		try:
			data = [int(a) for a in ls]
			if data == []:
				QMessageBox.about(self,'提示','发送的数据有错误！\n--放弃本次操作--')
				return None
			return data
		except:
			QMessageBox.about(self,'提示','发送的数据有错误！\n--放弃本次操作--')
			return None

	def _close_ser(self):
		self.ser.close()
		self.is_com_open = False
		self._dis_ser_par(False)
	#
	def _dis_ser_par(self, val):
		if val:
			#三个btn使能操作
			self.write_btn.setEnabled(True)
			self.read_btn.setEnabled(True)
			self.wm_btn.setEnabled(True)
			#三个通知
			self.status_w.setText("写通讯状态： 串口已经开启，可以进行通讯")
			self.status_r.setText("读通讯状态： 串口已经开启，可以进行通讯")
			self.status_m.setText("写通讯状态： 串口已经开启，可以进行通讯")
			#other
			self.combtn.setText("关闭串口")
			news = ' %s.%s.%s.%d.%d' % (self.ser.port,self.ser.baudrate,self.ser.parity,
								   	   self.ser.bytesize,self.ser.stopbits)			
		else:
			#三个btn使能操作
			self.write_btn.setEnabled(False)
			self.read_btn.setEnabled(False)
			self.wm_btn.setEnabled(False)
			#三个通知
			self.status_w.setText("写通讯状态： 串口未开启，不能进行通讯")
			self.status_r.setText("读通讯状态： 串口未开启，不能进行通讯")
			self.status_m.setText("写通讯状态： 串口未开启，不能进行通讯")
			#other
			self.combtn.setText("打开串口")
			news = "  串口关闭状态"
		self.comtip.setText(news)
		self.set_compic(val)
			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = Modbus_RTU()
	sys.exit(app.exec_())

