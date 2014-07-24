/*
 * Controle de quatro servo motores usando Python e TK
 * 
 * O ideal é que a alimentação dos motores de seja feita por uma fonte externa 
 * que seja capaz de fornecer a corrente necessária.
 * 
 * www.fisicarduino.com
 * utor: Marcelo Rocha
 * Data: 18-04-2014
 * 
*/
#include <Servo.h> 

Servo servo_A, servo_B, servo_C, servo_D; // Cria dois objetos do tipo Servo.
int eixo =0 , bytelido = 0; // Cria duas variaveis do tipo int.

void setup (){
  Serial.begin(9600); // Configura a velocidade da comunicação serial.
  servo_A.attach(9); // Anexa o objeto x_servo ao pino 9 do arduino.
  servo_B.attach(10); // Anexa o objeto y_servo ao pino 10 do arduino.
  servo_C.attach(11);
  servo_D.attach(12);
  servo_A.write(0); // posiciona servo a no angulo de zero grau.
  servo_B.write(0); // posiciona servo b no angulo de zero grau.
  servo_C.write(0); // posiciona servo c no angulo de zero grau.
  servo_D.write(0); // posiciona servo d no angulo de zero grau.
}

void loop(){
    while (Serial.available() > 0){ // Enquanto houver algum byte na entrada serial.
      eixo = Serial.read(); //Lê um byte e armazena na variável eixo.
      if ( eixo == 'a' ) { // Verifica se eixo é igual ao caractere a.
        delay(10); // Espera 10ms
        bytelido = Serial.read(); // Como eixo igual a 'a', bytelido recebe o valor do 'slider a' da UI em python.
        servo_A.write(bytelido); // Passa para o servo a o valor de bytelido.
      }
      if ( eixo == 'b' ) { // Verifica se eixo é igual ao caractere b.
        delay(10); // Espera 10ms
        bytelido = Serial.read(); // Como eixo igual a 'b', bytelido recebe o valor do 'slider b' da UI em python.
        servo_B.write(bytelido); // Passa para o servo b o valor de bytelido.
      }
      if ( eixo == 'c' ) { // Verifica se eixo é igual ao caractere c.
        delay(10); // Espera 10ms
        bytelido = Serial.read(); // Como eixo igual a 'c', bytelido recebe o valor do 'slider c' da UI em python.
        servo_C.write(bytelido); // Passa para o servo c o valor de bytelido.
      }
      if ( eixo == 'd' ) { // Verifica se eixo é igual ao caractere d.
        delay(10); // Espera 10ms
        bytelido = Serial.read(); // Como eixo igual a 'd', bytelido recebe o valor do 'slider d' da UI em python.
        servo_D.write(bytelido); // Passa para o servo d o valor de bytelido.
      }  
    }
}

