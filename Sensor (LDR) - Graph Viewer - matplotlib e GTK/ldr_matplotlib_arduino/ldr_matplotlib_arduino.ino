// Sensor (LDR) - Graph - Viewer
// www.fisicarduino.com
// Autor: Marcelo Rocha
// Data: 18-04-2014

const int analogInPin = 0;  // entrada que recebe a saido do divisor de tensao

int sensorValue = 0;
int outputValue = 0;

void setup() {
  // inicializa a comunicacao serial com a velocidade de 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  // le a entrada analogica
  sensorValue = analogRead(analogInPin);            
  // mapeia o intervalo de saida
  outputValue = map(sensorValue, 0, 1023, 20, 230);  
           
  // envia o valor da variavel para a porta serial   
  Serial.print(outputValue);
  // envia o caracter 'nova linha' para a porta serial
  Serial.print('\n');  
  
  digitalWrite(13,LOW); // apaga o led ligada ao pino 13
  delay(100); // aguarda 10ms
  digitalWrite(13,HIGH);   // acende o led
}
