import heapq
import os

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # definir comparadores
        def __lt__(self, outro):
            return self.freq < outro.freq

        def __eq__(self, outro):
            if (outro == None):
                return False
            if (not isinstance(outro, HeapNode)):
                return False
            return self.freq == outro.freq

    # funções para comprensão:

    def cria_frequencia(self, texto):
        frequencia = {}
        for caracter in texto:
            if not caracter in frequencia:
                frequencia[caracter] = 0
            frequencia[caracter] += 1
        return frequencia
