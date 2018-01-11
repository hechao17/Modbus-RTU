import base64

def handle_png_to_py(name):
	open_png = open("%s.png" % name, 'rb')
	b64str = base64.b64encode(open_png.read())
	open_png.close()

	write_data = 'img = "%s"' % b64str.decode()
	f = open("%s.py" % name, 'w+')
	f.write(write_data)
	f.close()



if __name__ == '__main__':
	pictrue = ['green', "red", 'title', 'wechat']
	for i in pictrue:
		handle_png_to_py(i)