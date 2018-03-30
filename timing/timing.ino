#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


RF24 radio(7,8);

const uint64_t rxAddr = 0xF0F0F0F0E1LL;
const uint64_t myAdd = 0x28;

int button = 5;
int resetButton = 6;//;
bool resetButtonState = 0;
unsigned long timer = 0;
bool buttonState = 0;
int goLED = 2;
int stopLED = 4;
unsigned int confirmationCode = 24;
unsigned long resetPress = 0;
//*****************************************************

//--------------
//SET LANE HERE
//--------------

unsigned int identifier = 1;
int nanoID = identifier;
int laneID = nanoID;

//******************************************************

void setup()
{
  pinMode(goLED,OUTPUT);
  pinMode(stopLED,OUTPUT);
  pinMode(resetButton, INPUT_PULLUP);
  pinMode(button,INPUT_PULLUP);
  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(8,15);
  radio.openWritingPipe(rxAddr);
  radio.openReadingPipe(1, myAdd);
  while(!Serial);
  Serial.begin(9600);
}


void loop()
{

radio.startListening();

//listening to the other radio
Serial.println("Waiting...");
digitalWrite(stopLED,HIGH);

bool message = false;
bool a = true;
bool heatLooping = true;

//************************************************************
while(!message){
    if(radio.available()){
        int text = 0;
        Serial.println("receiving stuff");
        radio.read(&text, sizeof(text));
        Serial.println(text);
        
        //checking for special message
            if (text == 666){
                //Serial.println("Yay");
                timer = millis();
                message = true;
                
                digitalWrite(goLED,HIGH);
                digitalWrite(stopLED,LOW);
                radio.stopListening();
                radio.flush_tx();
                heatLooping = true;
                }//End 666 if
        }//End radio.available if
                                      
      //Hande reset button press after accidental time send
      if (digitalRead(resetButton) == LOW && (millis() - resetPress > 500)){
          heatLooping = true;
          resetPress  = millis();
          Serial.println("Back to timing");
          digitalWrite(goLED,HIGH);
          digitalWrite(stopLED,LOW);
          break;
         }
}//End listening for message while
//*****************************************************************
          
//getting ready to send information
radio.stopListening();
radio.flush_tx();

while(heatLooping == true){
//waiting for button to be pressed

  buttonState      = digitalRead(button);
  resetButtonState = digitalRead(resetButton);

  //If reset button pressed, send a no swimmer message
  if (resetButtonState == LOW && (millis() - resetPress > 500)){
    Serial.println("No Swimmer");
    resetPress = millis();
    unsigned int voidState = 999;
    unsigned int fillerSpot = 69;
    unsigned int messageToSend[3] = {nanoID, fillerSpot, voidState};

    //STUFF TO HANDLE CONFIRMATION OF TIME SIGNAL BEING SENT & RECEIVED BY RECEIVING UNIT
    bool successfulComms = false;
    while (successfulComms == false){

      radio.write(&messageToSend, sizeof(messageToSend));
      Serial.println("Sent");
      radio.startListening();
      Serial.println("Listening...");
      unsigned int startListenTime = millis();
      unsigned int listenTime = millis();
      while (successfulComms == false || listenTime <= 20){
        //Serial.println("Trying again");
        if (radio.available()){
          int conf[2];
          Serial.println("RADIO WAS AVAIALABLE");
          radio.read(&conf, sizeof(conf));
          Serial.println(conf[0]);
          Serial.println(conf[1]);
            if ((conf[0]) == laneID){
              Serial.println("correct identifier");
                if ((conf[1]) == confirmationCode){
                  Serial.println("correct confirationCode");
                  successfulComms = true;
                  break; //Break out of || while loop, we're good
                }//End confirmation if
            }// End identifier if
          }//end radio.available() if
          
         listenTime = millis() - startListenTime;
         }// End successfulComm/wait for confirmation while

       radio.stopListening();
       radio.flush_tx();
       }//end sending/confirmation while (successfulComms == false)
       
      digitalWrite(goLED,LOW);
      digitalWrite(stopLED,HIGH);
      heatLooping = false;
  }//End reset button if






 //once the button is pressed send the time
  if (buttonState==LOW && heatLooping == true){
    //calculate the time
    unsigned long capture = millis()-timer;
    //Serial.println(capture);
    //send the time
    unsigned int seconds   = capture/1000;
    //String secondsString = String(seconds);
    unsigned int hundreths = (capture % 1000)/10;
    //String hundrethsString = String(seconds);
    //String identifierString = String(identifier);
    //String messageToSendString = identifierString +secondsString + hundrethsString;
    //Serial.println(messageToSendString);
    unsigned int messageToSend[3] = {nanoID, seconds, hundreths};
    Serial.println(messageToSend[0]);
    Serial.println(messageToSend[1]);
    Serial.println(messageToSend[2]);

    //STUFF TO HANDLE CONFIRMATION OF TIME SIGNAL BEING SENT & RECEIVED BY RECEIVING UNIT
    bool successfulComms = false;
    while (successfulComms == false){

      radio.write(&messageToSend, sizeof(messageToSend));
      Serial.println("Sent");
      radio.startListening();
      Serial.println("Listening...");
      unsigned int startListenTime = millis();
      unsigned int listenTime = millis();
      while (successfulComms == false && listenTime <= 40){
        //Serial.println("Trying again");
        if (radio.available()){
          int conf[2];
          Serial.println("RADIO WAS AVAIALABLE");
          radio.read(&conf, sizeof(conf));
          Serial.println(conf[0]);
          Serial.println(conf[1]);
            if ((conf[0]) == laneID){
              Serial.println("correct identifier");
                if ((conf[1]) == confirmationCode){
                  Serial.println("correct confirationCode");
                  successfulComms = true;
                  break; //Break out of || while loop, we're good
                }//End confirmation if
            }// End identifier if
          }//end radio.available() if
          
         listenTime = millis() - startListenTime;
         }// End successfulComm/wait for confirmation while

       radio.stopListening();
       radio.flush_tx();
       }//end sending/confirmation while (successfulComms == false)
       
      digitalWrite(goLED,LOW);
      digitalWrite(stopLED,HIGH);
      heatLooping = false;
      }//End loop for timer button press. Setting heatLooping = false breaks out of that loop
}// end while (heatLooping == true)
}//End main loop

void configure_lanes(){
 digitalWrite(goLED, HIGH);
 digitalWrite(stopLED, HIGH);
 resetButtonState = digitalRead(resetButton);
 while (resetButtonState == HIGH){
    if (digitalRead(resetButton) == LOW){
      
    bool successfulComms = false;
    while (successfulComms == false){
      String messageToSend = (String)nanoID;
      radio.write(&messageToSend, sizeof(messageToSend));
      //Serial.println("sent");
      radio.startListening();
      unsigned int startListenTime = millis();
      unsigned int listenTime = millis();
      while (successfulComms == false && listenTime <= 40){
        if (radio.available()){
          int conf[3];
          Serial.println("RADIO WAS AVAIALABLE");
          radio.read(&conf, sizeof(conf));
          Serial.println(conf[0]);
          Serial.println(conf[1]);
            if ((conf[0]) == nanoID){
              Serial.println("correct identifier");
                if ((conf[1]) == confirmationCode){
                  Serial.println("correct confirationCode");
                  int newLane = (int)conf[2];
                  laneID = newLane;
                  successfulComms = true;
                  break;
                }//End confirmation if
            }// End identifier if
          }//end radio.available() if
          
         listenTime = millis() - startListenTime;
         }// End successfulComm/wait for confirmation while

       radio.stopListening();
       radio.flush_tx();
       }//end sending/confirmation while (successfulComms == false)
       
      digitalWrite(goLED,LOW);
      digitalWrite(stopLED,HIGH);
      }//End loop for timer button press.

      break;
    }
 }
