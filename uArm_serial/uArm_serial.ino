/*
P<motor>,<pos> - set position
?<motor> - read position
A<motor> - attach 
D<motor> - detach
; - terminate input (end of int lines - prevents timeouts on parseInt)
*/

#include <Servo.h>

#define SERVO_COUNT 5
#define SERVO_START_PIN 9
#define BEEPER_PIN 3

Servo motors[SERVO_COUNT];
int pots[SERVO_COUNT] = {A4, A3, A2, A1, A0};

void setup() {
	// setup pins
	pinMode(A0, INPUT);
	pinMode(A1, INPUT);
	pinMode(A2, INPUT);
	pinMode(A3, INPUT);
	pinMode(A4, INPUT);
	pinMode(3, OUTPUT);
	//Setup serial

	Serial.begin(9600);
	Serial.println("Ready:");
}

void timestamp() {
//	Serial.print(millis());
//	Serial.print(":");
}

void error(char * msg) {
	Serial.print("Error:");
	Serial.println(msg);
}

void handle_set(int joint_no) {
	//Handle setting a motor position
	//digitalWrite(3, HIGH);
	int comma = Serial.read();
	if(comma != ',') {
		error("Expected comma");
		return;
	}
	int position = Serial.parseInt();
	
	motors[joint_no].write(position);
 	timestamp();
	Serial.print("-Moved motor");
	Serial.print(joint_no);
	Serial.print(" to position ");
	Serial.println(position);
	//digitalWrite(3, LOW);
}

void handle_read(int joint_no) {
	int value = analogRead(pots[joint_no]);
	Serial.println(value);
}

void handle_attach(int joint_no) {
	if(!motors[joint_no].attached()) {
		motors[joint_no].attach(joint_no + SERVO_START_PIN);
	}
}

void handle_detach(int joint_no) {
	if(motors[joint_no].attached()) {
		motors[joint_no].detach();
	}
}

void loop() {
  int value = Serial.read();
  //read char
  if(value != -1) {
	char cmd = value;
	timestamp();
	Serial.print("Command received:");
	if(cmd == ';') {
		return;
	}
	Serial.println(cmd);
	int joint_no = Serial.parseInt();
	// Respond
	switch(cmd) {
	case 'P':
		handle_set(joint_no);
		break;
	case '?':
		handle_read(joint_no);
		break;
	case 'A':
		handle_attach(joint_no);
		break;
	case 'D':
		handle_detach(joint_no);
		break;
	default:
		error("Not understood");
	}
	timestamp();
	Serial.println("Command complete");
  }
}
