#include <SPI.h>
#include <nRF24L01.h>
//#include <printf.h>
#include <RF24.h>
//#include <RF24_config.h>
RF24 radio(7,8);

const byte rxAddr[6] = "00001";
int button = 12;
bool pressed = false;
bool message = false; 
bool sending = false;
unsigned int t = 0;
unsigned int timer = 0;
bool buttonState = 0;

void setup()
{

  pinMode(button,INPUT_PULLUP);
  radio.begin();
  radio.setRetries(15,15);
  //radio.openWritingPipe(rxAddr);

  //radio.stopListening();
  while(!Serial);
  Serial.begin(9600);
}

void loop()
{
  radio.openReadingPipe(0, rxAddr);
  radio.startListening();
  
 //listening to the other radio
  
  while(!message){
    
    if(radio.available()){
      int text = 0;
      Serial.println("receiving stuff");
      radio.read(&text, sizeof(text));
      Serial.println(text);

 //checking for special message
 
        if (text == 2){
          Serial.println("Yay");
            message = true;
            timer = millis();
            radio.stopListening();        
        }
  
      }
  }

//getting ready to send information

  radio.openWritingPipe(rxAddr);
  while(true){
    
//waiting for button to be pressed
    
    buttonState = digitalRead(button);
    
 //once the button is pressed send the time
 
    if (buttonState==LOW){
      //calculate the time
      unsigned int capture = millis()-timer;
      Serial.println(capture);

 //send the time
 
      radio.write(&capture, sizeof(capture));
      break;
    }
  }

  delay(1000);
}

