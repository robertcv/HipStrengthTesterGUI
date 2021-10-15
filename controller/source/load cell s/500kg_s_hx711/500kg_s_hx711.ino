/*
 differs from manufacturer to manufacture
 black E+
 white E-
 green A-
 red A+
*/

#include "HX711.h"
#include "TimerOne.h"

//                DOUT, CLK
HX711 scale_left( 2,    3);
HX711 scale_right(4,    5);

// left factor 2135
// right factor 2113

int units_left, units_right;
int time_counter = 0;

void setup() {
  Serial.begin(115200);
  
  scale_left.tare();
  scale_left.set_scale(2135);
  scale_right.tare();
  scale_right.set_scale(2113);

  // every 10 ms -> 100Hz
  Timer1.initialize(10000);
  Timer1.attachInterrupt(make_measurement);
}

void make_measurement() {
  units_left = (int)scale_left.get_units();  // takes around 0.4 ms
  units_right = (int)scale_right.get_units();

  Serial.print(time_counter);
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
