/*
 differs from manufacturer to manufacture
 black E+
 white E-
 green A-
 red A+
*/

#include "HX711.h"
#include "TimerOne.h"

//               DOUT, CLK
HX711 scale_left( 2,    3);
HX711 scale_right(4,    5);

// left factor 2075
// right factor 2090

volatile int units_left, units_right;
volatile long time_counter = 0;

void setup() {
  Serial.begin(115200);
  
  scale_left.tare();
  scale_left.set_scale(2075);
  scale_right.tare();
  scale_right.set_scale(2090);

  Timer1.initialize(100000);
  Timer1.attachInterrupt(make_measurement);
}

void make_measurement() {
  units_left = (int)scale_left.get_units();
  units_right = (int)scale_right.get_units();

  Serial.print(time_counter / 10.0, 2);
  Serial.print(",");
  Serial.print(units_left);
  Serial.print(",");
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

  time_counter++;
}

void loop() { 
}
