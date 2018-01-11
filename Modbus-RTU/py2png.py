import base64
import os
from png.green import img as green
from png.title import img as title
from png.wechat import img as wechat
from png.red import img as red

pic_soc = {	
	'green' 	: green,
	'title' 	: title,
	'wechat' 	: wechat,
	'red' 		: red,
}

def get_sys_png(name):
	tmp = open('%s.png' % name,'wb+')
	tmp.write(base64.b64decode(pic_soc[name]))
	tmp.close()
	return '%s.png' % name
def del_sys_png(name):
	os.remove('%s.png' % name)