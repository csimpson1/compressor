import heapq
from compressor import node
import requests


class Compressor:

    """
    The compressor class creates a Huffman encoding tree of a given text document. 
    """

    def __init__(self, file):
        
        self.file = file
        self.frequencies = {}
        self.tree = None
        self.encoding = None
    
    def get_frequencies_file(self):
        
        """
        Scan through a file and count the occurences of each character.
        """
        
        with open(self.file, 'r') as f:
            for line in f:
                for char in line:
                    if char in self.frequencies:
                        self.frequencies[char] += 1
                        
                    else:
                        self.frequencies[char] = 1
                        
    def get_alphabet(self):
        """ Return a list consisting of the unique characters, or alphabet, seen in a given text"""
        
        return self.frequencies.keys()    
    
    def create_huffman_tree(self):
        """
        Create a tree representing the Huffman encoding for a given file. This function relies on the the frequencies distribution created by
        one of the get_frequencies functions
        """
        #Initialize the tree
        
        forest = []
        for frequency in self.frequencies.items():
            #frequency[0] is the char, frequency[1] is the count
            n= node.Node(None, None, None, frequency[0], frequency[1])
            heapq.heappush(forest, n)
            
        #Start combining trees
        while len(forest) > 1:
            candidate1 = heapq.heappop(forest)
            candidate2 = heapq.heappop(forest)
            print(f'c1:{candidate1.char} cd2:{candidate2.char}')
            tree = node.merge(candidate1, candidate2)
            heapq.heappush(forest, tree)
            
        #Now that we have a minimal tree, return it
        self.tree = heapq.heappop(forest)
    
    def parse_huffman_tree(self):
        """
        Return a dictionary where the keys are glyphs in the alphabet of a given document, and the
        values are the Huffman encoding in binary 
        """
        
        root = self.tree
        codeStr = ''
        self.dfs(root, codeStr)
        
        
    def dfs(self, node, codeStr):
        if node.char:
            self.encoding[node.char] = codeStr
            
        else:
            if node.left:
                codeStr += '0'
                self.dfs(node.left, codeStr)

            elif node.right:
                codeStr += '1'
                self.dfs(node.right, codeStr)
    
    
    def get_encoding(self):
        pass