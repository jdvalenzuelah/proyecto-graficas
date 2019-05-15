#Universidad del Valle de Guatemala
#Josue Valenzuela 171001

import struct

class BMP(object):
		"""
		Clase representando archivo Bitmap

		 Attributes:
		 	width (int): Ancho de archivo. El valor debe ser mayor que 0.
		 	height (int): Altura del archivo. El valor debe ser mayor que 0.
		"""
		def __init__(self, width, height):
			"""
			Inicializa valores del archivo en negro
			"""
			self.width = abs(int(width))
			self.height = abs(int(height))
			self.framebuffer = []
			self.zbuffer = []
			self.clear()

		def clear(self, r=0, b=0, g=0):
			"""
			Limpia bitmap a un solo color.
			"""
			self.framebuffer = [
				[
					self.color(r, b, g)
						for x in range(self.width)					
				]
				for y in range(self.height)
			]

			self.zbuffer = [ [-float('inf') for x in range(self.width)] for y in range(self.height)]

		def color(self, r=0, g=0, b=0):
			"""
			Define bytes del color, r, g b deben de ser integers entre 0 y 255.
			Entrada incorrecta pondra valores en 0.
			"""
			if (r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b <0):
				r = 0
				g = 0
				b = 0
			return bytes([b, g, r])

		def point(self, x, y, color):
			"""
			Cambiar color a un pixel especifico.
			Si indice fuera de limites, no hace cambios
			"""
			if(x < self.width and y < self.height):
				try:
					self.framebuffer[x][y] = color
				except Exception as e:
					pass
				

		def write(self, filename, zbuffer=False):
			"""
			Escribit el archivo
			"""
			print("writing bmp file")
			BLACK = self.color(0,0,0)
			import os
			os.makedirs(os.path.dirname(filename), exist_ok=True)
			file = open(filename, "bw")

			#Header de archivo (14 bytes)
			file.write(self.__char("B"))
			file.write(self.__char("M")) #BM
			file.write(self.___dword(14 + 40 + self.width * self.height * 3)) #File size
			file.write(self.___dword(0))
			file.write(self.___dword(14 + 40))

			#Header de imagen (14 bytes)
			file.write(self.___dword(40))
			file.write(self.___dword(self.width))
			file.write(self.___dword(self.height))
			file.write(self.___word(1))
			file.write(self.___word(24))
			file.write(self.___dword(0))
			file.write(self.___dword(self.width * self.height * 3))
			file.write(self.___dword(0))
			file.write(self.___dword(0))
			file.write(self.___dword(0))
			file.write(self.___dword(0))

			#Datos imagen
			for x in range(self.width):
				for y in range(self.height):
					if(x < self.width and y < self.height):
						if zbuffer:
							if self.zbuffer[y][x] == -float("inf"):
								file.write(BLACK)
							else:
								z = abs(int(self.zbuffer[y][x]*255))
								file.write(self.color(z,z,z))
						else:
							file.write(self.framebuffer[y][x])
					else:
						file.write(self.__char("c"))

			file.close()

		def load(self, filename):
			file = open(filename, "rb")
			file.seek(10)
			headerSize = struct.unpack("=l", file.read(4))[0]
			file.seek(18)

			self.width = struct.unpack("=l", file.read(4))[0]
			self.height = struct.unpack("=l", file.read(4))[0]
			self.clear()
			for y in range(self.height):
				for x in range(self.width):
					if x < self.width and y < self.height:
						b, g, r = ord(file.read(1)), ord(file.read(1)), ord(file.read(1))
						self.point(x, y, self.color(r,g,b))
			file.close()


		def __padding(self, base, c):
			"""
			Agregar pading a un numero
			"""
			if(c %  base == 0):
				return c
			else:
				while (c % base):
					c += 1
				return c

		def __char(self, c):
			"""
			Helpfull
			"""
			return struct.pack("=c", c.encode("ascii"))

		def ___word(self, c):
			"""
			Helpfull
			"""
			return struct.pack("=h", c)

		def ___dword(self, c):
			"""
			Helpfull
			"""
			return struct.pack("=l", c)

		def getZbufferValue(self, x, y):
			"""
			Get a value of (x,y) coordinates inside of the zbuffer
			"""
			if x < self.width and y < self.height:
				return self.zbuffer[x][y]
			else:
				return -float("inf")

		def setZbufferValue(self, x, y, z):
			"""
			Set z value on (x,y) coordinates on zbuffer
			"""
			if x < self.width and y < self.height:
				self.zbuffer[x][y] = z
				return 1
			else:
				return 0
