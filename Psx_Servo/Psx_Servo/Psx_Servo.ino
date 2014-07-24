/*  PSX Controller Decoder Library (Psx.pde)
	Written by: Kevin Ahrendt June 22nd, 2008
	
	Controller protocol implemented using Andrew J McCubbin's analysis.
	http://www.gamesx.com/controldata/psxcont/psxcont.htm
	
	Shift command is based on tutorial examples for ShiftIn and ShiftOut
	functions both written by Carlyn Maw and Tom Igoe
	http://www.arduino.cc/en/Tutorial/ShiftIn
	http://www.arduino.cc/en/Tutorial/ShiftOut
*/

// www.fisicarduino.wordpress.com

#include <Servo.h> 
#include <WProgram.h> 
#include <Psx.h>      

#define dataPin 2 // nomeia o pino 2 como dataPin etc....
#define cmndPin 3
#define attPin 4
#define clockPin 5

#define LEDPin 13

Servo x_servo, y_servo; // Cria dois objetos do tipo Servo.

Psx Psx;                // inicializa a biblioteca

unsigned int data = 0;  // a variavel data armazena a resposta de controlador
float x = 1;
float y = 1;

void setup()
{
  
  // Define quais pinos serao usados
  // (Data Pin #, Cmnd Pin #, Att Pin #, Clk Pin #, Delay)
  // delay mede o relogio demora em cada estado,
  // medido em microsegundos.
  Psx.setupPins(dataPin, cmndPin, attPin, clockPin, 50);  
                                                          
  x_servo.attach(9); // Anexa o objeto x_servo ao pino 9 do arduino.
  y_servo.attach(10); // Anexa o objeto y_servo ao pino 10 do arduino.
  x_servo.write(0); // posiciona x_servo no angulo zero grau.
  y_servo.write(0); // posiciona y_servo no angulo zero grau.
  
  pinMode(LEDPin, OUTPUT);  // coloca o LEDPin com saida
}

void loop()
{
  data = Psx.read();    // Psx.read() inicia o controle e retorna os dados dos botoes
                                                          
  if (data & psxDown)
  {
    digitalWrite(LEDPin, HIGH); // se a o botao seta baixo e' pressionado, incrementa a variavel y e acende o led
    y+=0.4;
  } else if (data & psxUp)
  
  {
    digitalWrite(LEDPin, HIGH); // se a o botao seta cima e' pressionado, decrementa a variavel y e acende o led
   y-=0.4;
  } else if (data & psxLeft)
  {
    digitalWrite(LEDPin, HIGH); // se a o botao seta esquerda e' pressionado, decrementa a variavel x e acende o led
    x-=0.4;
  } else if (data & psxRight)
  {
    digitalWrite(LEDPin, HIGH); // se a o botao seta direita e' pressionado, incrementa a variavel x e acende o led
    x+=0.4;
  } else
  {
    digitalWrite(LEDPin, LOW); // se nenhum botao e' pressionado, apaga o led
  }

// limites 0 =< (x ou y) <=180 

if (y > 180) y=180; // impede que as variaveis assumam valores incompativeis com os servo motores
if (y < 0) y=0;
if (x > 180) x=180;
if (x < 0) x=0;

// envia os valores para os servo motores

x_servo.write(x);
y_servo.write(y);

// espera 10ms
delay(10);
}
