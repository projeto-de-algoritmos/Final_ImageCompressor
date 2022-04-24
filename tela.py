from huffman import HuffmanCoding
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import re
import numpy as np
from PIL import Image
import os

import customtkinter

def buscarArquivos():
    nomedoarquivo = filedialog.askopenfilename(initialdir="/",
                                          title="Selecione um arquivo",
                                          filetypes=(("Image files",
                                                      "*.jpg*"),
                                                     ("all files",
                                                      "*.*")))
    buscarArquivos.caminho = str(nomedoarquivo)



    pathh.insert(tk.END, nomedoarquivo)



def comprimirImagem():
    
    local = buscarArquivos.caminho
    
    h = 1
    if h == 1:
        
        string_entrada = np.asarray(Image.open(local), np.uint8)
        prnt = ("Local da imagem: " + local + "\n\n")

        text.insert(tk.END, prnt)
        shape = string_entrada.shape
        a = string_entrada
        print("Valores de entrada:", string_entrada)
        string_entrada = str(string_entrada.tolist())
    elif h == 2:
        array = np.arange(0, 737280, 1, np.uint8)
        string_entrada = np.reshape(array, (1024, 720))
        print("valores de entrada:", string_entrada)
        a = string_entrada
        string_entrada = str(string_entrada.tolist())

    else:
        print("Imagem invalida")  # tipo de imagem selecionada

    letras = []
    apenas_letras = []
    for letra in string_entrada:
        if letra not in letras:
            frequency = string_entrada.count(letra)  # Frequência de repetição de cada letra
            letras.append(frequency)
            letras.append(letra)
            apenas_letras.append(letra)

    nodes = []
    while len(letras) > 0:
        nodes.append(letras[0:2])
        letras = letras[2:]  # Classificando de acordo com a frequência
    nodes.sort()
    huffman_tree = []
    huffman_tree.append(nodes)  # Criando nós
