import heapq
import itertools
#from compressor import node
from math import ceil
import node
import requests



class Compressor:

    """
    The compressor class creates a Huffman encoding tree of a given text document. 
    """

    def __init__(self, file, eof=None):
        
        self.file = file
        self.frequencies = {}
        self.tree = None
        self.encoding = {}
        self.decoding = {}
        self.eof = eof
        self.sortedEncoding = []
        self.minCw = {}
        self.cwToSymbol = {}

        
    
    def get_frequencies_file(self):
        
        """
        Scan through a file and count the occurences of each character.
        """
        
        with open(self.file, 'r', encoding='utf-8-sig') as f:
            for line in f:
                for char in line:
                    #char = char.encode('utf-8')
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
        self.create_canonical()
        self.create_decoding()
        
        
    def dfs(self, node, codeStr):
        """
        Perform a depth first traversal of the huffman tree and construct the codes for each of the leaves based on the path taken
        """
        oneKid = False
        if node.char:
            self.encoding[node.char] = codeStr
            
        if node.left:
            #We have visited on child 
            oneKid = True
            codeStr += '0'
            self.dfs(node.left, codeStr)

        if node.right:
            if oneKid:
                #We've already visited one child, so remove the last 0 added and put on a one
                codeStr = codeStr[:-1] + '1'
            
            else:
                #Otherwise we did not add a 0 already at this depth so proceed
                codeStr += '1'
            self.dfs(node.right, codeStr)
            
    def create_decoding(self):
        """
        Construct two lists which can be used to decode a canonical huffman encoding.
        The first list contains at index i the smallest numerical value of a codeword of length i
        The second list contains all the codewords of length i, sorted by their numerical value, smallest first 
        """
        
        
        #encodingIter = iter(self.sortedEncoding)
        
        for i in range(len(self.sortedEncoding)):
            char = self.sortedEncoding[i][0]
            code = self.sortedEncoding[i][1]
            codeLen = len(code)
            
            if codeLen in self.cwToSymbol:
                self.cwToSymbol[codeLen].append(char)
                
            else:
                #Because we are using a sorted list of encodings, the first code of 
                #any length is the minimum
                
                self.minCw[codeLen] = int(code, 2)
                self. cwToSymbol[codeLen] = [char]
        

    def create_canonical(self):
        """Convert the current encoding to a canonical one"""
        #First, convert the encoding to a list of tuples, and sort by code length
        
        encoding = [(k, v) for k, v in self.encoding.items()]
        encoding.sort(key=lambda x: (len(x[1]), x[1]))
        
        
        canonicalEncoding = {}
        sortedCEnc = []
        wordLengthCounts={}
        minCw = {}
        
        #Count the number of codewords of a given length
        maxCodeLength = len(encoding[-1][1])
        for i in range(1, maxCodeLength + 1):
            wordLengthCounts[i] = 0
            
        for item in encoding:
            length = len(item[1])
            wordLengthCounts[length] += 1
    
        #For each length, calculate the minimum codeword of that length
        
        self.minCw[maxCodeLength] = 0
        
        for i in range(maxCodeLength-1, 0, -1):
            self.minCw[i] = ceil((self.minCw[i+1] + wordLengthCounts[i+1])/2)
        
        
        #Now calculate the canonical huffman codes, and store them into the newEncoding dict
        #At the same time, add the characters into the cwToSymbol dict, grouping them together by their length, and 
        #the order they appear in the sorted list. This is crucial. Ordering the characters is what makes decoding
        #the canonical codes easy.
        
        #Initialize
        character = encoding[0][0]
        currentLength = len(encoding[0][1])
        currentCode = self.format_code(self.minCw[currentLength], currentLength)
        lengthNCodes = [character]
        canonicalEncoding[character] = currentCode

        
        #Calculate the new codes based on the first code created above
        for (character, code) in encoding[1:]:
            newLength = len(code)
            
            #Canonical Huffman codes for codewords of the same length are consecutive
            if currentLength == newLength:

                newCode = self.format_code(int(currentCode,2) + 1, currentLength)
                
                canonicalEncoding[character] = newCode    
                lengthNCodes.append(character)
                
                currentCode = newCode
                
            #We've found the first code of a new length    
            else:
                #The list comprehension below is copying lengthNCodes, so we can make changes to lengthNCodes without impacting
                #earlier values inserted into cwToSymbol
                self.cwToSymbol[currentLength] = [item for item in lengthNCodes]
                currentLength = newLength
                
                currentCode = self.format_code(self.minCw[currentLength], currentLength)
                canonicalEncoding[character] = currentCode
                lengthNCodes = [character]
        
        self.cwToSymbol[currentLength] = [item for item in lengthNCodes]
        self.encoding = canonicalEncoding
        self.sortedEncoding = sortedCEnc
    
    def encode(self):
        """
        Create an encoded file using an encoding previously generated by this object
        """
        
        
        bytes = []
        with open(self.file, 'r', encoding='utf-8-sig') as r:
            
            #Can this be done with a transform?
            bits = ''
            for line in r:
                
                #split the line into characters, perform the transformation, and join back 2getha
                bits += ''.join(map(lambda x:self.encoding[x], [char for char in line]))
        
        #add 0 padding to the end of the string  to make it a whole number of bytes
        
        padding = 8 - len(bits) % 8
        bits += '0' * padding
        
        
        #Get 8 chars from the encoded string, and convert this to a binary number
        bits = iter(bits)
        while(bits):
            byte = ''.join(list(itertools.islice(bits, 8)))
            if byte:
                byte = int(byte, 2)
                bytes.append(byte)
            else:
                break
               
        # Finished encoding the file, now write it
        with open ('encoded.bin', 'wb') as f:
            f.write(bytearray(bytes)) 
      
    def format_code(self, byte, length):
        """
        Format a byte from the compressed stream for decoding
        """               
        #Convert the binary into an integer
        #byte = int.from_bytes(byte, 'little')
        
        #Next convert that integer to a string
        byte = '{0:b}'.format(byte)
        
        #This conversion strips leading 0's, however we need them
        #If we have less than 8 bytes, pad the start with 0's
        
        """
        modulo = len(byte) % 8
        
        if modulo != 0:
            byte = '0' * (8-modulo) + byte
        """
        
        if len(byte) != length:
            byte = ('0' * (length - len(byte))) + byte
            
        return byte
    
    

        
    def decode(self, fName = 'encoded.bin'):
        """
        Decode a file according to the encoding contained in this compressor object
        """

        with open(fName, 'rb') as f:
            
            byte = f.read(1)
            byteFormatted = self.format_code(int.from_bytes(byte, 'little'), 8)
            
            idx = 0
            candidate = byteFormatted[idx]
            
            
            #while self.decoding.get(candidate, None) != self.eof:
            while True:
                
                while int(candidate, 2) < self.minCw.get(len(candidate)):
                    
                    #We still have bits that can be tried
                    if idx < len(byteFormatted) - 1:
                        idx += 1
                        
                    
                    #Need to read another byte from the file    
                    else:
                        byte = f.read(1)
                        byteFormatted = self.format_code(int.from_bytes(byte, 'little'), 8)
                        idx = 0
                        
                    candidate += byteFormatted[idx]
                        
                    
                #We have found a codeword. The difference between this codeword and the minimum codeword of the same length 
                #will be the index in cwToSymbol
                
                length = len(candidate)
                index = int(candidate, 2) - self.minCw[length]
                
                char = self.cwToSymbol[length][index]
                
                #DEBUGGING
                if char == 'e':
                    pass
                
                with open('decoded.txt', 'a', encoding='utf-8-sig') as d:
                    d.write(char)
                
                #Stop if we've written the end of the file
                if char == self.eof:
                    return
                    
                #Now that we've written a char, cleanup
                
                if idx < len(byteFormatted) - 1:
                    idx += 1
                
                else:
                    byte = f.read(1)
                    byteFormatted = self.format_code(int.from_bytes(byte, 'little'), 8)
                    idx = 0
                    
                candidate = byteFormatted[idx]
    
    
if __name__ == '__main__':
    
    c = Compressor('../tests/w&psample.txt', eof='$')
    c.get_frequencies_file()
    c.create_huffman_tree()
    c.parse_huffman_tree()
    c.encode()
    c.decode()
    