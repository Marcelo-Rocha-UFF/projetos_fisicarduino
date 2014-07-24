/*
   Sensor LM35 - Nova Versao
   www.fisicarduino.com
   Por Marcelo Rocha
 */
 
const int inPin = 5; // entrada analógica para o sensor LM35
char comando = ' ';

void setup()
{
  Serial.begin(9600); // define a velocidade da comunicação serial
}


void loop()
{
  while(1)
  {
	int valor = analogRead(inPin); // coloca na variável valor a leitura do sensor
	float millivolts = (valor / 1024.0) * 5000;
	float celsius = millivolts / 10;  // sensor sai 10mV por grau Celsius
	if (Serial.available() > 0) {
          // Esvazia o buffer
          comando = Serial.read();
          if (comando=='L'){
            Serial.println(celsius); // envia para a porta serial a temp. em celsius ex.: 21.34 ( 5 bytes )
	    Serial.println( (celsius * 9)/ 5 + 32 );  //  converte de Celsius para Fahrenheit   
          }
        }
	delay(100); // pausa por 100ms
   }
}
