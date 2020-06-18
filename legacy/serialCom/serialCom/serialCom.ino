char pin;
char state;

void setup(){

  pinMode(5, OUTPUT);
  
  Serial.begin(9600);
  Serial.flush();
}

void loop(){

  while(Serial.available() > 0){
  
    state = Serial.read() - '0';
    delay(5);
    pin = Serial.read() - '0';
  }
  
  digitalWrite(pin, state);

}
