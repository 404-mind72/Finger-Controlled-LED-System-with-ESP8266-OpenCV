#define LED1_PIN D1
#define LED2_PIN D2

void setup() {
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);

  Serial.begin(9600);
  Serial.println("Menunggu data 0/1 dari Python...");
}

void loop() {
  if (Serial.available() > 0) {
    int ledStatus = Serial.parseInt();

    Serial.print("LED Status: ");
    Serial.println(ledStatus);

    if (ledStatus == 1) {
      digitalWrite(LED1_PIN, HIGH);
      digitalWrite(LED2_PIN, HIGH);
    } else {
      digitalWrite(LED1_PIN, LOW);
      digitalWrite(LED2_PIN, LOW);
    }
  }
}
