import matplotlib.pyplot as plt
import matplotlib.animation as am

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


def video(l, ms):
	fig, ax = plt.subplots()
	ax.imshow(l[0],cmap='gray')
	ims = [[ax.imshow(l[i],cmap='gray',animated=True)] for i in range(len(l))]
	ani = am.ArtistAnimation(fig, ims, interval=ms, blit=True, repeat_delay=5000)
	plt.show()
