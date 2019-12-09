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

float calibration_factor = 870;
float units_left;
float units_right;
int foot = 0;

void setup() {
  Serial.begin(9600);
  scale_left.tare();
  scale_right.set_scale(-870);
  scale_left.tare();
  scale_right.set_scale(868);
}

void loop() {
  units_left = scale_right.get_units(), 10;
  units_right = scale_right.get_units(), 10;
  Serial.print(units_left);
  Serial.print(", ");
  Serial.print(units_right);
  Serial.print(", ");
  Serial.println(calibration_factor);
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == 'a')
      calibration_factor -= 0.01;
    else if(temp == 'y')
      calibration_factor += 0.01;
    else if(temp == 's')
      calibration_factor -= 0.1;
    else if(temp == 'x')
      calibration_factor += 0.1;
    else if(temp == 'd')
      calibration_factor -= 1;
    else if(temp == 'c')
      calibration_factor += 1;
    else if(temp == 'f')
      calibration_factor -= 10;
    else if(temp == 'v')
      calibration_factor += 10;
    else if(temp == 't' || temp == 'T'){
      scale_right.tare();
      scale_left.tare();}
    else if(temp == 'l')
      foot = 0;
    else if(temp == 'r')
      foot = 1;
  }
  if (foot == 0){
    scale_left.set_scale(calibration_factor);
  } else {
    scale_right.set_scale(calibration_factor);
  }
  delay(100);
}
