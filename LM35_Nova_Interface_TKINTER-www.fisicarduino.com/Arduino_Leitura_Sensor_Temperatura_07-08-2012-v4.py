#!/usr/bin/python
# -*- coding: cp1252 -*-

from Tkinter import *
import tkMessageBox
from datetime import datetime
import thread
import time
import locale
import serial

locale.setlocale(locale.LC_ALL, ''); # Configurações do usuário
ser = serial.Serial('/dev/ttyUSB0', 9600);  # abre a portal serial. Obs. no Windows use comx (x igual ao n. da porta)
parar = False
x = 30
parar = False
lock = thread.allocate_lock()
ponto = 0
yc1 = yc2 = yf1 = yf2 = 0
cont = 1 # variável usado no processo de contagem
leituras = 10 # número de leituras a executar
# o intervalo entre as leituras é definido no soft. do Arduino

ser.flushInput(); # limpa o buffer da porta serial

time.sleep(2) # tempo para inicializacao

def desenha():
	grafico.create_rectangle(0, 0, 300, 150, fill='white')
	grafico.create_line(30,15,30,135, fill='black', width = 2) # eixo y
	grafico.create_line(15, 120, 290, 120, fill='black', width = 2) # eixo x
	for i in range(13):
		x = 30 + (i*20)
		grafico.create_line(x, 115,x,120, fill='black', width = 2)
	for i in range(10):
		y = 120 - (i*20)
		grafico.create_line(30, y,35,y, fill='black', width = 2)
	
	
    
def iniciar():
	global parar, lock
	botao_iniciar.config (state = "disable")
	botao_cancelar.config (state = "active")
	parar = False
	thread.start_new_thread(registra_dados, (lock,))

def cancelar():
	global parar
	botao_iniciar.config (state = "active")
	botao_cancelar.config (state = "disable")
	parar = True

def mostra_dados(lock):
	while(1):
		try: 
			global x, ponto, yc1, yc2, yf1, yf2
			c_label.config(text = '')
			f_label.config(text = '')
			time.sleep(.3)
			lock.acquire()
			ser.write('L') # envia o comando de leitura para o Arduino.
			Celsius = ser.readline(); # lê os bytes enviados pelo Arduino. ex: 21.34
			Fahrenheit = ser.readline(); # lê os bytes enviados pelo Arduino. ex: 75.30
			lock.release()			
			Celsius = Celsius.strip('\r\n')
			Fahrenheit = Fahrenheit.strip('\r\n')
			if ponto == 0:
				yc1 = Celsius
				yf1 = Fahrenheit
			if ponto == 1:
				yc2 = Celsius
				yf2 = Fahrenheit
				grafico.create_line(x, 120-float(yc1), x+8, 120-float(yc2), fill="blue")
				grafico.create_line(x, 120-float(yf1), x+8, 120-float(yf2), fill="red")

				x = x + 8
				ponto = -1
	
			c_label.config(text = Celsius)
			f_label.config(text = Fahrenheit)
			term_imagem.create_image(150,75, image=file)
			term_imagem.create_rectangle(85,97,99,97-float(Celsius), fill="blue", outline='blue')
			term_imagem.create_rectangle(200,120,214,160-float(Fahrenheit), fill="red", outline='red')
			term_imagem.create_text(60,97-float(Celsius),text = Celsius, fill = 'blue')
			term_imagem.create_text(91,140,text = 'Celsius', fill = 'blue')
			term_imagem.create_text(240,160-float(Fahrenheit),text = Fahrenheit, fill = 'red')
			term_imagem.create_text(207,140,text = 'Fahrenheit', fill = 'red')
			time.sleep(.7)
			
			ponto = ponto + 1
			
			if (x >= 280):
				x = 30
				desenha()
		except:
			pass

def registra_dados(lock):
	texto.delete(1.0, END)
	time.sleep(1)
	texto.insert(END, 'Leitura\tHora\tCelsius\tFahrenheit\n', ('titulo'))
	hoje = datetime.today();
	nome_file = 'Dia_' + str(hoje.strftime("%x")).replace('/','.') + '_Hora_' + str(hoje.strftime("%X")).replace(':','_') + '_log.txt'
	f = open(nome_file, 'w'); # cria arquivo para armazenar as leituras recebidas pela serial port
	f.write("Leitura de sensor de temperatura\n"); # escreve esta linha no arquivo
	f.write("-------------------------------------------\n"); # escreve esta linha no arquivo
	f.write("Leitura\t" + "Hora\t" + "Celsius\t" + "Fahrenheit\n"); # escreve esta linha no arquivo
	f.write("-------------------------------------------\n"); # escreve esta linha no arquivo

	global cont, parar
	num_l = num_leituras_entry.get()
	int_t = interval_tempo_entry.get()
	while (cont <= int(num_l) and not parar):
		try:
			lock.acquire()
			ser.write('L') # envia o comando de leitura para o Arduino.
			Celsius = ser.readline(); # lê os 5 bytes enviados pelo Arduino. ex: 21.34
			Fahrenheit = ser.readline(); # lê os 5 bytes enviados pelo Arduino. ex: 75.30
			lock.release()			
			Celsius = Celsius.strip('\r\n')
			Fahrenheit = Fahrenheit.strip('\r\n')
			# Obtém um datetime da data e hora atual
			hoje = datetime.today();
			hora = str(hoje.strftime("%X")); # armazena a hora atual na variável hora em formato string
			hora = hora[0:5]; # aproveita somente horas e minutos
			# \t = a um tab. \n = finaliza uma linha
			# escreve no arquivo: hora + tabulação + Celsius + tab. + Fahrenheit + finaliza linha
			st = '%s\t%s\t' % ( cont, hora )#, Celsius, Fahrenheit )	
					
			if (cont % 2 == 0):
				texto.insert(END, st, ('linhapar'))
				texto.insert(END, ' ' + Celsius + '\t', ('celsius', 'linhapar'))
				texto.insert(END, '  ' + Fahrenheit + '\n', ('fahrenheit', 'linhapar'))
			else:
				texto.insert(END, st, ('linhaimpar'))
				texto.insert(END, ' ' + Celsius + '\t', ('celsius', 'linhaimpar'))
				texto.insert(END, '  ' + Fahrenheit + '\n', ('fahrenheit', 'linhaimpar'))	
				
			st = '%s\t%s\t%s\t%s\n' % ( cont, hora , Celsius, Fahrenheit )
			print st
			f.write(st);
			# escreve na tela: hora + Celsius + Fahrenheit + finaliza linha
			time.sleep(float(int_t))
			cont = cont + 1;
		except:
			pass
	
	print "-------------------------------------------";    
	print "";
	print "Foram feitas %d leitura(s)!" % (cont-1);
	texto.insert(END, '\n', ('titulo'))
	cont = 1
	f.close() # fecha o arquivo
	botao_iniciar.config (state = "active")
	botao_cancelar.config (state = "disable")


root = Tk() # Cria a janela
root.title('LM35 - Interface Grafica - www.FisicArduino.com') # Define o títula da janela
root.geometry('780x520') # Define o tamanho
frame = Frame(root, bd=2, relief=FLAT)
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
texto = Text ( frame, height=20, width=45, yscrollcommand=scrollbar.set )
texto.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=texto.yview)

texto.tag_config("linhaimpar", background="cyan", foreground="black")
texto.tag_config("linhapar", background="white", foreground="black")
texto.tag_config("titulo", background="gray", foreground="black")
texto.tag_config("celsius", foreground="blue")
texto.tag_config("fahrenheit", foreground="red")

texto.pack()
frame.pack()
frame.place(x=365,y=140)

grafico = Canvas(root, width=300, height=150); # cria um objeto tipo canvas e define o tamanho do Canvas
grafico.place(x=30, y=140); # posiciona o canvas na janela pricipal
term_imagem = Canvas(root, width=300, height=150); # cria um objeto tipo canvas e define o tamanho do Canvas
term_imagem.place(x=30, y=315); # posiciona o canvas na janela pricipal
file = PhotoImage(file="termometro.gif") # no windows use "/termometro.gif"


desenha() 

label = Label(root, text='Temperatura em Celsius: ')
label.place(x=30, y=50)
label = Label(root, text='Temperatura em Fahrenheit: ')
label.place(x=30, y=70)
label = Label(root, text='Numero de Leituras: ')
label.place(x=460, y=50)
label = Label(root, text='Intervalo de tempo (s): ')
label.place(x=460, y=70)
label = Label(root, text='Grafico da Temperatura (C/F) X Tempo')
label.place(x=65, y=120) # 75

c_label = Label(root, text=''); # 185
c_label.place(x=205, y=50);
f_label = Label(root, text=''); # 
f_label.place(x=205, y=70);

botao_iniciar = Button(root, text ='Iniciar', command = iniciar )
botao_iniciar.place( x=460, y=100)
#botao_iniciar.pack() # Coloca o botão na janela

botao_cancelar = Button(root, text ='Cancelar', command = cancelar, state = "disable")
botao_cancelar.place( x=577, y=100)
#botao_parar.pack() # Coloca o botão na janela


# variaveis associadas aos componentes entry
num_leituras = StringVar() # variavel associada ao entry max
interval_tempo = StringVar() # variavel associada ao entry min
# inicializa os valores dos entry
num_leituras.set('5') 
interval_tempo.set('1')

num_leituras_entry = Entry(root, textvariable = num_leituras, width=5);
interval_tempo_entry = Entry(root, textvariable = interval_tempo, width=5);

num_leituras_entry.place(x=600, y=50); # Posiciona o entry
interval_tempo_entry.place(x=600, y=70); # Posiciona o entry


thread.start_new_thread(mostra_dados, (lock,))

root.mainloop() # Coloca o programa em execução

ser.close() # fecha a porta serial
