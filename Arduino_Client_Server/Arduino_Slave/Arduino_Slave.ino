// Controle WebCAm, com dois servo motores usando Python e TK

#include <Servo.h> 

Servo servo_A, servo_B; // Cria dois objetos do tipo Servo.
int eixo = 0 , bytelido = 0; // Cria duas variaveis do tipo int.
int leda = 22;
int ledb = 23;
int tone_port = 6;
boolean tone_state = false;
boolean leda_state = LOW;
boolean ledb_state = LOW;

void setup (){
	
  pinMode(leda, OUTPUT);
  pinMode(ledb, OUTPUT);
  Serial.begin(9600); // Configura a velocidade da comunicação serial.
  servo_A.attach(10); // Anexa o objeto x_servo ao pino 9 do arduino.
  servo_B.attach(11); // Anexa o objeto y_servo ao pino 10 do arduino.
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
      if (eixo == 'L'){
        delay(10);
        bytelido = Serial.read();
        if (bytelido == '1') digitalWrite(leda, leda_state = !leda_state);
        if (bytelido == '2') digitalWrite(ledb, ledb_state = !ledb_state);
      }  
      if (eixo == 'S'){
        tone_state = !tone_state;
        if (tone_state == true) tone(tone_port, 2000);
        if (tone_state == false) noTone(tone_port);
      }
  }
}

