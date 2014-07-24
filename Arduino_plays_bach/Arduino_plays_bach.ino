/*
 Arduino Plays Bach - Prelude in C
 
 Este código mostra como conectar um dispositivo midi ao Arduino.
 Através da porta serial, o Arduino envia informação (protocolo midi) de (note on) e (note off) para o módulo de som.
 Note on (tecla do teclado pressionada) e note off (momento em que a tecla deixa de ser pressionada).
 Assim é possível controlar qualquer dispositivo midi. Ex.: Baterias eletrônicas, Teclados e através de uma interface 
 midi, conectada ao computador, controlar VSTs.
 
 O Circuito:
 * Entrada do pino digital 1 é conectada ao pino 5 do cabo midi (macho).
 * Pino 2 (cabo midi) conectado ao terra.
 * Pino 4 (cabo midi) conectado aos +5V em série com um resistor de 220 ohms.
 * Há um led conectado ao pino digital 8, que acende e apaga cada vez que uma nota é tocada.
 
 Conecte o cabo midi no módulo midi e ouça a música.
 
 Programa criado por Marcelo Rocha.
 
 Este código é de domínio público.
 
 Assista ao vídeo do projeto funcionando: www.fisicarduino.com
 
 */
 
boolean estado = 1; // Variável que define o estado do led ( aceso ou apagado ).
int ledPin = 8; // Pino do led.
// A variável Notas é um array que contém as notas da música. Cada nota musical equivale a um valor em hexadecimal.
// 0x3C é o dó central do piano, o dó3 e assim por diante.
char notas[] = {0x3C,0x40,0x43,0x48,0x4C,0x43,0x48,0x4C,0x3C,0x40,0x43,0x48,0x4C,0x43,0x48,0x4C,
                0x3C,0x3E,0x45,0x4A,0x4D,0x45,0x4A,0x4D,0x3C,0x3E,0x45,0x4A,0x4D,0x45,0x4A,0x4D,
                0x3B,0x3E,0x43,0x4A,0x4D,0x43,0x4A,0x4D,0x3B,0x3E,0x43,0x4A,0x4D,0x43,0x4A,0x4D,
                0x3B,0x3C,0x43,0x48,0x4C,0x43,0x48,0x4C,0x3B,0x3C,0x43,0x48,0x4C,0x43,0x48,0x4C};

void setup() {
  
  Serial.begin(31250); //  Configura a velocidade de comunicação serial.
  pinMode(ledPin, OUTPUT); // Configura o ledPin com saída.
  delay(1000); // Espera 1s.
  /* Através do protocolo midi podemos comandar o dispositivo midi com vários parâmetros.
     Podemos mudar o timbre através de um comando chamado (Program Change), mudar a afinação usando um PITCH BEND e etc.
  */
  Serial.write(0xC0); // Neste caso 0xC0 é o código para enviar informação do tipo PROGRAM CHANGE.
  Serial.write(0x0D); // Aqui temos o número do som que queremos, neste caso é o 0x0D que é 13 em decimal.
}

void loop() {
  // Este for varre o nosso vetor notas, que tem 64 posições.
  for (int nota = 0; nota <= 63; nota ++) {
    /*
      Os dispositivos midi possuem 16 canais de midi, que são mapeados no protocolo assim, de 0x00 à 0x0F.
      Alguns módulos midi são multitimbrais, ou seja, são capazes de reproduzir 16 canais simultaneamente.
      Por exemplo, podemos tem um piano no canal 1 e uma bateria no 10, simultaneamente.
      O módulo que eu uso neste projeto é o Micro Piano da KURZWEIL, este não é multitimbral, pode receber 
      informaçaõ em qualquer canal, porém só pode reproduzir um canal por vez.
    */
    int tempo = analogRead(0); // Tempo recebe a leitura da porta analógica 0, potênciometro que controla a velocidade de execução da música.
    int tom = analogRead(1); // Tom recebe a leitura da porta analógica 1, potênciometro que controla a tonalidade da música. Podemos subir 11 semitons.
    tempo = map(tempo, 0 , 1023, 30, 250); // Tempo = ao mapeamento da escala de 0 à 1023 (10 bits) para uma escala de 30 à 250.
    tom = map(tom, 0, 1023, 0, 11); // Tom = ao mapeamento da escala de 0 à 1023 (10 bits) para uma escala de 0 à 11 (semitons).
    // Toca a primeira nota através do canal de midi 1. Canal 1 = 0x90 + 0x00 = 0x90, canal 16 = 0x90 + 0x0F = 0x9F.
    noteOn(0x90, notas[nota]+tom, 0x45);
    digitalWrite(ledPin, estado); // Coloca o led no estado atual. Aceso de estado=1 e apagado se estado=0;
    delay(tempo); // Tempo de duração da nota.
    // Obs.: Aqui temos a mesma nota, transmitida pelo mesmo canal 1, porém com um velocity = 0x00. Que gera um noteOff.
    noteOn(0x90, notas[nota]+tom, 0x00);  
    estado = !estado; // Muda os estado do led. Se aceso, apaga ( 1 -> 0). Se apagado, acende ( 0 -> 1 ).
    delay(1); // Pequena pausa para que o módulo receba o noteOff.
  } 
  delay(1000); // Espera 1s para repetir a música.
}

// Função noteOn, recebe os parâmetros ( cmd = Comando, pitch = Nota, velocity = (Intensidade com que será tocada a nota, de 0 à 127.))
  void noteOn(int cmd, int pitch, int velocity) {
    Serial.write(cmd); // Envia o comando.
    Serial.write(pitch); // Envia a nota.
    Serial.write(velocity); // Envia o velocity.
}
