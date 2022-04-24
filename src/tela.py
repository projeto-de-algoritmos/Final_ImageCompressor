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


    def combine_nodes(nodes):
        pos = 0
        newnode = []
        if len(nodes) > 1:
            nodes.sort()
            nodes[pos].append("1")  # determinando valores 1 ou 0
            nodes[pos + 1].append("0")
            combined_node1 = (nodes[pos][0] + nodes[pos + 1][0])
            combined_node2 = (nodes[pos][1] + nodes[pos + 1][1])  # combinando os nos
            newnode.append(combined_node1)
            newnode.append(combined_node2)
            newnodes = []
            newnodes.append(newnode)
            newnodes = newnodes + nodes[2:]
            nodes = newnodes
            huffman_tree.append(nodes)
            combine_nodes(nodes)
        return huffman_tree  # Gerando arvore huffman


    newnodes = combine_nodes(nodes)

    huffman_tree.sort(reverse=True)
    print("Arvore de huffman:")

    checklist = []
    for level in huffman_tree:
        for node in level:
            if node not in checklist:
                checklist.append(node)
            else:
                level.remove(node)
    count = 0
    for level in huffman_tree:
        print("Nivel", count, ":", level)  # printa huffman arvore
        count += 1
    print()

    letra_binario = []
    if len(apenas_letras) == 1:
        letracode = [apenas_letras[0], "0"]
        letra_binario.append(letra_code * len(string_entrada))
    else:
        for letra in apenas_letras:
            code = ""
            for node in checklist:
                if len(node) > 2 and letra in node[1]:  # gerando codigo binário
                    code = code + node[2]
            letracode = [letra, code]
            letra_binario.append(letracode)
    print(letra_binario)
    print("Arquivo binario gerado:")
    for letra in letra_binario:
        print(letra[0], letra[1])

    bitstring = ""
    for character in string_entrada:
        for item in letra_binario:
            if character in item:
                bitstring = bitstring + item[1]
    binary = "0b" + bitstring
    print("Arquivo binario:")
    # código binário gerado

    uncompressed_file_size = len(string_entrada) * 7
    compressed_file_size = len(binary) - 2
    print("Tamanho do arquivo original", uncompressed_file_size, "bits. O tamanho do arquivo comprimido, e:",
        compressed_file_size)
    print("Salvando arquivo em: ", uncompressed_file_size - compressed_file_size, "bits")
    output = open("comprimido.txt", "w+")
    print("Arquivo comprimido gerado.txt")
    output = open("comprimido.txt", "w+")
    print("Decodificando.......")
    output.write(bitstring)

    bitstring = str(binary[2:])
    uncompressed_string = ""
    code = ""
    for digit in bitstring:
        code = code + digit
        pos = 0  # decodificando
        for letra in letra_binario:
            if code == letra[1]:
                uncompressed_string = uncompressed_string + letra_binario[pos][0]
                code = ""
            pos += 1

    print("Arquivo descomprimido, e:")
    if h == 1:
        temp = re.findall(r'\d+', uncompressed_string)
        res = list(map(int, temp))
        res = np.array(res)
        res = res.astype(np.uint8)
        res = np.reshape(res, shape)
        print(res)
        print("")
        print("Entrada Dimensao:", shape)
        print("Saída Dimensao:", res.shape)
        data = Image.fromarray(res)
        data.save('imagem descomprimida.png')
        if a.all() == res.all():
            print("Sucesso!")
    if h == 2:
        temp = re.findall(r'\d+', uncompressed_string)
        res = list(map(int, temp))
        print(res)
        res = np.array(res)
        res = res.astype(np.uint8)
        res = np.reshape(res, (1024, 720))
        print(res)
        data = Image.fromarray(res)
        data.save('imagem descomprimida.png')
        print("Descomprimida com sucesso")

# Comprimir
def compress():

    local = buscarArquivos.caminho

    h = HuffmanCoding(local)
    compress.output_path = h.compress()

    prnt = ("Local de descompressão: " + compress.output_path + "\n\n")

    text.insert(tk.END, prnt)

# Limpar caixa de texto
def limpar():
    text.delete('1.0', END)

new_c = "forestgreen"


#----Nome da Janela-----#
root = customtkinter.CTk()
root.title("Compressor de Texto")


# ---Wirgets da aplicação---#
mainframe = customtkinter.CTkFrame(root)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)




#----Menu----#
root.option_add('*tearOff', FALSE)

menubar = Menu(root)
root.config(menu=menubar)

menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Arquivo')
menubar.add_cascade(menu=menu_edit, label='Editar')

menu_file.add_command(label='Novo')

menu_file.add_command(label='Fechar', command=root.destroy)

menu_edit.add_command(label='Copiar')
menu_edit.add_command(label='Colar')


#--Selecionar o arquivo---#
select_file_label = customtkinter.CTkLabel(mainframe,
                                            text="Local do arquivo selecionado:",
                                            width=200,
                                            height=50,
                                            fg_color=None)
select_file_label.grid(row=0, column=0, pady=10, padx=30, sticky=(W))

pathh = customtkinter.CTkEntry(mainframe, width=240)
pathh.grid(row=0, column=1, columnspan=2, pady=5, padx=10, sticky=())

select_file_btn1 = customtkinter.CTkButton(mainframe,
                                            text="Selecione um Arquivo",
                                           command=buscarArquivos,
                                            fg_color=None,
                                            border_width=2,
                                            border_color=new_c,
                                            hover_color=new_c)
select_file_btn1.grid(row=0, column=3, pady=5, padx=10)



#--Selecionar a ação de Comprimir e descomprimir--#
select_audit_label = customtkinter.CTkLabel(mainframe,
                                            text="Selecione uma ação:",
                                            height=50,
                                            width=200,
                                            fg_color=None)
select_audit_label.grid(row=1, column=0, pady=10, padx=30, sticky=(W))



#--Opções--#
mob_btn = customtkinter.CTkButton(mainframe,
                                  text="Processar imagem",
                                  command=comprimirImagem,
                                  fg_color=None,
                                  border_width=2,
                                  border_color=new_c,
                                  hover_color=new_c)
mob_btn.grid(row=1, column=1, pady=5, padx=10, sticky=())


#-- Botões ---#

text = tk.Text(mainframe, wrap=WORD, height=30, width=100)
text.grid(row=2, column=0, columnspan=5, padx=35, pady=20)

clear_btn = customtkinter.CTkButton(mainframe,
                                    text="Limpar",
                                    command=limpar,
                                    fg_color=None,
                                    border_width=2,
                                    border_color=new_c,
                                    hover_color=new_c)
clear_btn.grid(row=4, column=4, pady=20, padx=10)




root.mainloop()