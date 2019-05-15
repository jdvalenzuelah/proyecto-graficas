"""
Universidad del Valle de Guatemala
Graficas por computadora
Proyecto 1
"""
from Render.SR import SR
import random


def star(sr, light=(0,0,1), bary=(1,1,1), Vnormals=0,baseColor=(1,1,1)):
	"""
	Shader to look like  the sun
	"""
	baseColor = (1,0.8431,0)
	w, v, u = bary
	nA, nB, nC = Vnormals
	light = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))

	iA = sr.dot(nA, light)
	iB = sr.dot(nB, nA)
	iC = sr.dot(nC, nB)

	intensity = w*iA + v*iB + u*iC

	if intensity <= 0:
		intensity = 0.85
	elif intensity < 0.25:
		intensity = 0.75
	elif intensity < 0.75:
		intensity = 0.55
	elif intensity < 1:
		baseColor = (1,1,0)
		intensity = 0.80


	r = intensity * baseColor[0]
	g = intensity * baseColor[1]
	b = intensity * baseColor[2]

	return sr.glColor(r,g,b)

def moon(sr, light=(0,0,1), bary=(1,1,1), Vnormals=0,baseColor=(1,1,1)):
	"""
	shader to smooth the surfaces and give a look like the moon
	"""
	# barycentric
	w, v, u = bary
	# normals
	nA, nB, nC = Vnormals
	light = (0,1,-2)
	# light intensity
	iA, iB, iC = [ sr.dot(n, light) for n in (nA, nB, nC) ]
	intensity = w*iA + v*iB + u*iC
	return sr.glColor(
	      baseColor[2] * intensity,
	      baseColor[1] * intensity,
	      baseColor[0] * intensity
	    )

# -------------- Main starts here --------------------------
image = SR()
image.glInit()
image.glCreateWindow(1500, 1500)
image.lookAt((-1,3,5), (0,0,0), (0,1,0))
image.glViewPort(0,0,1500,1500)
image.setFileName("./proyecto.bmp")

def mt(x, y):
	"""
	Load asteroid
	"""
	print("credit to Frogpony for 3d model")
	image.loadOBJ("./models/mt.obj", translate=(x,y,-0.30), scale=(0.08,0.08,0.08), rotate=(0.40,0.25,-0.1), fill=True, shader=moon)

#Stars background
for x in range(random.randint(300, 500)):
	x = random.uniform(-1,1)
	y = random.uniform(-1,1)
	image.glVertexV4(x,y)
#Random asteroids and positions
for x in range(random.randint(1,5)):
	mt(random.uniform(0,1), random.uniform(0,1))
#Load spaceship
print("CRedit to artturi for 3d models")
image.loadOBJ("./models/tr.obj", translate=(0.25,-0.75,0.3), scale=(0.08,0.08,0.08), rotate=(0.25,0.8,-0.25), fill=True)
#load atronaut
print("CRedit to artturi for 3d models")
image.loadOBJ("./models/ast.obj", translate=(0.80,-1,0), scale=(0.05,0.05,0.05), rotate=(-1,0.5,0), fill=True)
#load space station
print("CRedit to artturi for 3d models")
image.loadOBJ("./models/ss.obj", translate=(-0.30,-0.20,-0.25), scale=(0.16,0.16,0.16), rotate=(-1.50,-0.80,1), fill=True)

#load moon and star
image.loadOBJ("./models/planetN.obj", translate=(0.50,0.75,0), scale=(0.3,0.3,0.3),fill=True, shader=moon)
image.loadOBJ("./models/planetN.obj", translate=(-0.75,1,0), scale=(0.12,0.12,0.12), rotate=(1,1,1),shader=star)

#write changes
image.glFinish()
