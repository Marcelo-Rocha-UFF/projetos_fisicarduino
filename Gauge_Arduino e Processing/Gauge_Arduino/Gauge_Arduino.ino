/*

www.fisicarduino.com
Criação de um Gauge usando Arduino e Processing
Autor: Marcelo Rocha
18/04/2014

Este programa le um potenciômetro, mapeia essa leitura e envia os
valores para o programa feito em processing. Essa comunicação é
feita via porta serial. O software do Arduino também emite uma
frequência proporcional ao valor do potenciômetro.

*/

const int analogInPin = 0;  // pino para o potenciômetro
const int pino_buzzer = 7; // pino de conexão do buzzer

int sensorValue = 0;        // Variável que armazena o valor de entrada do potenciômetro
int outputValue = 0;        // Variável que armazena o valor a ser enviado para o Gauge

void setup() {
  // defina a veloc. da comunicação serial
  Serial.begin(9600); 
}

void loop() {
  // lê o valor do potenciômetro
  sensorValue = analogRead(analogInPin);            
  // mapeia o valor do sensor para os valores de saída
  outputValue = map(sensorValue, 0, 1023, 0, 255);  
  
  // envia o valor para a porta serial, isto é, para o programa em processing
  Serial.write(outputValue);   

  //envia valores de 50 Hz a 2Kz proporcionais aos valores enviados
  tone(pino_buzzer, map(outputValue,0,255,50,2000),100);
  delay(100); // espera 100ms  
  noTone(pino_buzzer);  // pausa o som
}
