import node
import requests

class Compressor:

    """
    The compressor class creates a Huffman encoding tree of a given text document. 
    """

    def __init__(self, file):
        
        self.file = file
        self.frequencies = {}
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
                        
    
    
    
    def create_encoding(self):
        pass
    
    def get_encoding(self):