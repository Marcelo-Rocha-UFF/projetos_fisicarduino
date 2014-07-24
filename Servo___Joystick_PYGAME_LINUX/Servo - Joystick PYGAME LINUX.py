# -*- coding: utf-8 -*-

#######################################################
#                                                     #
# Servo - Joystick PYGAME LINUX                       #
#                                                     #
# Código - FisicArduino.wordpress - Fisicarduino.com  #
#                                                     #
#######################################################

import pygame
import serial, sys
from pygame import locals

ser = serial.Serial("/dev/ttyUSB0",9600) # Define porta e velocidade de comunicação
print ser.portstr # Imprime a porta em uso

def sair(): # Função que fecha a porta serial
   ser.close() # Fecha a porta serial
   print('Fechando a porta serial...')
   exit(0) #sai

   
pygame.init()

pygame.joystick.init() # main joystick device system


try:
   j = pygame.joystick.Joystick(0) # create a joystick instance
   j.init() # init instance
   print 'Enabled joystick: ' + j.get_name()
   print 'Num of buttons: ' + str(j.get_numbuttons())
except pygame.error:
   print 'no joystick found.'

while 1:
   for e in pygame.event.get(): # iterate over event stack
      print 'event : ' + str(e.type)
      if e.type == pygame.locals.JOYAXISMOTION: # 7
         x , y = j.get_axis(0), j.get_axis(1)
         ser.write('x')
         ser.write(chr(int((x*100+100)*0.9)))
         ser.write('y')
         ser.write(chr(int((y*100+100)*0.9)))
      #elif e.type == pygame.locals.JOYBALLMOTION: # 8
         #print 'ball motion'
      #elif e.type == pygame.locals.JOYHATMOTION: # 9
         #print 'hat motion'
      elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
         if j.get_button(0): sair()
         #print 'button down' + str(j.get_button(8))
      #elif e.type == pygame.locals.JOYBUTTONUP: # 11
         #print 'button up'
