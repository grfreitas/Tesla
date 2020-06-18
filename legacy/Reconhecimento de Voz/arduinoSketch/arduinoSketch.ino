char estado, disp;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()>0){
    estado = Serial.read();
    disp   = Serial.read();
    if(estado == '1'){
      if(disp == 'l') digitalWrite(5, HIGH);
      /*...*/
    }
    else{
      if(disp == 'l') digitalWrite(5, LOW);
    }
  }
}
