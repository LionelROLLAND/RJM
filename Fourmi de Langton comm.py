import matplotlib.pyplot as plt
import matplotlib.animation as am

#Partie que je code :

#Ce qui suit c'est une classe qui sert à simuler un tableau infini dans toutes les directions,
# comme ça on n'a pas à se poser la question de si la fourmi va sortir du tableau
# parce qu'on sait pas où elle va aller : les cases sont toutes initialisées à self.d_val,
# sauf un nombre finies d'entre elles répertoriées dans self.id (un array 2D)
class tableau():
	
	def __init__(self, tab, d, x_b = 0, y_b = 0):
		self.d_val = d #valeur par défaut (partout à part là où on a déjà défini à l'aide de tab)
		self.x_b = x_b #abscisse du coin bas gauche de tab
		self.y_b = y_b #ordonnée du coin bas gauche de tab
		self.w = len(tab[0]) #largeur du tableau
		self.h = len(tab) #hauteur
		self.id = tab #le tableau où il y a l'information (toutes les cases qu'on a déjà touchées et qui ne sont plus forcément à self.d_val)
	
	def show(self, inter='nearest'): #affiche self.id (= les cases modifiées)
		plt.figure()
		plt.imshow(self.id, cmap = 'gray', interpolation = inter)
		plt.show()
	
	def copy(self):
		temp = [[self.id[i][j] for j in range(self.w)] for i in range(self.h)]
		return tableau(temp, self.d_val, self.x_b, self.y_b)


#fait le miroir dans le sens de la hauteur de self.id (parce que matplotlib affiche les tableaux à l'envers)
#(je m'en sers pas finalement parce que dans notre cas c'est pas très grave de voir la figure à l'envers)
	def reverse_y(self):
		temp = []
		for i in range(self.h):
			temp.append(self.id[self.h - i - 1])
		self.id = temp
	
	def add_c(self, c): #rajoute une colonne à droite ou à gauche des existantes
		if c>0:
			for j in range(self.h):
				self.id[j] = self.id[j] + [self.d_val]
		else:
			for j in range(self.h):
				self.id[j] = [self.d_val] + self.id[j]
			self.x_b -= 1
		self.w += 1
	
	def add_l(self, c): #rajoute une ligne en haut ou en bas des existantes
		if c>0:
			self.id = self.id + [[self.d_val for i in range(self.w)]]
		else:
			self.id = [[self.d_val for i in range(self.w)]] + self.id
			self.y_b -= 1
		self.h += 1
	
	def elt(self,x,y): #equivalent à t[y][x] pour t un array 2D
		if x<self.x_b or y<self.y_b or x>=self.x_b+self.w or y>=self.y_b+self.h:
			return self.d_val
		else:
			return self.id[y-self.y_b][x-self.x_b]
	
	def chg_elt(self,x,y,e): #equivalent à t[y][x] = e
		if x<self.x_b or x>=self.x_b+self.w:
			self.add_c(x-self.x_b)
			self.chg_elt(x,y,e)
		elif y<self.y_b or y>=self.y_b+self.h:
			self.add_l(y-self.y_b)
			self.chg_elt(x,y,e)
		else:
			self.id[y-self.y_b][x-self.x_b] = e
	
	def include(self,left,right,bottom,top): #agrandit self.id pour qu'il représente le rectangle contenu entre left et right en abscisse et bottom et top en ord.
		self.chg_elt(left,bottom,self.elt(left,bottom))
		self.chg_elt(right,top,self.elt(right,top))


#joue la vidéo (en noir et blanc) correspondants à l la liste d'array de 0 et de 1 (O = noir, 1 = blanc) à raison de ms millisecondes par frame
def video(l, ms):
	fig, ax = plt.subplots()
	ax.imshow(l[0],cmap='gray')
	ims = [[ax.imshow(l[i],cmap='gray',animated=True)] for i in range(len(l))]
	ani = am.ArtistAnimation(fig, ims, interval=ms, blit=True, repeat_delay=5000)
	plt.show()


#partie que elles elles codent :


#fait avancer la fourmi (représentée par sa position x,y et sa direction dx,dy (pos = x,y,dx,dy)) sur le tableau tab :
#ça met à jour pos et tab
def avance(pos,tab):
	x,y,dx,dy = pos
	c = 1 - tab.elt(x,y) #c = 0 si tab.elt(x,y) = 1 et inversement
	tab.chg_elt(x,y,c) #change la couleur de la case sur laquelle est la fourmi
	n_x = x + dx #noiuvelle position de la fourmi
	n_y = y + dy
	if tab.elt(n_x,n_y) == 0: #nouvelle direction de la fourmi
		n_dx = -dy
		n_dy = dx
	else:
		n_dx = dy
		n_dy = -dx
	pos[0],pos[1],pos[2],pos[3] = n_x,n_y,n_dx,n_dy #là je pensais faire un commentaire sur le fait que je pouvais pas
#écrire pos = n_x,n_y,n_dx,n_dy même si ça semble être la même chose du fait du fonctionnement de python

def sel_frames(n_d,n_f): #retourne la liste des arrays correspondants aux étapes qu'on veut voir
	test = tableau([[1]],1)
	u = [0,0,0,1] #on place la fourmi à 0,0 et qui va vers le haut (dx = 0, dy = 1)
	for i in range(n_f+1):
		avance(u,test)
	#A l'issue de cette boucle le tableau test a été agrandi de sorte à laisser assez de place à la fourmi :
	#maintenant on sait quelle taille de tableau utiliser pour l'affichage et on peut donc refaire la même
	#chose avec un tableau dont le self.id ne va pas changer de taille
	left = test.x_b #on prend les dimensions du tableau
	right = test.x_b + test.w - 1
	bottom = test.y_b
	top = test.y_b + test.h - 1
	final = tableau([[1]],1)
	final.include(left,right,bottom,top) #on dimensionne le final.id de sorte que la fourmi n'en sorte pas, et donc que sa taille ne varie pas
	f = [0,0,0,1]
	l = []
	for i in range(n_f+1):
		avance(f,final)
		if i >= n_d: #on prend que les étapes entre n_d et n_f
			l.append(final.copy().id)
	return l

video(sel_frames(0,100),50) #petite démo :)

