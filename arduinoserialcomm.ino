#define ledon 6
#define ledoff 8
bool value,text;
String inpstr;
String mesaj;
int count;
int data;
void setup(){
  Serial.begin(9600);
  pinMode(ledon,OUTPUT);
  pinMode(ledoff,OUTPUT);
  }

void clearbuff(){
  mesaj = "";
  inpstr = "";
  }

void loop(){
  if (Serial.available()){
    char deger = Serial.read();
    inpstr += deger;
    int val = digitalRead(ledon); // send data of component to pc
    Serial.println(val);
    if (inpstr.substring(0,3) == "202"){
      if (inpstr.substring(inpstr.length(),inpstr.length()-3) == "son"){
        digitalWrite(ledon,HIGH);
        digitalWrite(ledoff,LOW);
        Serial.println("CODE : 202");
        Serial.println("==========");
        mesaj = inpstr.substring(3,inpstr.length()-3);
        Serial.print("Message: ");
        Serial.println(mesaj);
        Serial.println("RECEIVE COMPLETED");
        Serial.print("Message Length: ");
        Serial.println(mesaj.length());
        delay(3000);
        clearbuff();
        Serial.println("BUFFER CLEARED");
        digitalWrite(ledoff,HIGH);
        digitalWrite(ledon,LOW);
        }
      }
    }
    
  else{
    digitalWrite(ledon,LOW);
    digitalWrite(ledoff,HIGH);
    }
  }
