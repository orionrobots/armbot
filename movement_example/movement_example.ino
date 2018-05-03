#include <Servo.h>

Servo gripper;
Servo wrist;
Servo elbow;
Servo shoulder;
Servo base;

#define buttona 7
#define buttonb 4

void setup() {
  pinMode(buttona, INPUT);
  pinMode(buttonb, INPUT);
  gripper.attach(9);
  wrist.attach(10);
  base.attach(11);
  elbow.attach(12);
  shoulder.attach(13);
}

void loop() {
  if(!digitalRead(buttona)) {
    gripper.write(60);
    wrist.write(90);
    elbow.write(90);
    shoulder.write(90);
    base.write(90);
    
    delay(1000);
  //  base.write(;
    shoulder.write(20);
    elbow.write(130);
    delay(300);
    gripper.write(90);
    delay(500);
    
    base.write(100);
    shoulder.write(90);
    elbow.write(90);
    gripper.write(60);
    delay(100);
    gripper.write(90);
  }
}
