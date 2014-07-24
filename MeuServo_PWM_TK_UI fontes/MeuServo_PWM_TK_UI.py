########################################################################
#                                                                      #
# www.fisicarduino.com                                                 #                                                                     #
# Programa para controle de dois servo motores ( x_servo e y_servo )   #
# Autor: Marcelo Rocha                                                 #
# Data: 18-04-2014                                                     #
# Se comunica com o arduino através da porta serial                    #
# Protocolo simples de comunicação: ( byte_servo + valor do slider )   #
# Exemplo x100 ( Envia o valor 100 para x_servo )                      #
#                                                                      #
########################################################################

from Tkinter import *
import serial
import time

# Configuração da porta serial

ser = serial.Serial("COM3",9600); # Define porta e velocidade de comunicação
print ser.portstr; # Imprime a porta em uso
print ('aguarde, incializando a porta...');
time.sleep(3); # Aguarda 3 segundos

def y_axis(valor): # Funcão que envia o valor do slide Y para a porta serial
   ser.write('y')
   ser.write(chr(int(valor))) # Converte a variável valor de str para int e de int para char ( byte )

def x_axis(valor): # Funcão que envia o valor do slide X para a porta serial
   ser.write('x')
   ser.write(chr(int(valor))) # Converte a variável valor de str para int e de int para char ( byte )

def sair(): # Função que destrói a Janela principal, antes fecha a porta serial
   ser.close() # Fecha a porta serial
   print('Fechando a porta serial...')
   time.sleep(1)
   print('Fechando a janela..')
   time.sleep(1)
   root.destroy() # Destrói a janela

# processo de criação da UI com TKinter

root = Tk() # Cria a janela
root.title('Servo Motor Arduino Control') # Define o títula da janela
root.geometry('280x280') # Define o tamanho

# Cria um objeto Scale que pode varia de 0 a 179, e associa-o à função y_axis

scale = Scale( root, from_=0, to=179, command = y_axis, width=9, length=179 )
scale.pack(anchor=CENTER) # Coloca o Scale na janela

# Cria um objeto Scale ( Horizontal ) que pode varia de 0 a 179, e associa-o à função x_axis

scale = Scale( root, from_=0, to=179, command = x_axis, width=9, length=179, orient=HORIZONTAL )
scale.pack(anchor=CENTER) # Coloca o Scale na janela

# Cria um objeto botão
b = Button(root, text ='Exit', command = sair)
b.pack() # Coloca o botão na janela

root.mainloop() # Coloca o programa em execução
