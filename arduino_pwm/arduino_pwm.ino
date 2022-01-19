#include <Servo.h> 


#define enable 8


Servo s1;
Servo s2;

long input = 0;
long v1;
long v2;
long e;

void setup() 

{ 

  Serial.begin(115200);
  Serial.setTimeout(10);   
  s1.attach(11);
  s2.attach(10);

  s1.writeMicroseconds(1000);
  s2.writeMicroseconds(1000); 

} 



void loop() {

  if (Serial.available() > 0) {

    input = Serial.parseInt();

    if (input!=0){

      if (input<0){

        input = 0;

      }
      e = input * 0.000001;
      input = input-e*1000000;
      v1 = input * 0.001;
      input =input-v1*1000;
      v2 = input;
      
      v1 = v1 + 1000;
      v2 = v2 + 1000;
      
      s1.writeMicroseconds(v1);
      s2.writeMicroseconds(v2);
      
      Serial.print(e);
      Serial.print(" ");
      Serial.print(v1);
      Serial.print(" ");
      Serial.print(v2);
      Serial.print("\n");
      
    }

    

  }

  delay (10);

}
