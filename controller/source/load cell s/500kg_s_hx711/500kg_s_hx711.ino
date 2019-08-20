/*
 Setup your scale and start the sketch WITHOUT a weight on the scale
 Once readings are displayed place the weight on the scale
 Press +/- or a/z to adjust the calibration_factor until the output readings match the known weight
 Arduino pin A0 -> HX711 CLK
 Arduino pin A1 -> HX711 DOUT
 Arduino pin 5V -> HX711 VCC
 Arduino pin GND -> HX711 GND 

 red E+
 black E-
 green A-
 white A+t
*/

#include "HX711.h"
//        DOUT, CLK
HX711 scale_left(2, 3);
HX711 scale_right(4, 5);

// left factor -870
// right factor 868

float units_left;
float units_right;

void setup() {
  Serial.begin(9600);
  scale_left.tare();
  scale_right.set_scale(-870);
  scale_left.tare();
  scale_right.set_scale(868);
}

void loop() {
  units_left = scale_right.get_units();
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
