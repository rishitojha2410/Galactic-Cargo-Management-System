#implementation of AVL tree in python:
from node import Node 
class AVLTree:
    def __init__(self, compare_function):
        self.root = None
        self.size = 0
        self.compare = compare_function
    
    def insert(self, key, obj):
        new_node = Node(key, obj)
        self.root = self._insert(self.root, new_node)
    
    def _insert(self, root, new_node):
        if not root:
            return new_node
        if self.compare(new_node, root) < 0:
            root.left = self._insert(root.left, new_node)
        else:
            root.right = self._insert(root.right, new_node)
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        return self._balance(root)
    
    def delete(self, key):
        temp_node = Node(key)
        self.root = self._delete(self.root, temp_node)

    def _delete(self, root, temp_node):
        if not root:
            return root
        if self.compare(temp_node, root) < 0:
            root.left = self._delete(root.left, temp_node)
        elif self.compare(temp_node, root) > 0:
            root.right = self._delete(root.right, temp_node)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            temp = self._get_min_value_node(root.right)
            root.key = temp.key
            root.obj = temp.obj
            root.right = self._delete(root.right, temp)
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        return self._balance(root)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if not root:
            return None
        if key < root.key:
            return self._search(root.left, key)
        elif key > root.key:
            return self._search(root.right, key)
        else:
            return root.obj
    
    def _get_min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def _get_height(self, node):
        return 0 if node is None else node.height

    def _get_balance(self, node):
        return 0 if node is None else self._get_height(node.left) - self._get_height(node.right)

    def _balance(self, node):
        balance = self._get_balance(node)
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, z):
        y = z.right
        z.right = y.left
        y.left = z
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _rotate_right(self, z):
        y = z.left
        z.left = y.right
        y.right = z
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def in_order_traversal(self):
        return self._in_order_traversal(self.root)

    def _in_order_traversal(self, node):
        result = []
        if node:
            result.extend(self._in_order_traversal(node.left))
            result.append(node)
            result.extend(self._in_order_traversal(node.right))
        return result