import itertools as it
import json
from pprint import pprint
from copy import deepcopy

class _Node:
	def __init__(self, name, content=None):
		self.name = name
		self.content = content if content != None else {}

	def __hash__(self):
		return hash(self.name)

	def __str__(self):
		return self.name

class KnowledgeMap:
	def __init__(self):
		self._map = {}
		self._anchor = {}

	def __str__(self):
		str_dict = {}
		for key, val in self._map.items():
			str_dict[str(key)] = list([str(v) for v in val]) 
		return json.dumps(str_dict) #+ '\n' + json.dumps(self._anchor)

	def add_node(self, name, content=None, neighbours=None):
		newNode = _Node(name, content)
		try:
			print('add_node: Node already exists: {' + name + ': ' + self._anchor[name] + '}')
		except:
			self._anchor[name] = newNode
			self._map[newNode] = neighbours if neighbours != None else set()

	def add_edge(self, name_pair):
		try:
			node1 = self._anchor[name_pair[0]]
			node2 = self._anchor[name_pair[1]]
			self._map[node1].add(node2)
			self._map[node2].add(node1)
		except:
			print('add_edge: Node does not exist: {' + name_pair[0] + ' and/or ' + name_pair[1] + '}')

	def get_neighbours(self, name):
		try:
			node = self._anchor[name]
			return self._map[node]
		except:
			print('node_with_name: Node does not exist: {' + name + "}")
			

class Logic:
	def __init__(self, data, name=None):
		self.name = name
		self.map = KnowledgeMap()

		nodes = data['node']
		neigs = data['neighbour']
		paths = data['path']
		list(map(lambda n: self.map.add_node(n.pop('name')), nodes))
		list(map(lambda n: list(map(self.map.add_edge, it.zip_longest(it.repeat(n[0], len(n[1])), n[1]))), neigs.items()))
		list(map(lambda p: map(self.map.add_edge, it.zip_longest(p[:-1], p[1:])), paths))

	def resp(self, data):
		return None

if __name__ == '__main__':
	f = open('test.json', 'r')
	data = json.loads(f.read())
	f.close()


	test_logic = Logic(data, 'test')
	print(test_logic.map)

	