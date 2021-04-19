class Node:
    
    """
    The Node class is used to make the trees used as a part of the Huffman encoding algorithm.
    An instance of the Node class has the following propertoes
    
    parent : The parent node of this node
    left   : The left child node of this node
    right  : The right child node of this node
    char   : The character assigned to this node
    weight : The weight of the subtree rooted at this node
     
    """
    
    def __init__(self, parent, left, right, char, weight):
        self.parent = parent
        self.left = left
        self.right = right
        self.char = char
        self.weight = weight
        

def merge(node1, node2):
    """
    Take two trees and return one that has the two trees past as 
    children, and a weight which is the sum of the weights of the two child trees
    """
    
    return Node(None, node1, node2, None, node1.weight + node2.weight)