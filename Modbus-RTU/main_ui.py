import sys
from PyQt5.QtWidgets import (QWidget,QApplication,QGroupBox,QLabel,QComboBox,QPushButton,QLineEdit, QTextEdit)
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt
from aboutsoft import About_Soft
from py2png import get_sys_png, del_sys_png

sizeA = [610, 370]
sizeB = [610, 520]
txt = '''<p>本Modbus软件依旧采用RTU通讯模式</p>	
<p>为了向经典致敬，特别制作这一复古版本。</p>
<p>Modbus调试精灵v5版，谢谢使用！</p>
'''

class Modbus_UI(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.aboutMe = About_Soft()

	def initUI(self):
		self.setFixedSize(sizeA[0], sizeA[1])
		self.setWindowTitle("Modbus调试精灵 V5 (向经典致敬)   淡泊明志，宁静致远")	
		self.setWindowIcon(QIcon(get_sys_png("title")))
		del_sys_png("title")
		self.initGroup()
		self.show()	

	def initGroup(self):
		gc = QGroupBox('通讯参数设置', self)
		gc.setGeometry(10, 5, 255, 170)
		gp = QGroupBox('Modbus协议参数设置', self)
		gp.setGeometry(10, 185, 255, 50)
		gw = QGroupBox('写寄存器区', self)
		gw.setGeometry(270, 5, 330, 150)
		gr = QGroupBox('读寄存器区', self)
		gr.setGeometry(270, 160, 330, 200)
		#gc-------------------------------
		comlb = QLabel("串口号：", gc)
		comlb.move(15, 30)
		crclb = QLabel("校验位：", gc)
		crclb.move(15, 65)
		stoplb = QLabel("停止位：", gc)
		stoplb.move(15, 100)
		self.combox = QComboBox(gc)
		self.combox.setGeometry(65, 25, 60, 21)		
		self.crcbox = QComboBox(gc)
		self.crcbox.setGeometry(65, 60, 60, 21)
		crclist = ['NONE','ODD','EVEN']
		self.crcbox.addItems(crclist)
		self.stopbox = QComboBox(gc)
		self.stopbox.setGeometry(65, 95, 60, 21)
		stoplist = ['1','2']
		self.stopbox.addItems(stoplist)
		#---
		baudlb = QLabel("波特率：", gc)
		baudlb.move(135, 30)
		bitlb = QLabel("数据位：", gc)
		bitlb.move(135, 65)
		self.baudbox = QComboBox(gc)
		self.baudbox.setGeometry(185, 25, 61, 21)
		baudlist = ['300','600','1200','2400','4800','9600','19200','38400','43000','56000','57600','115200']
		self.baudbox.addItems(baudlist)	
		self.baudbox.setCurrentIndex(5)
		self.bitbox = QComboBox(gc)
		self.bitbox.setGeometry(185, 60, 61, 21)
		bitlist = ['8','7','6']
		self.bitbox.addItems(bitlist)	
		self.comtip = QLabel("  串口关闭状态", gc)
		# self.comtip = QLabel("Com15.115200.N.8.1", gc)
		self.comtip.setGeometry(135, 100, 110, 12)
		#------------------------------------
		self.scanbtn = QPushButton("扫描", gc)
		self.scanbtn.setGeometry(20, 130, 41, 23)
		self.compic = QLabel("", gc) 
		self.compic.setGeometry(85, 125, 40, 35)
		self.set_compic(False)
		self.combtn = QPushButton("打开串口", gc)
		self.combtn.move(150, 130)

		#gp-------------------------------
		devaddlb = QLabel("设备地址：", gp)
		devaddlb.move(15, 25)
		self.devaddtxt = QLineEdit('1', gp)		
		self.devaddtxt.setGeometry(75, 22, 60, 20)
		self.devaddtxt.setAlignment(Qt.AlignHCenter)

		#写多寄存器部分	-----------------------------	
		note = QLabel(txt, self)
		note.setGeometry(40, 240, 250, 100)
		morebtn = QPushButton("更多功能", self)
		morebtn.move(20, 335)
		morebtn.setEnabled(False)
		self.writemorebtn = QPushButton("写多寄存器", self)
		self.writemorebtn.move(100, 335)
		self.writemorebtn.clicked.connect(self.wrtemore)
		self.aboutbtn = QPushButton("关于软件", self)
		self.aboutbtn.move(180, 335)
		self.aboutbtn.clicked.connect(self.about)
		#gw------------------------------------------
		regaddlb = QLabel("寄存器地址：", gw)
		regaddlb.move(15, 25)
		self.regadd_w = QLineEdit('', gw)
		self.regadd_w.setGeometry(85, 22, 50, 20)
		self.regadd_w.setAlignment(Qt.AlignHCenter)
		regvallb = QLabel("数值：", gw)
		regvallb.move(150, 25)
		self.regval_w = QLineEdit('', gw)
		self.regval_w.setGeometry(185, 22, 50, 20)
		self.regval_w.setAlignment(Qt.AlignHCenter)
		self.write_btn = QPushButton("写入", gw)
		self.write_btn.move(245, 20)
		#发送
		sendlb = QLabel("发送：", gw)
		sendlb.move(15, 55)
		self.sendtxt_w = QLineEdit('', gw)
		self.sendtxt_w.setGeometry(50, 52, 260, 20)
		reclb = QLabel("接收：", gw)
		reclb.move(15, 85)
		self.rectxt_w = QTextEdit('', gw)
		self.rectxt_w.setGeometry(50, 75, 260, 46)
		self.status_w = QLabel("写通讯状态： 串口未开启，不能进行通讯", gw)
		self.status_w.setGeometry(15, 130, 300, 12)

		#gr------------------------------------------
		regaddlb = QLabel("寄存器地址：", gr)
		regaddlb.move(15, 25)
		self.regadd_r = QLineEdit('', gr)
		self.regadd_r.setGeometry(85, 22, 50, 20)
		self.regadd_r.setAlignment(Qt.AlignHCenter)
		regvallb = QLabel("数值：", gr)
		regvallb.move(150, 25)
		self.regval_r = QLineEdit('', gr)
		self.regval_r.setGeometry(185, 22, 50, 20)
		self.regval_r.setAlignment(Qt.AlignHCenter)
		self.read_btn = QPushButton("读出", gr)
		self.read_btn.move(245, 20)
		#dis
		self.dishex = QLabel("十六进制显示：十六进制数值", gr)
		self.dishex.move(15,55)
		self.disten = QLabel("十进制显示：十进制数值", gr)
		self.disten.move(180,55)
		#发送
		sendlb = QLabel("发送：", gr)
		sendlb.move(15, 85)
		self.sendtxt_r = QLineEdit('', gr)
		self.sendtxt_r.setGeometry(50, 82, 260, 20)
		reclb = QLabel("接收：", gr)
		reclb.move(15, 115)
		self.rectxt_r = QTextEdit('', gr)
		self.rectxt_r.setGeometry(50, 105, 260, 70)
		self.status_r = QLabel("读通讯状态： 串口未开启，不能进行通讯", gr)
		self.status_r.setGeometry(15, 180, 300, 12)
		#新增加的写多个寄存器
		self.initWriteMore()

	def wrtemore(self):
		if self.writemorebtn.text() == '写多寄存器':
			self.setFixedSize(sizeB[0], sizeB[1])
			self.writemorebtn.setText('隐藏')
		else:
			self.setFixedSize(sizeA[0], sizeA[1])
			self.writemorebtn.setText('写多寄存器')
	def about(self):
		self.aboutMe.show()

	def initWriteMore(self):
		gm = QGroupBox('写多寄存器区', self)
		gm.setGeometry(10, 370, 590, 145)
		regaddlb = QLabel("寄存器地址：", gm)
		regaddlb.move(15, 25)
		self.regadd_m = QLineEdit('', gm)
		self.regadd_m.setGeometry(85, 22, 50, 20)
		self.regadd_m.setAlignment(Qt.AlignHCenter)
		regvallb = QLabel("数值：", gm)
		regvallb.move(150, 25)
		self.regval_m = QLineEdit('', gm)
		self.regval_m.setGeometry(185, 22, 50, 20)
		self.regval_m.setAlignment(Qt.AlignHCenter)
		self.wm_btn = QPushButton("写入", gm)
		self.wm_btn.move(245, 20)
		tiplb = QLabel("写入数据格式示范：1023/1024/1019/23/1982/", gm)
		tiplb.move(330, 25)
		#---
		lb = QLabel("  写入数据：", gm)
		lb.move(15, 50)
		lb = QLabel("  发送数据：", gm)
		lb.move(15, 75)
		lb = QLabel("  接收数据：", gm)
		lb.move(15, 100)
		self.status_m = QLabel("写通讯状态： 串口未开启，不能进行通讯", gm)
		self.status_m.setGeometry(15, 125, 300, 12)
		self.inputtxt_m = QLineEdit('', gm)
		self.inputtxt_m.setGeometry(85, 50, 490, 20)
		self.sendtxt_m = QLineEdit('', gm)
		self.sendtxt_m.setGeometry(85, 75, 490, 20)
		self.rectxt_m = QLineEdit('', gm)
		self.rectxt_m.setGeometry(85, 100, 490, 20)

	def set_compic(self, val):
		if val:
			img = QPixmap(get_sys_png("green"))
			del_sys_png("green")
		else:
			img = QPixmap(get_sys_png("red"))
			del_sys_png("red")
		self.compic.setPixmap(img)


if __name__ == '__main__':	
	app = QApplication(sys.argv)
	m = Modbus_UI()		
	sys.exit(app.exec_())

