const int ledPins[5] = {18, 19, 21, 22, 23};
const int totalLeds = 5;

void setup() {
  Serial.begin(115200);
  
  for (int i = 0; i < totalLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    int count = data.toInt();

    count = constrain(count, 0, totalLeds);

    for (int i = 0; i < totalLeds; i++) {
      if (i < count) {
        digitalWrite(ledPins[i], HIGH);
      } else {
        digitalWrite(ledPins[i], LOW);
      }
    }
  }
}