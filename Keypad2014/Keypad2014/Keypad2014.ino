/*
Este projeto usa um keypad para receber uma senha e desbloquear uma entrada.
Esta entrada pode ser um relé, pode ser uma fechadura eletrônica.
Ao iniciar o projeto o led vermelho indica que a entrada está bloqueada.
Para entrar com a senha (3 dígitos) deve-se apertar a tecla #
Após isso o led amarelo acende e aguarda a entrada da senha.
Se a senha estiver errada o led volta a ficar vermelho bloqueando a entrada.
Se a senha estiver correta o led verde fica piscando indicando a liberação da entrada

www.fisicarduino.com
Autor: Marcelo Rocha
Data: 18-04-2014
 
*** Lembre-se de colocar a library Keypad na pasta arduino/libraries

*/

#include <Keypad.h> // library Keypad

int count = 0;
char pass [3] = {'1', '2', '3'}; // define a senha

const int greenPin = 10; // pino para o Led verde
const int yellowPin = 11; // pino para o Led amarelo
const int redPin = 12; // pino para o Led vermelho

const int audioPin = 9; // pino da saída de som, a ser ligado no buzzer
const int duration = 200; // pausa do bip sonoro

// configuração do keypad
const byte ROWS = 4; // Quatro linhas
const byte COLS = 3; // Três colunas

char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = {2, 3, 4, 5}; // conecte as saídas das linha do keypad
byte colPins[COLS] = {6, 7, 8}; // conecte as saídas das colunas do keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup(){
  pinMode(audioPin, OUTPUT); // configura os pinos digitas como saída
  pinMode(yellowPin, OUTPUT); //
  pinMode(redPin, OUTPUT); //
  pinMode(greenPin, OUTPUT); //
  key_init(); // inicializa o keypad
}

void loop(){
  char key = keypad.getKey(); // espera que uma tecla seja digitada
  if (key != NO_KEY)
  {
    if (key == '#') // se # então vai para o modo de entrada de senha
    { 
      code_entry_init(); // rotina que acende o led amarelo
      int entrada = 0;
      while (count < 3 ) // espera até que seja digitado 3 caracteres
      {
        char key = keypad.getKey();
        if (key != NO_KEY)
        {
          entrada += 1;
          tone(audioPin, 1080, 100); // sinal sonoro de tecla digitada
          delay(duration);
          noTone(audioPin);
          if (key == pass[count]) count += 1; // verifica se a tecla digitada equivale ao um dígito da senha
          if ( count == 3 ) unlocked(); // se estiver correta, chama a rotina de desbloqueio
          if ((key == '#') || (entrada == 3)) // se # ou senha inválida, inicia tudo de novo
          {
            key_init(); 
            break;
          }
        }
      }
    }
  }
}

void key_init (){ // rotina de inicialização (Led vermelho)
  count = 0;
  digitalWrite(redPin, HIGH);
  digitalWrite(yellowPin, LOW);
  digitalWrite(greenPin, LOW);
  tone(audioPin, 1080, 100);
  delay(duration);
  noTone(audioPin);
  tone(audioPin, 980, 100);
  delay(duration);
  noTone(audioPin);
  tone(audioPin, 770, 100);
  delay(duration);
  noTone(audioPin);
}

void code_entry_init(){ // rotina de entrada de senha (Led amarelo)
  count = 0;
  tone(audioPin, 1500, 100);
  delay(duration);
  noTone(audioPin);
  tone(audioPin, 1500, 100);
  delay(duration);
  noTone(audioPin);
  tone(audioPin, 1500, 100);
  delay(duration);
  noTone(audioPin);
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, HIGH);
  digitalWrite(greenPin, LOW);
}

void unlocked(){ // rotina de desbloqueio (Led verde)
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, LOW);
  while ( true ){ // loop infinito, pressione o reset do arduino para reiniciar
    digitalWrite(greenPin, HIGH);
    tone(audioPin, 2000, 100);
    delay(duration);
    noTone(audioPin);
    digitalWrite(greenPin, LOW);
    tone(audioPin, 2000, 100);
    delay(duration);
    noTone(audioPin);
  }
}
