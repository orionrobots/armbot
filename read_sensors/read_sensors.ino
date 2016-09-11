/**
 Reads all 5 A0 sensors and outputs them to serial.
 For checking/calibrating the uARm feedback
 */
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

int sensors[] = {A0, A1, A2, A3, A4};
int sensor_vals[5];
void loop() {
  // read the analog in value:
  for(int i=0; i<5; i++) {
    sensor_vals[i] = analogRead(sensors[i]);
  }
 
  // print the results to the serial monitor:
  Serial.print("sensors = " );
  for(int i=0; i<5; i++) {
    Serial.print(sensor_vals[i]);
    Serial.print(" ,");
  }
  Serial.println("");
  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);                     
}
