// Controle WebCAm, com dois servo motores usando Python e TK
// www.fisicarduino.com
// Autor: Marcelo Rocha
// Data: 18-04-2014

#include <Servo.h> 

Servo servo_A, servo_B; // Cria dois objetos do tipo Servo.
int eixo =0 , bytelido = 0; // Cria duas variaveis do tipo int.

void setup (){
  Serial.begin(9600); // Configura a velocidade da comunicação serial.
  servo_A.attach(9); // Anexa o objeto x_servo ao pino 9 do arduino.
  servo_B.attach(10); // Anexa o objeto y_servo ao pino 10 do arduino.
  servo_A.write(0); // posiciona x_servo no angulo zero grau.
  servo_B.write(0); // posiciona y_servo no angulo zero grau.
}

void loop(){
    while (Serial.available() > 0){ // Enquanto houver algum byte na entrada serial.
      eixo = Serial.read(); //Lê um byte e armazena na variável eixo.
      if ( eixo == 'a' ) { // Verifica se eixo é igual ao caractere a.
        delay(10); // Espera 10ms
        bytelido = Serial.read(); // Como eixo igual a 'a', bytelido recebe o valor do 'slider a' da UI em python.
        servo_A.write(bytelido); // Passa para o servo_A o valor de bytelido.
      }
      if ( eixo == 'b' ) { // Verifica se eixo é igual ao caractere b.
        delay(10); // Espera 10ms
        bytelido = Serial.read(); // Como eixo igual a 'b', bytelido recebe o valor do 'slider b' da UI em python.
        servo_B.write(bytelido); // Passa para o servo_B o valor de bytelido.
      }  
    }
}

