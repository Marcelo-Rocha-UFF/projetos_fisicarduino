##############################################################################################################
#                                                                                                            #
# Programa que controla uma webCAm usando dois servo motores que sao controlados pelo Arduino.               #
# O programa se comunica com o Arduino atraves da porta serial.                                              #
# A visualizacao da imagem da webCam e feita atraves de um programa na linguagem PROCESSING                  #
# Ha um trabalho em equipe das linguagens: PYTHON, C++ ( ARDUINO ) e PROCESSING                              #
# Muita atencao na hora de usar os fontes pois o codigo para o Arduino tem a mesma extensao para PROCESSING  #
# Autor: Marcelo Rocha - www.fisicarduino.com  Data 18-04-2014                                               #
#                                                                                                            #
##############################################################################################################

from Tkinter import * # Importa a biblioteca grafica
import serial # Importa o modulo para a comunicacao serial
import time # Importa a biblioteca para trabalhar com temporizacao

# Configuração da porta serial

ser = serial.Serial("COM3",9600); # Define porta e a velocidade de comunicação
print ser.portstr; # Imprime a porta em uso
print ('aguarde, incializando a porta...');
time.sleep(2); # Aguarda 2 segundos

# Obs. A variável valor é enviada pelo Scale implicitamente e contém o valor atual da posição do Scale
def servo_A(valor): # Funcão que envia o valor do Slide_A para o Servo_A, através da porta serial
   ser.write('a') # parte do protocolo de comunicação. Ex.: a100
   ser.write(chr(int(valor))) # Converte a variável valor de str para int e de int para char ( byte )

def servo_B(valor): # Funcão que envia o valor do slide A para o Servo_A, através da porta serial
   ser.write('b') # parte do protocolo de comunicação. Ex.: b100
   ser.write(chr(int(valor))) # Converte a variável valor de str para int e de int para char ( byte )

def clica_Move( event ):
   if (event.x >= 0 and event.x <=179): # Verifica se o mouse esta dentro dos limites do Canvas
      scale1.set(179 - event.x) # Envia os valores da posicao do mouse para o scale, e consequentemente chama a funcao servo_A 
      
   if (event.y >= 0 and event.x <=179): # Verifica se o mouse esta dentro dos limites do Canvas
      scale2.set(179 - event.y) # Envia os valores da posicao do mouse para o scale, e consequentemente chama a funcao servo_B
      
def sair(): # Função que destrói a Janela principal, antes fecha a porta serial
   ser.close() # Fecha a porta serial
   print('Fechando a porta serial...')
   time.sleep(1)
   print('Fechando a janela..')
   time.sleep(1)
   root.destroy() # Destrói a janela
  
# processo de criação da UI com TKinter

root = Tk() # Cria a janela
root.title('WebCam_Servo') # Define o títula da janela
root.geometry('380x290') # Define o tamanho da janela principal
Meu_Canvas = Canvas(root, width=180, height=180) # Cria um objeto tipo canvas e define o tamanho do Canvas
Meu_Canvas.place(x=30,y=30) # Posiciona o Canvas na janela pricipal


# Desenha o retangulo preto mais o grid ( Azul ) no Canvas

Meu_Canvas.create_rectangle(0, 0, 180, 180, fill="black")
coords = 1 # São 10 linhas horizontais e 10 verticais
while (coords <= 10): # conta de 1 até 10
   Meu_Canvas.create_line(0, 18*coords, 179, 18*coords, fill="blue") # linha horizontal
   Meu_Canvas.create_line(18*coords, 0, 18*coords, 179, fill="blue") # linha vertical
   coords = coords+1 # Mais uma linha, mais uma coluna

Meu_Canvas.bind("<B1-Motion>", clica_Move) # Anexa ao Meu_Canvas, a função que trata o clicar e arrastar do mouse sobre o Canvas

# Cria dois objetos Scale que pode variar de 0 a 179, e associa-o à função servo_A e servo_B respectivamente

# Pega os valores do scale1 e 
scale1 = Scale( root, from_=0, to=179, command = servo_A, width=15, length=179 )
scale1.place(x=250,y=30)
scale2 = Scale( root, from_=0, to=179, command = servo_B, width=15, length=179 )
scale2.place(x=310,y=30)

# Cria os Labels na tela.
label = Label(root, text='WEBCAM - Servo Controller - FisicArduino')
label.place(x=10, y=5) # Posiciona o label
label = Label(root, text='Y_Spin')
label.place(x=260, y=210) # Posiciona o label
label = Label(root, text='X_Spin')
label.place(x=320, y=210) # Posiciona o label

# Cria um objeto botão

b = Button(root, text ='     Exit     ', command = sair) # Anexa a funcao Sair a evento de clique do botao
b.place(x=90, y=240) # Posiciona o botao

root.mainloop() # Coloca o programa em execução
