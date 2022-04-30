from bs4 import BeautifulSoup
from Levenshtein import distance
from pip import main

# https://www.unixuser.org/~euske/python/webstemmer/howitworks.html
class Webpage:
	BLOCKS = [
		'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
		'title', 'p', 
		'table', 'tr', 'td', 'hr',
		'code', 'cite',
		'nav', 'summary', 'u', 'i'
	]
	def __init__(self,path):
		self.path = path
		self.blocks = []
		self.anchors = []
		self._init()

	# STEP 1
	def _init(self): 
		print(self.path)
		with open(self.path, errors='ignore') as f:
			soup = BeautifulSoup(f.read(), 'html.parser')
			for b in soup.descendants:
				if b.name == 'a':
					self.anchors.append(b)
				if b.name in self.BLOCKS:
					if len(b.text) > 0:
						print(b.name)
						self.blocks.append(b)
	
	# STEP 2, STEP 4 (removing banners and nav links)
	def getSimilarBlocks(self, webpage):
		size = min([len(webpage.blocks), len(self.blocks)])
		newBlocks = []
		for i in range(size):
			b1 = self.blocks[i]
			b2 = webpage.blocks[i]
			if b1.name == b2.name:
				d = distance(b1.text, b2.text)
				maxChars = max([len(b1.text), len(b2.text)])
				distP = d/maxChars
				if distP > 0.1:
					newBlocks.append(b1)
		self.blocks = newBlocks
	
	# STEP 5
	def findTitle(self):
		for a in self.anchors:
			minDistance = 1
			bestMatchingBlock = None
			for b in self.blocks:
				d = distance(a.text, b.text)
				maxChars = max([len(a.text), len(b.text)])
				distP = d/maxChars
				if distP < minDistance:
					bestMatchingBlock = b
					minDistance = distP
			if minDistance < 0.90:
				if None not in [a, bestMatchingBlock]:
					print(f'{round(minDistance*100, 2):<10}% -> {a.text:<50} || {bestMatchingBlock.text:<50}'.replace('\n', ''))


	


def webrunner(path1, path2):
	web1 = Webpage(path1)
	web2 = Webpage(path2)
	web1.getSimilarBlocks(web2)
	web1.findTitle()

if __name__ == '__main__':
	webrunner(
		'WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html',
		'WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html'
	)