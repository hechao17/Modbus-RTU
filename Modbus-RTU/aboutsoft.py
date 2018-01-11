import sys
from PyQt5.QtWidgets import (QWidget,QApplication,QLabel,QPushButton,QTextBrowser)
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt
from py2png import get_sys_png, del_sys_png

size = [400, 300]
notes = '''

	最新版本请联系： he-128@163.com
	
   本软件是用Python3.4和PyQt5制作。
   本人在调试modbus过程中经常使用<<经典的modbus调试精灵>>，但是
   老版本有几个设置的地方需要切换用8进制，16进制，10进制的方式，
   颇不方便，而更新的网站已经关闭。

   为了向经典致敬！ 特别制作复古版的通讯软件。谢谢大家帮忙测试

   联系方式： he-128@163.com
   Q     Q ： 357407542

   心里有阳光，哪里都是晴天！'''

class About_Soft(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setFixedSize(size[0], size[1])
		self.setWindowTitle("关于Modbus调试精灵V5  2017.12.26")	
		self.setWindowIcon(QIcon(get_sys_png('title')))
		del_sys_png('title')
		self.setWindowModality(Qt.ApplicationModal)	
		self.setWindowFlags(self.windowFlags()& ~Qt.WindowMaximizeButtonHint& ~Qt.WindowMinimizeButtonHint);
		self.initGroup()		

	def initGroup(self):
		self.txt = QTextBrowser(self)
		self.txt.resize(size[0], size[1])	
		self.txt.setStyleSheet("background-color:rgb(0,0,0,0);")
		#----
		quitbtn = QPushButton('确定',self)
		quitbtn.move(size[0]-85, size[1]-33)
		quitbtn.clicked.connect(self.quit)
		#--------------------------------
		self.compic = QLabel("", self) 
		self.compic.setGeometry(40, 20, 40, 35)
		img = QPixmap(get_sys_png("green"))
		del_sys_png('green')		
		self.compic.setPixmap(img)		
		#----
		self.wechat = QLabel("", self) 
		self.wechat.setGeometry(200, 155, 100, 106)
		pic = QPixmap(get_sys_png("wechat"));
		del_sys_png('wechat')		
		self.wechat.setPixmap(pic)		
		#----
		lb = QLabel("希望使用后有好的意见反馈给我，再次感谢！", self) 
		lb.move(20, size[1]-28)
		#----
		self.txt.setText(notes)

	def quit(self):
		self.hide()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	about = About_Soft()
	about.show()
	sys.exit(app.exec_())