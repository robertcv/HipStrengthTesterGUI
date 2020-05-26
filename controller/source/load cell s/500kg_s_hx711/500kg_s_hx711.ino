/*
 differes from manufacturet to manufacture
 black E+
 white E-
 green A-
 red A+
*/

#include "HX711.h"
//               DOUT, CLK
HX711 scale_left(2, 3);
HX711 scale_right(4, 5);

// left factor 2135
// right factor 2113

float units_left;
float units_right;

void setup() {
  Serial.begin(9600);
  scale_left.tare();
  scale_left.set_scale(2135);
  scale_right.tare();
  scale_right.set_scale(2113);
}

void loop() {
  units_left = scale_left.get_units();
  units_right = scale_right.get_units();
  Serial.print(units_left);
  Serial.print(", ");
  Serial.print(units_right);
  Serial.print("\n");
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == 't' || temp == 'T'){
      scale_right.tare();
      scale_left.tare();
    }
  }
  delay(100);
}
