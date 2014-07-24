// Game Genius no Arduino
// www.fisicarduino.com
// Autor: Marcelo Rocha
// Data: 27-04-2014
// OS - Gnu/Linux - Debian Wheezy - amd64 
// Ide Arduino versão 1.0.1

// define as cores
#define VERMELHO  0
#define VERDE     1
#define AMARELO   2
#define AZUL      3

//define o pino do buzzer e as caracteristicas do som
#define BUZZER 8
// frequência base
#define FREQ_BASE 1000
// define a duração do som
#define DURACAO 200

// pinos dos leds // pino base 9
#define LEDPIN_BASE 9
// define os pinos para o leds
byte ledVermelho = LEDPIN_BASE + VERMELHO; // 9 + 0 = 9
byte ledVerde    = LEDPIN_BASE + VERDE;    // 9 + 1 = 10
byte ledAmarelo  = LEDPIN_BASE + AMARELO;  // 9 + 2 = 11
byte ledAzul     = LEDPIN_BASE + AZUL;     // 9 + 3 = 12

// pinos dos push buttons // pino base 4
#define INPIN_BASE 4

byte inPinVermelho = INPIN_BASE + VERMELHO; // 4 + 0 = 4
byte inPinVerde = INPIN_BASE + VERDE;       // 4 + 1 = 5
byte inPinAmarelo = INPIN_BASE + AMARELO;   // 4 + 2 = 6
byte inPinAzul = INPIN_BASE + AZUL;         // 4 + 3 = 7

// valores para a função random que vai gerar numeros de 0 (inclusive) a 3 (inclusive)
const int MIN = 0;
const int MAX = 3;

const byte NUM_ELEMENTOS = 4; // 4 elementos igual a 4 fases. Mude esse valor para quantas fases desejar
byte matriz_jogo [NUM_ELEMENTOS]; // cria a matriz_jogo
byte fase = 0; // fase atual = 0. teremos 4 fases [0, 1, 2, 3]


void setup() {
	// gera a semente para a função random usando a instabilidade da porta analógica quando não está conectada
	randomSeed(analogRead(0)); 
	
	// configura os pinos dos leds como pinos de saída
	pinMode (ledVermelho, OUTPUT);
	pinMode (ledVerde,    OUTPUT);
	pinMode (ledAmarelo,  OUTPUT);
	pinMode (ledAzul,     OUTPUT);
	
	// configura os pinos dos botões como pinos de entrada
	pinMode (inPinVermelho, INPUT);
	pinMode (inPinVerde,    INPUT);
	pinMode (inPinAmarelo,  INPUT);
	pinMode (inPinAzul,     INPUT);
}

void loop() {
	init_game(); // inicializa o jogo
	while (fase < NUM_ELEMENTOS) {
		joga(fase); // joga a fase corrente
		fase++; // muda de fase
	}
	ganhou(); // chama a função da vitória
}

void init_game() {
	for (int n = 0; n < NUM_ELEMENTOS; n++) {
		matriz_jogo [n] = random(MIN, MAX + 1); // sorteia um cor (de min=0 até max=3) e alimenta a matriz_jogo
	}
	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH); // acende o led no pino 13 indicando que o jogo começou
}

// inicia o jogo a partir da primeira fase
void joga(byte fase) {
	// varre a matriz lendo cada elemento de cada fase
	for (int i=0; i <= fase; i++) {
		leds((matriz_jogo[i])); // acende o led referente ao conteúdo da matriz. ex.: 0 = vermelho...
	}
	// recebe a entrada dos botões e as compara com o conteúdo da matriz
	for (int i=0; i <= fase; i++) {
		if (recebe() == matriz_jogo[i]) { // a função recebe retorna o valor da cor referente ao botão pressionado
			leds((matriz_jogo[i])); // acende o led de acordo com o botão pressionado
		} 
		else {
			perdeu(); // chama a função da derrota
		}  
	}
}

// le os contatos do push buttons e retorna um byte. 0 = vermelho....
byte recebe() {
	while(1) {
		if (digitalRead(inPinVermelho) == 1) return VERMELHO; // VERMELHO = 0
		if (digitalRead(inPinVerde) == 1)    return VERDE;    // VERDE = 1
		if (digitalRead(inPinAmarelo) == 1)  return AMARELO;  // AMARELO = 2
		if (digitalRead(inPinAzul) == 1)     return AZUL;     // AZUL = 3
		delay(100); // um pequena pausa de 100ms
	} 
}

// acende o led de acordo com a cor passado como parâmetro
void leds(byte cor) {
	const int PAUSA = 500; // pausa em millisegundos (500ms)
	som_pin(cor); // chama a função que gera o som referente à cor
	digitalWrite(LEDPIN_BASE + cor, HIGH); // acende led cor
	delay(PAUSA);
	digitalWrite(LEDPIN_BASE + cor, LOW);  // apaga led cor
	delay(PAUSA); 
}

// função da derrota
void perdeu() {
	while (1) {
		digitalWrite(LEDPIN_BASE + VERMELHO, HIGH); // acende o led vermelho
		// gera o ruído
		for (int f = 1000; f > 100; f = f - 100) {
			tone(BUZZER, f, 50);
			delay(50);
			noTone(BUZZER);
		}
		// gera o ruído	
		digitalWrite(LEDPIN_BASE + VERMELHO, LOW); // apaga o led vermelho
		for (int f = 1000; f > 100; f = f - 100) {
			tone(BUZZER, f, 50);
			delay(50);
			noTone(BUZZER);
		}		
	}
}

// função da vitória
void ganhou() {
	while (1) {
		apaga_leds(); // chama a função que apaga os leds
		// acende os leds um de cada vez
		for (int i = 0; i < 4; i++) {
			digitalWrite(LEDPIN_BASE + i, HIGH);
			tone(BUZZER, FREQ_BASE * (i + 1), DURACAO); // gera o som de cada cor
			delay(200);
		}
	}
}

// emite um tom para cada cor
void som_pin(byte cor) { 
	noTone(BUZZER); // pára o som do Buzzer
	tone(BUZZER, FREQ_BASE * (cor + 1), DURACAO); // emite o tom 1000 * (0 + 1) = 1000Hz = 1KHz
}

// apaga todos os leds
void apaga_leds() {
	// apaga os leds  
	for (int i = 0; i < 4; i++) {
		digitalWrite(LEDPIN_BASE + i, LOW);
	}
}
