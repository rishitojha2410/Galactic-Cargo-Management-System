# a node in AVL tree: 
class Node:
    
    def __init__(self,key,binobj=None):
        self.key = key  #will either be used as a tuple storing (id,capacity) pair or will be used to store object size or bin size
        self.obj = binobj #to store the bin or object so that we can extract all attributes of the bin or object. 
        self.left = None #left child
        self.right = None #right child
        self.height = 1 #any non-leaf node has height 1