# matplotlib Figure object
from matplotlib.figure import Figure

# import the GtkAgg FigureCanvas object, that binds Figure to
# GTKAgg backend. In this case, this is a gtk.DrawingArea
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas


import numpy as np

# gtk module
import gtk
import gobject

import serial; # importa o modulo para a comunicacao serial
import time # importa a biblioteca para trabalhar com temporizacao

ser = ""

tamanho = 100
i = 0
x = np.arange(tamanho)
y = np.arange(tamanho)

	

def conecta():
	global ser
	print "abrindo a porta serial..."
	ser = serial.Serial("/dev/ttyUSB0", 9600);  # abre a portal serial
	print "conexao feita com sucesso!"
	
def fecha():
	global ser
	print "...fechando a porta serial"
	ser.close()
	
	
def le_dados():
	global x, y, ser	
	y = np.delete(y, 0)
	y = np.append(y, int(ser.readline()))

def update_draw(*args):
	global x, y, i
	i = i + 1
	le_dados()
	l.set_data(x, y)
	fig.canvas.draw()
	#if i > 30:
	#	return False
	#else:
	#	time.sleep(0.1)
	#time.sleep(0.05)
	return True


# instantiate the GTK+ window object
win = gtk.Window()
# connect the 'destroy' signal to gtk.main_quit function
win.connect("destroy",gtk.main_quit)
# define the size of the GTK+ window
win.set_default_size(600, 400)
# set the window title
win.set_title("Monitor de Luminosidade - Usando MatPlotLib e Gtk")

# matplotlib code to generate the plot
fig = Figure(figsize=(6, 4), dpi=70)
ax = fig.add_subplot(111)
ax.set_ylim(20, 230)
ax.set_xlabel("Tempo de amostragem")
ax.set_ylabel("Intensidade da Luz")
ax.grid()

l, = ax.plot(x, y, label='Luz')
ax.legend()
# we bind the figure to the FigureCanvas, so that it will be
# drawn using the specific backend graphic functions
canvas = FigureCanvas(fig)
# add that widget to the GTK+ main window
win.add(canvas)

conecta()
# explicit update the graph (speedup graph visualization)
update_draw()

# exec our "updated" funcion when GTK+ main loop is idle
gobject.idle_add(update_draw)

# show all the widget attached to the main window
win.show_all()
# start the GTK+ main loop
gtk.main()

#fecha()
	


