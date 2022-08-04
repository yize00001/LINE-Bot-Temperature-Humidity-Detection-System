//讀取光敏電阻
int photocellPin = A2; // 光敏電阻接在anallog pin 2
int photocellVal = 0; // photocell variable
void setup() {
 Serial.begin(115200);
}
 
void loop() {
 // 讀取光敏電阻並輸出到 Serial Port 
 photocellVal = analogRead(photocellPin);
 Serial.println(photocellVal); 
 delay(100); 
}
