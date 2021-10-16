#include <math.h>

float out = 0;
int n = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (n < 500) {
    out = (float)random(6) - 3;
  }
  else if (n < 1000) {
    out = (float)random(6) + 25;
  }
  else if (n < 1200) {
    out = (float)tanh((float)(n - 100) / 5) * 100.0 + 100 + (float)random(6) - 3;
  }
  else if (n < 1500) {
    out = 200 + (float)random(6) - 3;
  }
  else {
    out = (float)random(6) - 3;
  }
  
  Serial.print(n / 100.0, 2);
  Serial.print(",");
  Serial.print((int)out);
  Serial.print(",");
  Serial.print((int)out);
  Serial.println();
  delay(10);
  n++;
}
