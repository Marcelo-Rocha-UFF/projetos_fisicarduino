#!/usr/bin/python
# -*- coding: cp1252 -*-
####################################################################################                                                                                                          #
# Programa que controla dois servo motores, 2 leds e um buzzer usando o Arduino.
# O programa se comunica com o Arduino atraves da porta serial.  
# Este código recebe os comandos enviados pelo client.py através da rede
# 
# Autor: Marcelo Rocha www.fisicarduino.com
#
####################################################################################

import serial # Importa o modulo para a comunicacao serial
import time # Importa a biblioteca para trabalhar com temporizacao
from socket import *

# Configuração da porta serial

ser = serial.Serial("/dev/ttyUSB0", 9600); # Define porta e a velocidade de comunicação
print ser.portstr; # Imprime a porta em uso
print ('aguarde, incializando a porta...');
time.sleep(2); # Aguarda 2 segundos



s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 2124))
s.listen(1)
client, addr = s.accept()
print client, '\t', addr
client.send('Conexao estabelecida com o servidor, pronto para receber dados.')
while 1:
    #print 'Conectado com: ', client, ' no endereco: ', addr
    #time.sleep(0.5)
    data = client.recv(1024)
    if (data == '00'):  break
    ser.write(data)
    print data
client.send('Encerrando a conexao com o servidor, ate a proxima!')    
s.close()
ser.close()
print "O cliente encerrou a conexao!"
