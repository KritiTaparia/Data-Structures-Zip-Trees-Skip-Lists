# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

import random
from typing import TypeVar

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class TreeNode:
	def __init__(self, key: KeyType, val: ValType, rank: int):
		self.key = key
		self.val = val
		self.rank = rank
		self.left = self.right = None

class ZipTree:
	def __init__(self):
		self.root: TreeNode = None
		self.count: int = 0

	@staticmethod
	def get_random_rank() -> int:
		import math
		def geometric_custom():
			u = random.random()
			k = math.floor(math.log(1 - u) / math.log(0.5))

			return k
		return geometric_custom()

	# returns a node based on the value, its parent, depth and whether left/ right child
	def search_node(self, key, root, parent, is_left_flag, depth):
		if root is None:
			return None, parent, is_left_flag, depth
		if root.key == key:
			return root, parent, is_left_flag, depth
		elif root.key < key:
			return self.search_node(key, root.right, root, False, depth + 1)
		else:
			return self.search_node(key, root.left, root, True, depth + 1)
		
	def insert(self, key: KeyType, val: ValType, rank: int = -1):
		self.count += 1
		new_node_rank = self.get_random_rank()
		new_node_rank = rank
		new_node = TreeNode(key, val, new_node_rank)
		if self.root is None:
			self.root = new_node
			return

		# function to find the position of the insetion of the node
		def find_insertion_position(rank, key, root, parent, is_left_flag):
			if root is None:
				# print('P:', parent.key if parent else -1)
				return None, parent, is_left_flag
			if root.rank < rank or (root.rank == rank and root.key > key):
				return root, parent, is_left_flag
			elif root.key < key:
				return find_insertion_position(rank, key, root.right, root, False)
			else:
				return find_insertion_position(rank, key, root.left, root, True)

		def unzip_lookup(k, node):
			if node is None:
				return (None, None)
			if node.key < k:
				(P, Q) = unzip_lookup(k, node.right)
				node.right = P
				return (node, Q)
			else:
				(P, Q) = unzip_lookup(k, node.left)
				node.left = Q
				return (P, node)
		
		
		insertion_point, parent, is_left_flag = find_insertion_position(new_node_rank, key, self.root, None, None)

		if insertion_point is not None:
			(P, Q) = unzip_lookup(key, insertion_point)
			# attach P and Q
			new_node.left = P
			new_node.right = Q

		if parent is not None:
			if is_left_flag:
				parent.left = new_node
			else:
				parent.right = new_node
		else:
			self.root = new_node

	def remove(self, key: KeyType):
		def zipup(P, Q):
			if P is None:
				return Q
			if Q is None:
				return P
			
			if Q.rank > P.rank:
				Q.left = zipup(P, Q.left)
				return Q
			else:
				P.right = zipup(P.right, Q)
				return P
			
		node, parent, is_left_flag, _ = self.search_node(key, self.root, None, None, 0)

		merged_list = zipup(node.left, node.right)



		if parent is not None:
			if is_left_flag:
				parent.left = merged_list
			else:
				parent.right = merged_list
		else:
			self.root = merged_list

		self.count -= 1

	def find(self, key: KeyType) -> ValType:
		return self.search_node(key, self.root, None, False, 0)[0].val

	def get_size(self) -> int:
		return self.count

	def get_height(self) -> int:
		def max_depth(node):
			if node is None:
				return 0
			else:
				max_depth_left = max_depth(node.left)
				max_depth_right = max_depth(node.right)
				return max(max_depth_left + 1, max_depth_right + 1)
		
		return max_depth(self.root) - 1

	def get_depth(self, key: KeyType):
		return self.search_node(key, self.root, None, None, 0)[3]

# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
