import processing.serial.*;

Serial myPort;  // Create object from Serial class
int val;
int x_gauge, y_gauge, comp;
PImage img;
float grau = 0;

void setup() {
 size(290, 360);
 img = loadImage("gauge.png");
 x_gauge = 143;
 y_gauge = 140;
 comp = 80;
 String portName = Serial.list()[0];
 myPort = new Serial(this, portName, 9600);
}
void draw() {
  if ( myPort.available() > 0) {  // If data is available,
    val = myPort.read();         // read it and store it in val
  }
  background(255);
  stroke(153);
  grau = map(val, 0, 255, 0, 271);
  image(img, 20, 20);
  float radiano = ( PI * (225 - grau) ) / 180;
  line(x_gauge,y_gauge, x_gauge+comp*cos(radiano), y_gauge+comp*-(sin(radiano)));
  line(x_gauge-1,y_gauge-1, x_gauge+comp*cos(radiano), y_gauge+comp*-(sin(radiano)));
  line(x_gauge-2,y_gauge-2, x_gauge+comp*cos(radiano), y_gauge+comp*-(sin(radiano)));
}
