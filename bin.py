from avl import AVLTree
class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.objects_tree = AVLTree(self._compare_objects)

    def _compare_objects(self, node_1, node_2):
        return (node_1.key > node_2.key) - (node_1.key < node_2.key)

    def add_object(self, obj):
        if obj.size > self.remaining_capacity:
            return None
        self.objects_tree.insert(obj.object_id, obj)
        #no updating capacity here

    def remove_object(self, object_id):
        obj = self.objects_tree.search(object_id)
        if obj is None:
            return None
        self.objects_tree.delete(object_id)
        return obj.size
    def _get_total_sum_objects(self):
        return sum([obj.obj.size for obj in self.objects_tree.in_order_traversal()])

    def get_info(self):
        return self.remaining_capacity, [node.key for node in self.objects_tree.in_order_traversal()]
    
