import matplotlib.pyplot as plt

class tableau():
	
	def __init__(self, tab, d, x_b = 0, y_b = 0):
		self.d_val = d
		self.x_b = x_b
		self.y_b = y_b
		self.w = len(tab[0])
		self.h = len(tab)
		self.id = tab
	
	def show(self,inter = 'nearest'):
		plt.figure()
		plt.imshow(self.id, cmap = 'gray', interpolation = inter)
		plt.pause(0.1)
	
	def copy(self):
		temp = [[self.id[i][j] for j in range(self.w)] for i in range(self.h)]
		return tableau(temp, self.d_val, self.x_b, self.y_b)
	
	def reverse_y(self):
		temp = []
		for i in range(self.h):
			temp.append(self.id[self.h - i - 1])
		self.id = temp
	
	def add_c(self, c):
		if c>0:
			for j in range(self.h):
				self.id[j] = self.id[j] + [self.d_val]
		else:
			for j in range(self.h):
				self.id[j] = [self.d_val] + self.id[j]
			self.x_b -= 1
		self.w += 1
	
	def add_l(self, c):
		if c>0:
			self.id = self.id + [[self.d_val for i in range(self.w)]]
		else:
			self.id = [[self.d_val for i in range(self.w)]] + self.id
			self.y_b -= 1
		self.h += 1
	
	def elt(self,x,y):
		if x<self.x_b or y<self.y_b or x>=self.x_b+self.w or y>=self.y_b+self.h:
			return self.d_val
		else:
			return self.id[y-self.y_b][x-self.x_b]
	
	def chg_elt(self,x,y,e):
		if x<self.x_b or x>=self.x_b+self.w:
			self.add_c(x-self.x_b)
			self.chg_elt(x,y,e)
		elif y<self.y_b or y>=self.y_b+self.h:
			self.add_l(y-self.y_b)
			self.chg_elt(x,y,e)
		else:
			self.id[y-self.y_b][x-self.x_b] = e
	
	def include(self,left,right,bottom,top):
		self.chg_elt(left,bottom,self.elt(left,bottom))
		self.chg_elt(right,top,self.elt(right,top))

#Partie que elles elles codent :

def rev(l):
	return [l[len(l) - i - 1] for i in range(len(l))]

def opp(l):
	return [-l[i] for i in range(len(l))]

#crée la liste des tournants dans la feuille : 1 pour droite, -1 pour gauche : impossible à expliquer pourquoi cette fonction
#marche sans dessin par contre ^^' Mais avec dessin c'est intuitif :)
def liste_d(n):
	if n == 1:
		return [1]
	else:
		r = liste_d(n-1)
		return r + [1] + opp(rev(r))

def dessine(n): #"déplie" la feuille plié avec la liste l en mettant tous les tournants à angle droit
	l = liste_d(n)
	t = tableau([[1]],1)
	x,y,dx,dy = 0,0,0,1
	u = 2 #longueur en cases de chaque section de feuille non pliée
	for e in l: #là on va parcourir le tableau selon le chemin tracé par la feuille dépliée
		for i in range(u):
			t.chg_elt(x,y,0)
			x += dx
			y += dy
		if e == 1:
			dx,dy = dy,-dx #tourne à droite
		else:
			dx,dy = -dy,dx #tourne à gauche
	for i in range(u): #juste pour bien finir le dessin, sinon il manque un petit bout de feuille
		t.chg_elt(x,y,0)
		x += dx
		y += dy
	t.chg_elt(x,y,0) #idem haha
	if n >= 13: #ça c'est pour que l'affichage soit joli dans tous les cas
		t.show('hanning')
	else:
		t.show()

for i in range(4): #petite démo :)
	plt.figure()
	dessine(i+1)
	plt.pause(1)
plt.figure()
dessine(10)
plt.pause(1)
plt.figure()
dessine(13)
plt.pause(1)
input()
	
