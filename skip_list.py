# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import TypeVar
import random
from zip_tree import ZipTree

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class Node:
	def __init__(self, key: KeyType, val: ValType, height):
		self.key = key
		self.val = val
		self.next = [None] * height

class SkipList:
	def __init__(self):
		# 21 because get_random_level returns a
		self.head = Node(-float('inf'), -1, 21)
		self.tail = Node(float('inf'), -1, 21)
		self.max_height = 20
		for i in range(21):
			self.head.next[i] = self.tail


	def get_random_level(self, key: KeyType) -> int:
	  	# Do not change this function. Use this function to determine what level each key should be at. Assume levels start at 0 (i.e. the bottom-most list is at level 0)
		# e.g. for some key x, if get_random_level(x) = 5, then x should be in the lists on levels 0, 1, 2, 3, 4 and 5 in the skip list.
		random.seed(str(key))
		level = 0
		while random.random() < 0.5 and level < 20:
			level += 1
		return level

	def insert(self, key: KeyType, val: ValType, height=None):
		if height is None:
			new_height = self.get_random_level(key)
		else:
			new_height = height
		new_node = Node(key, val, new_height + 1)

		current_node = self.head
		level = self.max_height
		while level >= 0:
			next_node = current_node.next[level]
			if next_node and next_node.key > new_node.key:  # overshoot
				# insert here at this level
				if new_height >= level:
					current_node.next[level] = new_node
					new_node.next[level] = next_node
				# move to lower level
				level -= 1
			else:
				# move forward
				current_node = next_node

	def remove(self, key: KeyType):
		current_node = self.head
		level = self.max_height
		while level >= 0:
			next_node = current_node.next[level]
			if next_node and next_node.key >= key:
				if next_node.key == key:
					current_node.next[level] = next_node.next[level]
				# move to lower level
				level -= 1
			else:
				# move forward
				current_node = next_node

	def find(self, key: KeyType) -> ValType:
		current_node = self.head
		level = self.max_height
		while level >= 0:
			next_node = current_node.next[level]
			if next_node and next_node.key > key:
				if current_node.key == key:
					return current_node.val
				# move to lower level
				level -= 1
			else:
				# move forward
				current_node = next_node
		
		assert False

	def get_list_size_at_level(self, level: int):
		ptr = self.head.next[level]
		count = 0
		while ptr.key != float('inf'):
			count += 1
			ptr = ptr.next[level]
		return count

	def from_zip_tree(self, zip_tree: ZipTree) -> None:
		from math import ceil
		root = zip_tree.root

		def inorder(root):
			if root is not None:
				inorder(root.left)
				self.insert(root.key, root.val, height=int(ceil(root.rank)))
				inorder(root.right)
		
		inorder(root)

# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
