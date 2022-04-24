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

    def make_heap(self, frequencia):
        for chave in frequencia:
            node = self.HeapNode(chave, frequencia[chave])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while (len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def codificador_auxiliar(self, root, no_atual):
        if (root == None):
            return

        if (root.char != None):
            self.codes[root.char] = no_atual
            self.reverse_mapping[no_atual] = root.char
            return

        self.codificador_auxiliar(root.left, no_atual + "0")
        self.codificador_auxiliar(root.right, no_atual + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        codigo_atual = ""
        self.codificador_auxiliar(root, codigo_atual)

    def codificado(self, texto):
        encoded_text = ""
        for caracter in texto:
            encoded_text += self.codes[caracter]
        return encoded_text

    def bloco_codificado(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Texto codificado não organizado")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        nomearquivo, file_extension = os.path.splitext(self.path)
        caminho_saida = nomearquivo + ".bin"

        with open(self.path, 'r+') as file, open(caminho_saida, 'wb') as output:
            texto = file.read()
            texto = texto.rstrip()

            frequencia = self.cria_frequencia(texto)
            self.make_heap(frequencia)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.codificado(texto)
            padded_encoded_text = self.bloco_codificado(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        print("Comprimido")
        return caminho_saida

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decodifica_texto(self, encoded_text):
        codigo_atual = ""
        texto_decodificado = ""

        for bit in encoded_text:
            codigo_atual += bit
            if (codigo_atual in self.reverse_mapping):
                caracter = self.reverse_mapping[codigo_atual]
                texto_decodificado += caracter
                codigo_atual = ""

        return texto_decodificado

    def decompress(self, input_path):
        nomearquivo, file_extension = os.path.splitext(self.path)
        caminho_saida = nomearquivo + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(caminho_saida, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decodifica_texto(encoded_text)

            output.write(decompressed_text)

        print("Descomprimido")
        return caminho_saida
