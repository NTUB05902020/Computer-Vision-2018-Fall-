import numpy
import sys
B, W = 0, 255

class PIC:
	"""
	def checkIn(cor, arr):
		for tmp in arr:
			if numpy.array_equal(cor, tmp): return True
		return False
	"""
	def __init__(self, row, column, points, compl=None):
		self.row, self.col = row, column
		self.Ws, self.Bs = points, compl
	def toDataArray(self):
		ret = numpy.zeros((self.row, self.col), dtype=numpy.uint8)
		for r,c in self.Ws: ret[r][c] = W
		return ret
	def printPIC(self):
		print(self.row, self.col)
		print(self.Ws)
	def getmmMM(self):
		mr, mc, Mr, Mc = None, None, None, None
		for i,j in self.Ws:
			if mr==None or mr>i: mr = i
			if mc==None or mc>j: mc = j
			if Mr==None or Mr<i: Mr = i
			if Mc==None or Mc<j: Mc = j
		return mr,mc,Mr,Mc
	def dilation(self, pic):
		whole = set([(i,j) for i in range(self.row) for j in range(self.col)])
		return PIC(self.row, self.col, whole.intersection(set([(r1+r2,c1+c2) for r1,c1 in self.Ws for r2,c2 in pic.Ws])))
	def erosion(self, pic):
		new = self.complement().dilation(pic.reflection()).complement()
		#i+mr2>=mr1   j+mc2>=mc1
		#i+Mr2<=Mr1   j+Mc2<=Mc1
		(mr1,mc1,Mr1,Mc1), (mr2,mc2,Mr2,Mc2) = self.getmmMM(), pic.getmmMM()
		new.Ws = set([(i,j) for i in range(mr1-mr2, Mr1-Mr2+1) for j in range(mc1-mc2, Mc1-Mc2+1)]).intersection(new.Ws)
		return new
	def opening(self, pic):
		return self.erosion(pic).dilation(pic)
	def closing(self, pic):
		return self.dilation(pic).erosion(pic)
	def complement(self):
		if self.Bs == None: self.Bs = set([(i,j) for i in range(self.row) for j in range(self.col)]).difference(self.Ws)
		return PIC(self.row, self.col, self.Bs, self.Ws)
	def reflection(self):
		return PIC(self.row, self.col, set([(-i,-j) for i,j in self.Ws]))
	def hitAndMiss(self, pic1, pic2):
		tmp1, tmp2 = self.erosion(pic1), self.complement().erosion(pic2)
		return PIC(self.row, self.col, tmp1.Ws.intersection(tmp2.Ws))
	@staticmethod
	def imToPic(data_array):
		r, c = len(data_array), len(data_array[0])
		return PIC(r, c, set([(i, j) for i in range(r) for j in range(c) if data_array[i][j]==W]))

tffft = PIC(5, 5, [(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-2),(0,-1),(0,0),(0,1),(0,2),(1,-2),(1,-1),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1)])
J = PIC(2, 2, [(0,0), (1,0), (0,-1)])
K = PIC(2, 2, [(0,1), (-1,0), (-1,1)])