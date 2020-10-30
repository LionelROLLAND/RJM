import matplotlib.pyplot as plt
import random as rd
rd.seed()

class tableau():
	
	def __init__(self, tab, d, x_b = 0, y_b = 0):
		self.d_val = d
		self.x_b = x_b
		self.y_b = y_b
		self.w = len(tab[0])
		self.h = len(tab)
		self.id = tab
	
	def show(self, inter = 'nearest'):
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

def est_premier(n):
	if n <= 1:
		return False
	i = 2
	while i*i <= n:
		if n%i == 0:
			return False
		i += 1
	return True

def alea(n): #retourne True avec une proba pr
	if rd.random() <= pr:
		return True
	return False


#parcourt le tableau t en "spirale carrée", en coloriant en blanc les cases où f(i) est vraie, où i est la longueur du chemin parcouru,
#s'arrête quand on a parcouru n cases
def meta_spi(n,f):
	c = 0
	t = tableau([[0]],0)
	x,y,dx,dy = 0,0,0,1
	i = 0
	p = 1 #chemin à parcourir en ligne droite (augmente de 1 tous les deux tournants)
	while i <= n:
		for k in [0,1]: #exécute 2 fois ce qui suit
			j = 1
			while i <= n and j <= p:
				if f(i):
					t.chg_elt(x,y,1)
					c += 1 #compte combien de fois f est vraie dans le parcours
				x += dx
				y += dy
				i += 1
				j += 1
			dx,dy = dy,-dx #tourne à droite
		p += 1
	t.show()
	return c/n #proportion de cases où f est vraie

N = 100 #petite démo :)
pr = meta_spi(N*N,est_premier)
meta_spi(N*N,alea) #pr = proportion de nb premiers jusqu'à N*N, pour avoir à peu près le même nb de cases blanchies mais aléatoirement
#a titre de comparaison
print(pr)
input()
