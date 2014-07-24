/*

Este código faz com que o Arduino toque tons em frequências e ritmos
determinados pelos potenciômetros.
Usa dois alto falantes de 8 Ohms
Alternando a frequência em cada alto falante

www.fisicarduino.com
Autor: Marcelo Rocha
Data: 18-04-2014

 */

const int falante1 = 6;
const int falante2 = 7;

void setup() {

}

void loop() {
  int pot_duracao = analogRead(0); // entrada analógica 0 // pot. que controla a velocidade dos tons
  int duracao = map(pot_duracao, 0, 1023, 10, 450); // mapeia a entrada do pot. para durações de 10ms a 450ms
  int pot_freq = analogRead(2); // entrada analógica 2 // pot. que controla a freq. do ton
  int frequencia = map(pot_freq, 0, 1023, 100, 880); // mapeia a entrada do pot. para freq. de 100Hz a 800Hz 
  
  // toca a nota no alto falante 1
  tone(falante1, frequencia, duracao); // gera o som com as características acima
  delay(duracao); // pausa com a duração especificada

  // desliga o som no alto falante 1
  noTone(falante1); 
  
  // toca a nota no alto falante 2
  tone(falante2, 2 * frequencia, duracao); // gera o som com as características acima, sendo que com o dobro da frequencia
  delay(duracao); // pausa com a duração especificada
  
  // desliga o som no alto falante 2
  noTone(falante2);  


}
