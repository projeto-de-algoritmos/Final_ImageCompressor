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
