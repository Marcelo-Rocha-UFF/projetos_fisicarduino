# -*- coding: utf-8 -*-

###########################################################
#                                                         #
# Servo - Joystick PYGAME LINUX                           #
#                                                         #
# Código - FisicArduino.wordpress - www.Fisicarduino.com  #
#                                                         #
###########################################################

#obs1.: para rodar este programa e' preciso ter instalado as bibliotecas: pygame e pyserial
#obs2.: codigo feito para linux
# ficar atento, no caso de usar o codigo em outro sistema, para fazer a modificacoes necessarias. ex.:
# trocar /dev/ttyUSB0 por COMX e etc.

import pygame
import pygame.camera
import thread
import serial, sys
from pygame import locals

global fotos, soundcap, soundexit # variaveis globais
fotos = 0 # indice para os nome dos arquivos de imagem gerados

ser = serial.Serial("/dev/ttyUSB0",9600) # se conecta a porta e define a velocidade de comunicação
	
pygame.init() # inicialixa a pygame

# inicializacao necessaria para que possamos usar a parte de audio
# freq=44.1Khz, 16bits, 2 channels=Stereo (caracteristicas do arquivo de audio usado)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
screen = pygame.display.set_mode([400,400]) # define o tamanho da janela
pygame.camera.init() # inicializa a camera
cam_lista = pygame.camera.list_cameras() # cam_lista contem as cameras que estão no sistema

# lista as cameras disponiveis no sistema
for x in cam_lista:
	print "Cameras encontradas: " + x

# cria um objto camera com as seguintes caracteristicas:
# dispositivo: /dev/video0 (primeira camera encontrada no sistema)
# tamanho da imagem: 300,300
# tipo de imagem: RGB. Pode ser tambem: YUV ou HSV
cam = pygame.camera.Camera("/dev/video0",(300,300),"RGB")

cam.start() # inicia o funcionamento da camera
# associa as variaveis: souncap e soundexit aos arquivos de som
soundcap = pygame.mixer.Sound('camsound.ogg')
soundexit = pygame.mixer.Sound('plimplimsound.ogg')


pygame.joystick.init() # Inicializa o joystick

try:
	j = pygame.joystick.Joystick(0) # cria uma instancia do objeto joystick
	j.init() # inicializa o objeto
	print 'joystick encontrado: ' + j.get_name() # imprime o nome do joystick encontrado
	print 'Num de botoes: ' + str(j.get_numbuttons()) # imprime o numero de botoes
except pygame.error:
	print 'nenhum joystick encontrado' # erro! Joystick nao encontrado

def sair(): # Função que fecha a porta serial
	soundexit.play(loops=0, maxtime=0, fade_ms=0)
	ser.close() # Fecha a porta serial
	print('Fechando a porta serial...')
	exit(0) #sai

def captura_tela(): # função para a captura da tela da webcam
	global fotos, sound 
	soundcap.play(loops=0, maxtime=0, fade_ms=0) # toca o som da máquina fotografica
	fotos += 1 # valor usado no final do nome do arquivo de imagem
	arq_nome = 'captura' + str(fotos) + '.jpg' # cria o nome do arquivo. ex: captura1.jpg ou captura2.jpg
	pygame.image.save(tela,arq_nome) # salva a imagem da camera no hd usando o nome definido acima
	
def imagem(): # thread responsavel em ficar lendo e exibindo a imagem da camera
	while(1):
		global tela # e' uma Surface que recebe a imagem da camera
		tela = cam.get_image() # tela recebe a imagem  
		screen.fill([0,0,0]) # pinta a tela de preto
		screen.blit( tela, ( 25, 50 ) ) # desenha a imagem da camera na tela
		pygame.display.update() 
		pygame.display.flip() # faz um flip, trocando as imagens

# inicia uma thread com a funcao "imagem" responsavel pela captura da imagem da camera
thread.start_new_thread(imagem, ())


while 1:
	for e in pygame.event.get(): # percorre todos os eventos ocorridos. (tecla, joystick, mouse e etc.)
		if e.type == pygame.locals.JOYAXISMOTION: # evento num 7 - movimento do joystick
			x , y = j.get_axis(0), j.get_axis(1) # le as coordenadas dos eixos x e y do joy - Joy analogico
			# envia os valores de x e y para a porta serial, seguindo o protocolo pre-definido
			ser.write('x')
			ser.write(chr(int((x*100+100)*0.9))) # formula de ajuste de valores
			ser.write('y')
			ser.write(chr(int((y*100+100)*0.9))) # formala de ajuste de valores
		elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
			if j.get_button(0): sair() #0 e' o botao1
			if j.get_button(2): #2 e' o botao 3
				captura_tela() # chama a funcao que captura a tela
				print 'Imagem capturada'
