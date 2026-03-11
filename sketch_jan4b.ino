int buzzPin = 10;   // Pin for the buzzor
int pirPin = 12;   // Pin for the PIR sensor

void setup() {
  pinMode(buzzPin, OUTPUT);   // Set buzz pin as output
  pinMode(pirPin, INPUT);    // Set PIR sensor pin as input
  Serial.begin(9600);        // Start serial communication at 9600 baud rate
}

void loop() {
  int pirState = digitalRead(pirPin); // Read the PIR sensor value
  
  if (pirState == HIGH) {
    digitalWrite(buzzPin, HIGH);  // Turn on the buzz when motion is detected
    Serial.println("Motion detected");
  } else {
    digitalWrite(buzzPin, LOW);   // Turn off the buzz when no motion is detected
    Serial.println("No motion");
  }
  
  delay(3000); // Delay for 3000 milliseconds before checking again
}
