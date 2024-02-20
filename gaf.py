import struct
import zlib

class Gaf:
	def __init__(self, bytes):
		self.bytes = bytes
		self.pos = 0#self.len()
		self.config = {}

	def len(self):
		return len(self.bytes)

	def read(self, index):
		old_pos = self.pos
		self.pos += index #self.pos -= index
		return self.bytes[old_pos:self.pos][::-1]#return self.bytes[self.pos:old_pos]

	def read_i8(self):
		return struct.unpack(">b", self.read(1))[0]

	def read_u8(self):
		return struct.unpack(">B", self.read(1))[0]

	def read_i16(self):
		return struct.unpack(">h", self.read(2))[0]

	def read_u16(self):
		return struct.unpack(">H", self.read(2))[0]

	def read_i32(self):
		return struct.unpack(">i", self.read(4))[0]

	def read_f32(self):
		return struct.unpack(">f", self.read(4))[0]

	def read_u32(self):
		return struct.unpack(">I", self.read(4))[0]

	def read_i64(self):
		return struct.unpack(">q", self.read(8))[0]

	def read_f64(self):
		return struct.unpack(">d", self.read(8))[0]


	def dezlib(self):
		zlibdata = self.bytes[10:]
		self.bytes = zlib.decompress(zlibdata)

	def process(self):
		#self.bytes = self.bytes[::-1]
		compress = self.read_i32() # 4669763
		major = self.read_i8()
		minor = self.read_i8()
		leng = self.read_u32()
		self.config["compress"] = compress
		self.config["major"] = major
		self.config["minor"] = minor
		self.config["length"] = leng
		self.config["show"] = {}
		if compress == 4669763:
			self.dezlib()
			if major < 4:
				self.pos = 0 #len(self.bytes)
				#self.bytes = self.bytes[::-1]
				frame_count = self.read_i16()
				self.config["show"]["frames"] = frame_count
				bounds = (self.read_f32(), self.read_f32(), self.read_f32(), self.read_f32()) # хитбокс объекта
				pivot = (self.read_f32(), self.read_f32()) # точка опоры/оси
				self.config["show"]["object"] = {}
				self.config["show"]["object"]["bounds"] = bounds
				self.config["show"]["object"]["pivot"] = pivot
		self.next_tag()

	def read_layer(self):
		layerLeng = self.read_u32()
		self.config["show"]["object"]["layer"] = []
		while (layerLeng):
			part_id = self.read_u32()
			utf8Len = self.read_i16()
			layer = self.read(utf8Len)[::-1].decode()
			layerLeng-=1
			self.config["show"]["object"]["layer"].append(layer)

	def read_config(self):
		self.config["fps"] = self.read_i8()
		self.config["show"]["object"]["color"] = -self.read_i32()
		self.config["show"]["object"]["width"] = self.read_u16()
		self.config["show"]["object"]["height"] = self.read_u16()

	def read_anim_seq(self):
		self.config["show"]["animate"] = {}
		animLeng = self.read_u32()
		while (animLeng):
			utf8Len = self.read_i16()
			#print("LEN UTF", utf8Len)
			name = self.read(utf8Len)[::-1].decode()
			enabled = bool(self.read_i16())
			duration = self.read_i16()
			self.config["show"]["animate"][name] = {"enabled": enabled, "duration": duration}
			animLeng -= 1
		"""while(_loc4_ < _loc3_)
									{
									   _loc5_ = param1.readUTF();
									   _loc6_ = param1.readShort();
									   _loc7_ = param1.readShort();
									   param2.addSequence(_loc5_,_loc6_,_loc7_);
									   _loc4_++;
									}"""


	def next_tag(self):
		while True:
			tag = self.read_i16()
			addpos = self.read_u32()
			print(tag, addpos)
			if tag == 0:
				print(self.config)
				break
				# конец
			elif tag < 5:
				self.read(addpos)
			elif tag == 5:
				self.read_layer()
				# слои
			elif tag == 6:
				self.read_anim_seq()
				# анимац. порядок
			elif tag == 7:
				...
			elif tag == 8:
				...
			elif tag == 9:
				self.read_config()
				# настройки холста
			elif tag == 10:
				...
			elif tag == 11:
				...
			elif tag == 12:
				...
			elif tag == 13:
				...
			elif tag == 14:
				...
			elif tag == 15:
				...

				




#Gaf(b"CAG\x00\x03\x0f\xe2\x00\x00\x00x\xdacd8{f\x8fC\xda3E\xe7Y3%\x9df\xcd\xb4w\x02\xf2\x0f\x00\xf9\x87\x19\x19|\x18@\xa0\xc1\x9e\x91\x11H1\x8a0\xb8g\x16\xe5\xc4'\x97\xa4T\x1aY\x18\x19W8V\xe8\x15\xe4\xa5\x83\xe5\xc1\xea\x0e\x1c``P:\xcc\xc0\xb0\xcd\x89\x81!\xc4\x19$\xce\xc0\xa0\x01d{8\x81\xe4\xd9\x81\x98\x99\x81\x07d\x10\x10\x0bBEX\x19\x04\x90D\xd8\x182\x83<\x12\xf3RX\x18\x8c\xa1\xa20\x0cU\xc0\x00u\x10\x04#\xf8g\xcf\x9c\xb1\x05\xb18\x81\x90\x81A\xc2\xd8\xd8\xf8\xbf\x0f\x8b\x023D\x1a\x00\x89S%^").process()
Gaf(open(input("File gaf: "), "rb").read()).process()
		



