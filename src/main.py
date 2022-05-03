from bs4 import BeautifulSoup
from Levenshtein import distance
from pip import main

# https://www.unixuser.org/~euske/python/webstemmer/howitworks.html
class Webpage:
	BLOCKS = [
		'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
		'title', 'p',
		's','span','b',
		'code', 'cite',
		'nav', 'summary', 'u', 'i'
	]
	def __init__(self,path):
		self.path = path
		self.blocks = []
		self._init()


	# STEP 1
	def _init(self): 
		print(self.path)
		with open(self.path, errors='ignore') as f:
			soup = BeautifulSoup(f.read(), 'html.parser')
			for i,b in enumerate(soup.descendants):
				if b.name in self.BLOCKS:
					if len(b.text) > 0:
						print(i,b.name, b.text[:10])
						self.blocks.append(b)

	def alignWebsiteBlocks(self, webpage):
		s1 = {} #dictionary
		s2 = {}
		#find equal elements to align by text
		for b in self.blocks:
			for b2 in webpage.blocks:
				if b==b2 and len(b.text)>10:
					s1[b]=[]
					s2[b2]=[]
					break
		# add empty spaces 1st webpage
		for i in range(len(s1)-1):
			start=False
			key1=list(s1.keys())[i]
			key2 = list(s1.keys())[i+1]
			for b in self.blocks:
				if b==key2:
					break #nasli, gremo na naslednji key
				if start:
					s1[key1].append(b)
				if b==key1:
					start=True
					continue
		# align-search same elements
		for i in range(len(s2) - 1):
			start = False
			key1 = list(s2.keys())[i]
			key2 = list(s2.keys())[i + 1]
			for b in webpage.blocks:
				if b == key2:
					break  # nasli, gremo na naslednji key
				if start:
					s2[key1].append(b)
				if b == key1:
					start = True
					continue
		#fill missing elements

		for key,blocks in s1.items():
			blocks2 = s2[key]
			if len(blocks)<len(blocks2):
				for i in range(len(blocks2)):
					if i < len(blocks):
						if blocks[i].name!=blocks2[i].name:
							blocks.insert(i,BeautifulSoup(f"<{blocks2[i].name}></{blocks2[i].name}"))
					else:
						blocks.insert(i, BeautifulSoup(f"<{blocks2[i].name}></{blocks2[i].name}"))
			elif len(blocks)>len(blocks2):
				for i in range(len(blocks)):
					if i<len(blocks2):
						if blocks[i].name != blocks2[i].name:
							blocks2.insert(i, BeautifulSoup(f"<{blocks[i].name}></{blocks[i].name}"))
					else:
						blocks2.insert(i, BeautifulSoup(f"<{blocks[i].name}></{blocks[i].name}"))
		alignBlocks=[]
		for key,blocks in s1.items():
			alignBlocks.append(key)
			alignBlocks+=list(blocks)
		self.blocks=alignBlocks


	def equalLayout(self, webpage):
		s1 = len(self.blocks)
		s2 = len(webpage.blocks)
		if s1 != s2:
			print(s1, s2, 'leyout size')
			return False

		for i in range(s1):
			b1 = self.blocks[i]
			b2 = webpage.blocks[i]
			if b1.name != b2.name:
				print('tags not matching')
				print(b1.name,b2.name)
				return False
		return True
	# STEP 2, STEP 4 (removing banners and nav links)
	def removeSimilarBlocks(self, webpage):
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
	
	def createFormat(self):
		formatt=""
		for b in self.blocks:
			formatt += str(b) + "\n"

		return formatt


def webrunner(path1, path2):
	web1 = Webpage(path1)
	web2 = Webpage(path2)
	web1.alignWebsiteBlocks(web2)
	web2.alignWebsiteBlocks(web1)

	web1.removeSimilarBlocks(web2)
	formatt=web1.createFormat()
	with open("output.html","w") as f:
		f.write(formatt)


if __name__ == '__main__':
	webrunner(
		#'../WebPages/overstock.com/jewelry01.html',
		#'../WebPages/overstock.com/jewelry02.html'
		'../WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html',
		'../WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html'
	)