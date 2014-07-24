/*

www.fisicarduino.com
Criação de um Gauge usando Arduino e Processing
Autor: Marcelo Rocha
18/04/2014

*/

import processing.serial.*; // importa a biblioteca que dá acesso à porta serial

Serial myPort;  // Cria um objeto SerialPort
int val; // variável que recebe o dado vindo da serial port
int x_gauge, y_gauge, comp; // coordenadas do gráfico do ponteiro
PImage img; // objeto Imagem
float grau = 0; // variável grau

void setup() {
 size(290, 360); // define o tamanho da janela
 img = loadImage("gauge.png"); // carrega a imagem do Gauge
 x_gauge = 143;
 y_gauge = 140;
 comp = 80;
 String portName = Serial.list()[0]; // pega a primeira porta serial disponível e armazena em portName
 myPort = new Serial(this, portName, 9600); // inicializa a porta serial
}
void draw() {
  if ( myPort.available() > 0) {  // Se há algum dado disponivel,
    val = myPort.read();         // lê o dado e armazena em val
  }
  background(255); // define a cor de fundo
  stroke(153); // define a cor do traço do desenho
  grau = map(val, 0, 255, 0, 271); // mapeia os valores de entrada
  image(img, 20, 20); // posiciona a imagem do Gauge
  float radiano = ( PI * (225 - grau) ) / 180; // conersão para radianos
  
  // desenha o ponteiro
  line(x_gauge,y_gauge, x_gauge+comp*cos(radiano), y_gauge+comp*-(sin(radiano)));
  line(x_gauge-1,y_gauge-1, x_gauge+comp*cos(radiano), y_gauge+comp*-(sin(radiano)));
  line(x_gauge-2,y_gauge-2, x_gauge+comp*cos(radiano), y_gauge+comp*-(sin(radiano)));
}
