#!/usr/bin/python
# -*- coding: cp1252 -*-
####################################
#
# www.fisicarduino.com
# Autor: Marcelo Rocha
# Data: 18-04-2014
#
####################################

from Tkinter import * # importa a biblioteca grafica
import thread;
import serial; # importa o modulo para a comunicacao serial
import time # importa a biblioteca para trabalhar com temporizacao

ser = serial.Serial("COM3", 9600);  # abre a portal serial

# variaveis globais

# vetor de 200 posicoes
num_elementos = 200;
luz = ser.readline(); # faz a leitura da porta. ex: 123\n
luz = luz.strip('\n'); # remove o caracter \n (escape code - line feed) vindo do arduino
fila = [luz for i in range(num_elementos)]; # enche com valores iguais a zero
indices_x = [2*x for x in range(num_elementos/2)];
  
def works(num_elementos, fila) : # funcao que desenha o grafico e le os dados da porta serial 
    loop = 6; # variavel usada na contagem abaixo
    while 1:
        # desenha grafico
        if (loop<1): # evita que o grafico seja desenhado a cada leitura da porta, melhorando assim a performance
            loop = 6; # frequencia de atualizacao do grafico
            max_var.set(max(fila));
            min_var.set(min(fila));
            grafico.create_rectangle(0, 0, (2*num_elementos+2), 230, fill='white'); 
            grafico.create_line(5,0,5,230, fill="black", width="2", arrow="first"); 
            grafico.create_line(0,225,400,225, fill="black", width="2", arrow="last"); 
            for x in range(num_elementos-2):            
                grafico.create_line(2*x+5, 230-int(fila[x]), (2*x)+7, 230-int(fila[x+1]), fill="blue");   
        else:
            loop-=1;
            
        # le porta serial
        luz = ser.readline(); # faz a leitura da porta. ex: 123\n
        luz = luz.strip('\n'); # remove o caracter \n (escape code - line feed) vindo do arduino
        
        # converte o valor lido em um valor que o representara no grafico
        # executa FIFO (first in is first out)
        fila = fila[1:num_elementos]; # retira o primeiro elemento da fila
        # acrescenta a ultima leitura no fim da fila
        fila.append(luz);
        # espera algun tempo
        instant_var.set(luz);  

# desenha a interface grafica

root = Tk(); # cria a janela
root.title('Sensor (LDR) - Graph Viewer - FisicArduino'); # define o titula da janela
root.geometry('580x310'); # define o tamanho da janela principal
grafico = Canvas(root, width=2*num_elementos+7, height=230); # cria um objeto tipo canvas e define o tamanho do Canvas
grafico.place(x=50, y=30); # posiciona o canvas na janela pricipal
l_x = Label(root, text="Tempo (200ms)"); # desenha e posiciona os labels
l_x.place(x=210, y=265);
l_y = Label(root, text="Luz(*)");
l_y.place(x=10, y=30);

# variaveis associadas aos componentes entry

max_var = StringVar(); # variavel associada ao entry max
min_var = StringVar(); # variavel associada ao entry min
instant_var = StringVar(); # variavel associada ao entry instant

# inicializa os valorese dos entry
max_var.set(''); 
min_var.set('');
instant_var.set('');

# cria os entry components com as variaveis associadas

max_entry = Entry(root, textvariable=max_var, width=15);
min_entry = Entry(root, textvariable=min_var, width=15);
instant_entry = Entry(root, textvariable=instant_var, width=15);

# cria os labels

l_max = Label(root, text="Valor Maximo");
l_min = Label(root, text="Valor Minimo");
l_instant = Label(root, text="Valor instantaneo");

# posiciona labels e entrys na tela

l_max.place(x=470, y=69);
l_min.place(x=470, y=119);
l_instant.place(x=470, y=169);
max_entry.place(x=470, y=90); # Posiciona o entry
min_entry.place(x=470, y=140); # Posiciona o entry
instant_entry.place(x=470, y=190); # Posiciona o entry

# coloca a funcao work para funcionar como um processo independente

thread.start_new_thread(works, (num_elementos, fila)); # le a porta serial e desenha os graficos

root.mainloop() # coloca o programa em execução
