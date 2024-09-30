from avl import AVLTree
from bin import Bin
from object import Object, Color
from exception import NoBinFoundException
class GCMS:
    def __init__(self):
        self.bins_by_capacity = AVLTree(self._compare_bins_by_capacity)
        self.bins_by_id = AVLTree(self._compare_objects_by_id)
        self.object_bin_mapping = AVLTree(self._compare_objects_by_id)
        self.objects = AVLTree(self._compare_objects_by_id)

    def _compare_objects_by_id(self, node1, node2):
        return (node1.key > node2.key) - (node1.key < node2.key)

    def _compare_bins_by_capacity(self, node1, node2):
        cap1, id1 = node1.key
        cap2, id2 = node2.key
        if cap1 > cap2:
            return 1
        elif cap1 < cap2:
            return -1
        else:
            return (id1 > id2) - (id1 < id2)

    def add_bin(self, bin_id, capacity):
        new_bin = Bin(bin_id, capacity)
        self.bins_by_capacity.insert((new_bin.remaining_capacity, bin_id), new_bin)
        self.bins_by_id.insert(bin_id, new_bin)

    def add_object(self, object_id, size, color):
        new_object = Object(object_id, size, color)
        self.objects.insert(object_id, new_object)

        select_bin = None
        if color == Color.RED:
            select_bin = self._find_largest_fit_least_id(size)
        elif color == Color.GREEN:
            select_bin = self._find_largest_fit_greatest_id(size)
        elif color == Color.BLUE:
            select_bin = self._find_smallest_fit_least_id(size)
        elif color == Color.YELLOW:
            select_bin = self._find_smallest_fit_greatest_id(size)

        if select_bin is None:
            raise NoBinFoundException()
        else:
            #print(f"Selected bin {select_bin.bin_id} for object {object_id}")
            old_capacity = select_bin.remaining_capacity
            select_bin.add_object(new_object)
            select_bin.remaining_capacity -= size
            self.object_bin_mapping.insert(object_id, select_bin.bin_id)
            self._update_bin_tree(select_bin,old_capacity)
            

    def delete_object(self, object_id):
        bin_id = self.object_bin_mapping.search(object_id)
        if bin_id is None:
            return None

        obj = self.objects.search(object_id)
        bin_obj = self.bins_by_id.search(bin_id)
        old_capacity = bin_obj.remaining_capacity 
        bin_obj.remove_object(object_id)
        bin_obj.remaining_capacity += obj.size
        self.object_bin_mapping.delete(object_id)
        self.objects.delete(object_id)
        self._update_bin_tree(bin_obj,old_capacity)

    def bin_info(self, bin_id):
        bin_obj = self.bins_by_id.search(bin_id)
        return bin_obj.get_info()

    def object_info(self, object_id):
        bin_id = self.object_bin_mapping.search(object_id)
        return bin_id
    def _update_bin_tree(self, bin_obj, old_capacity):
        # Remove and reinsert bin based on updated capacity
        self.bins_by_capacity.delete((old_capacity, bin_obj.bin_id))
        
        self.bins_by_capacity.insert((bin_obj.remaining_capacity, bin_obj.bin_id), bin_obj)

        

    

    def _find_largest_fit_least_id(self, size):
        # Traverse the tree to find the largest bin with least ID that fits the object
        return self._find_fit(size, largest=True, by_id_least=True)

    def _find_largest_fit_greatest_id(self, size):
        # Traverse the tree to find the largest bin with greatest ID that fits the object
        return self._find_fit(size, largest=True, by_id_least=False)

    def _find_smallest_fit_least_id(self, size):
        # Traverse the tree to find the smallest bin with least ID that fits the object
        return self._find_fit(size, largest=False, by_id_least=True)

    def _find_smallest_fit_greatest_id(self, size):
        # Traverse the tree to find the smallest bin with greatest ID that fits the object
        return self._find_fit(size, largest=False, by_id_least=False)

    def _find_fit(self, size, largest=True, by_id_least=True):
        # Initialize best fitting bin variables
        self.best_fit_bin = None
        self.best_fit_capacity = None
        self.best_fit_bin_id = None
        # Start traversal
        if largest:
            self._find_largest_fit(self.bins_by_capacity.root, size, by_id_least)
        else:
            self._find_smallest_fit(self.bins_by_capacity.root, size, by_id_least)
        return self.best_fit_bin

    def _find_largest_fit(self, node, size, by_id_least=False):
        if node is None:
            return

        # Traverse the right subtree first for larger capacities
        self._find_largest_fit(node.right, size, by_id_least)
    
        cap, bin_id = node.key  # capacity and bin ID from the current node
    
        if cap >= size:
            # Compare the current bin's capacity with the best-fit bin
            if self.best_fit_bin is None:
                # If no best fit bin yet, set the current bin as the best fit
                self.best_fit_bin = node.obj
                self.best_fit_capacity = cap
                self.best_fit_bin_id = bin_id
                
            else:
                # If there's already a best fit bin, compare capacity and bin ID
                if cap > self.best_fit_capacity:
                    # Current bin has a larger capacity, so it's the new best fit
                    self.best_fit_bin = node.obj
                    self.best_fit_capacity = cap
                    self.best_fit_bin_id = bin_id
                    #print(f"Updated best fit to bin {bin_id} with larger capacity {cap}")
                elif cap == self.best_fit_capacity:
                    # If capacities are the same, compare by bin ID
                    if by_id_least:
                        # Choose the bin with the smaller ID
                        if bin_id < self.best_fit_bin_id:
                            self.best_fit_bin = node.obj
                            self.best_fit_bin_id = bin_id
                            #print(f"Tie in capacity, selecting bin {bin_id} with smaller ID")
                    else:
                        # Choose the bin with the larger ID (for Green cargo)
                        if bin_id > self.best_fit_bin_id:
                            self.best_fit_bin = node.obj
                            self.best_fit_bin_id = bin_id
                            #print(f"Tie in capacity, selecting bin {bin_id} with larger ID")

    # Now traverse the left subtree for smaller capacities
        self._find_largest_fit(node.left, size, by_id_least)


    def _find_smallest_fit(self, node, size, by_id_least):
        if node is None:
            return
        
        self._find_smallest_fit(node.left, size, by_id_least)
        cap, bin_id = node.key
        if cap >= size:
            if self.best_fit_bin is None or cap < self.best_fit_capacity or (cap == self.best_fit_capacity and ((by_id_least and bin_id < self.best_fit_bin_id) or (not by_id_least and bin_id > self.best_fit_bin_id))):
                self.best_fit_bin = node.obj
                self.best_fit_capacity = cap
                self.best_fit_bin_id = bin_id
        self._find_smallest_fit(node.right, size, by_id_least)