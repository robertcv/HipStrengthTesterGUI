/*
 differs from manufacturer to manufacturer
 black E+
 white E-
 green A-
 red A+
*/

#include "HX711.h"
              // DOUT, CLK
HX711 scale_left(2, 3);
HX711 scale_right(4, 5);

// left factor 2135
// right factor 2113

float calibration_factor = 2115;
float units_left;
float units_right;
int foot = 1;

void setup() {
  Serial.begin(9600);
  scale_left.tare();
  scale_left.set_scale(calibration_factor);
  scale_right.tare();
  scale_right.set_scale(calibration_factor);
}

void loop() {
  units_left = scale_left.get_units(), 10;
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
  delay(50);
}
