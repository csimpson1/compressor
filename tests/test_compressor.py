from compressor import compressor
import unittest

class TestCompressorMethods(unittest.TestCase):
    
    def setUp(self):
        self.comp = compressor.Compressor('sample.txt')
        
    def dfs(self, root):
        """
        Perform a depth first search on a huffman tree, return the list of leaf nodes
        """
        
        nodes = []
        stack = [root]
        
        while stack:
            node = stack.pop()
            
            if node.char:
                nodes.append(node)
            
            else:
                if node.left:
                    stack.append(node.left)
                    
                if node.right:
                    stack.append(node.right)
                    
        return nodes    
            
        
    
    def test_create_frequencies(self):
        self.comp.get_frequencies_file()
        keys = list(self.comp.frequencies.keys())
        keys.sort()
        
        self.assertEqual(keys, ['a','b', 'c', 'd', 'e'])
        
        self.assertEqual(self.comp.frequencies['a'], 4)
        self.assertEqual(self.comp.frequencies['b'], 2)
        self.assertEqual(self.comp.frequencies['c'], 5)
        self.assertEqual(self.comp.frequencies['d'], 2)
        self.assertEqual(self.comp.frequencies['e'], 1)
        
    def test_create_huffman_tree(self):
        self.comp.get_frequencies_file()
        self.comp.create_huffman_tree()
        
        leaves = self.dfs(self.comp.tree)
        leaves.sort(key=lambda x:x.char)
        leafChars = [x.char for x in leaves]
        self.assertEqual(leafChars, ['a', 'b', 'c', 'd', 'e'])
        
        aNode = leaves[0]
        bNode = leaves[1]
        cNode = leaves[2]
        dNode = leaves[3]
        eNode = leaves[4]

        self.assertEqual(bNode.parent, eNode.parent)
        self.assertEqual(bNode.parent.parent, dNode.parent)
        self.assertEqual(aNode.parent, cNode.parent)
        self.assertEqual(aNode.parent.parent, dNode.parent.parent)
        
        
    def test_parse_huffman_tree(self):
        
        self.comp.get_frequencies_file()
        self.comp.create_huffman_tree()
        self.comp.parse_huffman_tree()
        
        for node in self.comp.encoding:
            print(f'{node}, {self.comp.encoding[node]} ')
            
        
        
if __name__ == '__main__':
    unittest.main()