from compressor.node import Node,merge
import unittest

class TestNodeMethods(unittest.TestCase):
    
    def setUp(self):
        self.node1 = Node(None, None, None, 'a', 1)
        self.node2 = Node(None, None, None, 'b', 2)
    
    def test_merge(self):
        node3 = merge(self.node1, self.node2)
        self.assertEqual(node3.weight, 3)
        self.assertEqual(node3.left, self.node1)
        self.assertEqual(node3.right, self.node2)
        self.assertEqual(self.node2.parent, node3)
        

if __name__ == '__main__':
    unittest.main()