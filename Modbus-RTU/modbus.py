from crc import crc16

def int16_to_char(int16):
	return [int16>>8, int16&0xff]

def char_to_int16(c1, c2):
	return c1*256 + c2

class ModbusCmd:
	#读取指令
	def cmd03(self, addr, reg_start, reg_count):
		dat = []
		dat.append(addr)
		dat.append(0x03)
		dat.extend(int16_to_char(reg_start))
		dat.extend(int16_to_char(reg_count))
		check = crc16()
		check.createarray(dat)
		return bytes([a for a in dat]) 
	#06写指令
	def cmd06(self, addr, reg, value):
		dat = []
		dat.append(addr)
		dat.append(0x06)
		dat.extend(int16_to_char(reg))
		dat.extend(int16_to_char(value))
		check = crc16()
		check.createarray(dat)
		return bytes([a for a in dat])
	#10写指令
	def cmd10(self, addr, reg_start, reg_count, value_list):
		dat = []
		dat.append(addr)
		dat.append(0x10)
		dat.extend(int16_to_char(reg_start))
		dat.extend(int16_to_char(reg_count))
		dat.append(reg_count*2)
		for i in range(reg_count):
			dat.extend(int16_to_char(value_list[i]))		
		check = crc16()
		check.createarray(dat)
		return bytes([a for a in dat])

if __name__ == '__main__':
	a = 65539
	print(a//256)
	print(a%256)

