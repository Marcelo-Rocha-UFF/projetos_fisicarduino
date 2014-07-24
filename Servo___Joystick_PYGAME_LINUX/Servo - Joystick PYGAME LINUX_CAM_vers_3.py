# -*- coding: utf-8 -*-

#######################################################
#                                                     #
# Servo - Joystick PYGAME LINUX                       #
#                                                     #
# Código - FisicArduino.wordpress - Fisicarduino.com  #
#                                                     #
#######################################################

import pygame
import pygame.camera
import thread
import serial, sys
from pygame import locals

global fotos
fotos = 0


ser = serial.Serial("/dev/ttyUSB0",9600) # Define porta e velocidade de comunicação
print "Porta serial: " + ser.portstr # Imprime a porta em uso
   
pygame.init()
screen = pygame.display.set_mode([400,400])
pygame.camera.init()
cam_lista = pygame.camera.list_cameras()

for x in cam_lista:
   print "Cameras encontradas: " + x
cam = pygame.camera.Camera("/dev/video0",(300,300),"HSV")
cam.start()
print cam.get_controls()
pygame.joystick.init() # main joystick device system

try:
   j = pygame.joystick.Joystick(0) # create a joystick instance
   j.init() # init instance
   print 'joystick encontrado: ' + j.get_name()
   print 'Num de botoes: ' + str(j.get_numbuttons())
except pygame.error:
   print 'nenhum joystick encontrado'

def sair(): # Função que fecha a porta serial
   ser.close() # Fecha a porta serial
   print('Fechando a porta serial...')
   exit(0) #sai

def captura_tela():
   global fotos
   print fotos
   fotos += 1
   arq_nome = 'captura' + str(fotos) + '.jpg'
   pygame.image.save(tela,arq_nome)
   
def imagem():
   while(1):
      global tela
      tela = cam.get_image()   
      screen.fill([0,0,0])
      screen.blit( tela, ( 25, 50 ) )
      pygame.display.update()
      pygame.display.flip()

thread.start_new_thread(imagem, ())


while 1:
   global incx, incy, graux, grauy
   incx = 0
   incy = 0
   graux = 0
   grauy = 0
   for e in pygame.event.get(): # iterate over event stack
      #print 'event : ' + str(e.type)
      if e.type == pygame.locals.JOYAXISMOTION: # 7
         x , y = j.get_axis(0), j.get_axis(1)
         graux += x
         grauy += y
         if graux < 0 : graux = 0
         if graux > 179 : graux = 179
         if grauy < 0 : grauy = 0
         if grauy > 179 : grauy = 179
         print graux, x
         ser.write('x')
         ser.write(chr(int(graux)))
         ser.write('y')
         ser.write(chr(int(grauy)))
      #elif e.type == pygame.locals.JOYBALLMOTION: # 8
         #print 'ball motion'
      #elif e.type == pygame.locals.JOYHATMOTION: # 9
         #print 'hat motion'
      elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
         if j.get_button(0): sair() #0 e' o botao1
         if j.get_button(2):
            captura_tela() #2 e' o botao 3
            print 'Imagem capturada'
         #print 'button down' + str(j.get_button(8))
      #elif e.type == pygame.locals.JOYBUTTONUP: # 11
         #print 'button up'
