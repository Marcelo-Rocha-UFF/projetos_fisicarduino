int digit[] = {254, 48, 109, 121, 51, 91, 95, 112, 127, 115};
int myPins[] = {24, 25, 34, 33, 32, 23, 22};
int vel[]= {0, 70, 100, 130, 255};
int pwPort = 12; 
int bytelido = 0;

void setup (){
  for ( int i=0 ; i<=7 ; i++){
    pinMode(myPins[i], OUTPUT);
  }
  pinMode(pwPort, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  while (Serial.available() > 0){
    bytelido = Serial.read();
    if (bytelido == '0') { 
      analogWrite(pwPort, vel[0]);
      showNumber(0);
    };
    if (bytelido == '1') { 
      analogWrite(pwPort, vel[1]);
      showNumber(1);
    };
    if (bytelido == '2') { 
      analogWrite(pwPort, vel[2]);
      showNumber(2);
    };
    if (bytelido == '3') { 
    analogWrite(pwPort, vel[3]);
    showNumber(3);
    };
    if (bytelido == '4') { 
    analogWrite(pwPort, vel[4]);
    showNumber(4);
    };
  }
}
void showNumber( int n ){
  for ( int b=0; b<=6 ; b++){
      digitalWrite(myPins[b], bitRead(digit[n], 6-b));
    }
}

