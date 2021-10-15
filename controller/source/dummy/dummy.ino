#include <math.h>

float out = 0;
int n = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (n < 100) {
    out = (float)random(6) - 3;
  } 
  else if (n < 120) {
    out = (float)tanh((float)(n - 100) / 5) * 100.0 + 100 + (float)random(6) - 3;
  }
  else if (n < 150) {
    out = 200 + (float)random(6) - 3;
  }
  else {
    out = (float)random(6) - 3;
  }
  
  Serial.print(n / 10.0);
  Serial.print(",");
  Serial.print((int)out);
  Serial.print(",");
  Serial.print((int)out);
  Serial.println();
  delay(100);
  n++;
}
