import itertools as it
import json

class a:
     def __init__(self):
             self.name = 'test'
             self.dict = {}
             self.list = []
             self.test = {1:2, 3:4, 5:6}
     def __str__(self):
             return json.dumps(self.test)



if __name__ == '__main__':
	b = {1:2, 2:3, 3:4}
	try:
		x = b[1]
		y = b[2]
		z = b[4]
	except:
		print('hah')
	print(x, y, z)
	print(a())