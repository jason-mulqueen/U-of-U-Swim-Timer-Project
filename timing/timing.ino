#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


RF24 radio(7, 8);

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
int configureCode = 33;
unsigned long resetPress = 0;
int exitConfigureCode = 12345;
bool resetUsed = false;
//*****************************************************

//--------------
//SET LANE HERE
//--------------
//nanoID should never change
//laneID allows for configuration routine
//identifier is legacy

unsigned int identifier = 6;
unsigned int nanoID = identifier;
unsigned int laneID = nanoID;

//******************************************************

void setup()
{
  pinMode(goLED, OUTPUT);
  pinMode(stopLED, OUTPUT);
  pinMode(resetButton, INPUT_PULLUP);
  pinMode(button, INPUT_PULLUP);
  digitalWrite(stopLED, HIGH);
  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(8, 15);
  radio.openWritingPipe(rxAddr);
  radio.openReadingPipe(1, myAdd);
  while (!Serial);
  Serial.begin(9600);
  digitalWrite(stopLED, LOW);

}


void loop()
{

  radio.startListening();

  //listening to the other radio
  Serial.println("Waiting...");
  digitalWrite(stopLED, HIGH);

  bool message = false;
  bool heatLooping = false;

  //************************************************************
  while (!message) {
    digitalWrite(stopLED, HIGH);
    digitalWrite(goLED, LOW);
    if (radio.available()) {
      int text = 0;
      Serial.println("Receiving...Checking Message:");
      radio.read(&text, sizeof(text));
      Serial.println(text);

      if (text == 33){
        configure_lanes();
        Serial.println("Yup");
        resetUsed = true;
        break;
      }
      
      //checking for special message
      if (text == 666) {
        Serial.println("Starting Timing");
        timer = millis();
        message = true;
        resetUsed = false;

        digitalWrite(goLED, HIGH);
        digitalWrite(stopLED, LOW);
        radio.stopListening();
        radio.flush_tx();
        heatLooping = true;
      }//End 666 if
    }//End radio.available if

    //Hande reset button press after accidental time send
    if (digitalRead(resetButton) == LOW && resetUsed == false) {
      
      resetUsed = true;
      heatLooping = true;
      resetPress  = millis();
      Serial.println("Back to timing");
      digitalWrite(goLED, HIGH);
      digitalWrite(stopLED, LOW);
      break;
    }
  }//End listening for message while
  //*****************************************************************

  //getting ready to send information
  radio.stopListening();
  radio.flush_tx();

  while (heatLooping == true) {
    //waiting for button to be pressed

    buttonState      = digitalRead(button);
    resetButtonState = digitalRead(resetButton);

    //If reset button pressed, send a no swimmer message
    if (resetButtonState == LOW && resetUsed == false) {
      Serial.println("No Swimmer");
      resetUsed = true;
      resetPress = millis();
      unsigned int voidState = 999;
      unsigned int fillerSpot = 69;
      unsigned int messageToSend[3] = {laneID, fillerSpot, voidState};
      heatLooping = send_w_ack(nanoID, fillerSpot, voidState, false);
    }//End reset button if

    //once the button is pressed send the time
    if (buttonState == LOW && heatLooping == true) {
      //calculate the time
      unsigned long capture = millis() - timer;
      //send the time
      unsigned int seconds   = capture / 1000;
      unsigned int hundreths = (capture % 1000) / 10;
      heatLooping = send_w_ack(laneID, seconds, hundreths, false);

    }//End loop for timer button press. Setting heatLooping = false breaks out of that loop
  }// end while (heatLooping == true)
}//End main loop

//*******************************************************************
//USER-DEFINED FUNCTIONS
//*************************



bool send_w_ack(unsigned int &a, unsigned int &b, unsigned int &c, bool configuring) {
  radio.stopListening();
  unsigned int messageToSend[3] = {a, b, c};
  Serial.println(messageToSend[0]);
  Serial.println(messageToSend[1]);
  Serial.println(messageToSend[2]);

  //STUFF TO HANDLE CONFIRMATION OF TIME SIGNAL BEING SENT & RECEIVED BY RECEIVING UNIT
  bool successfulComms = false;
  while (successfulComms == false) {

    radio.write(&messageToSend, sizeof(messageToSend));
    //radio.txStandBy();
    Serial.println("Sent");
    radio.startListening();
    //Serial.println("Listening...");
    unsigned int startListenTime = millis();
    unsigned int listenTime = 0;
    while (successfulComms == false && listenTime <= 40) {
      Serial.println("Top of Listening Loop");
      if (radio.available()) {

        //Code for Configuration Routine--------------------------
        if (configuring == true) {
          int conf[3];
          radio.read(&conf, sizeof(conf));
          if ((conf[0]) == nanoID) {
            //Serial.println("correct identifier");
            if ((conf[1]) == confirmationCode) {
              //Serial.println("correct confirmationCode");
              laneID = conf[2];
              digitalWrite(goLED, LOW);
              digitalWrite(stopLED, HIGH);
              successfulComms = true;
              break; //Break out of && while loop, we're good
            }//End confirmation if
          }// End identifier if
        }//end "Configuring" special algorithm

        //Code for normal message such as times & resets-----------------
        else {
          int conf[2];
          radio.read(&conf, sizeof(conf));
          if ((conf[0]) == laneID) {
            Serial.println("correct identifier");
            if ((conf[1]) == confirmationCode) {
              Serial.println("correct confirmationCode");
              successfulComms = true;
              break; //Break out of && while loop, we're good
            }//End confirmation if
          }// End identifier if
        }//end else

        //End of branching routines

      }//end radio.available() if

      listenTime = millis() - startListenTime;

    }// End successfulComm && listenTime for confirmation while

    radio.begin();
    radio.setAutoAck(false);
    radio.setDataRate(RF24_250KBPS);
    radio.setRetries(8, 15);
    radio.openWritingPipe(rxAddr);
    radio.openReadingPipe(1, myAdd);
    radio.flush_tx();
    radio.stopListening();



  }//end while (successfulComms == false)

  radio.flush_tx();
  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(8, 15);
  radio.openWritingPipe(rxAddr);
  radio.openReadingPipe(1, myAdd);
  radio.flush_tx();
  radio.stopListening();
  digitalWrite(goLED, LOW);
  digitalWrite(stopLED, HIGH);
  //heatLooping = false;

  return false;

}//end void send_w_ack


//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

void configure_lanes() {
  int ledState = HIGH;
  digitalWrite(goLED, ledState);
  digitalWrite(stopLED, ledState);
  unsigned long currentMillis = millis();
  unsigned long previousMillis = currentMillis;
  resetButtonState = digitalRead(resetButton);

  while (resetButtonState == HIGH) {

    currentMillis = millis();
    if (currentMillis - previousMillis > 500) {
      previousMillis = currentMillis;

      if (ledState == HIGH) {
        ledState = LOW;
      }
      else {
        ledState = HIGH;
      }
      digitalWrite(goLED, ledState);
      digitalWrite(stopLED, ledState);
    }

    //*****
    resetButtonState = digitalRead(resetButton);
    if (resetButtonState == LOW) {
      unsigned int voidState = 999;
      send_w_ack(nanoID, voidState, voidState, true);
      digitalWrite(goLED, LOW);
      digitalWrite(stopLED, HIGH);
      //*****

      //Once "send_w_ack" exits, the timer knows who it is
      //Now we reverse the acknowlwedgement - the receiver will ping the timer until the
      //receiver gets confirmation that the timer knows it's new lane assignment
        radio.flush_tx();
        radio.begin();
        radio.setAutoAck(false);
        radio.setDataRate(RF24_250KBPS);
        radio.setRetries(8, 15);
        radio.openWritingPipe(rxAddr);
        radio.openReadingPipe(1, myAdd);
        radio.flush_tx();
        radio.stopListening();
        Serial.print("nanoID = ");
        Serial.println(nanoID);
        Serial.print("laneID = ");
        Serial.println(laneID);
      while (true) {
        radio.startListening();
        if (radio.available())
        {
          //Serial.println("Incoming coolnes");
          unsigned int receivedMessage[3];
          radio.read(&receivedMessage, sizeof(receivedMessage));
          Serial.println(receivedMessage[0]);
          Serial.println(receivedMessage[1]);
          Serial.println(receivedMessage[2]);

//OPTION 1
          if (receivedMessage[0] == nanoID) {
            if (receivedMessage[2] == laneID) {

              //Stuff to confirm receipt of message for robustness
              radio.stopListening();
              radio.flush_tx();
              int confirmation[2];
              confirmation[0] = (int)receivedMessage[0];
              confirmation[1] = laneID;
              for (int z = 0; z < 5; z++) {
              radio.write(&confirmation, sizeof(confirmation));
              }
      
              //Serial.println("Sent Confirmation");
              radio.startListening();
            }//end laneID if
          }//end nanoID if

//OPTION 2
          if (receivedMessage[0] == exitConfigureCode) {
            break; //break out of while(true) and exit function
          }

          
        }//end if radio.available()


        currentMillis = millis();
          if (currentMillis - previousMillis > 500) {
          previousMillis = currentMillis;

          if (ledState == HIGH) {
          ledState = LOW;
          }
             else {
          ledState = HIGH;
          }
          digitalWrite(goLED, ledState);
          //digitalWrite(stopLED, ledState);
          }
          
        //radio.flush_tx();
        //radio.begin();
        //radio.setAutoAck(false);
        //radio.setDataRate(RF24_250KBPS);
        //radio.setRetries(8, 15);
        //radio.openWritingPipe(rxAddr);
        //radio.openReadingPipe(1, myAdd);
        //radio.flush_tx();
        //radio.stopListening();
        
        }//end while(true)

        radio.flush_tx();
        radio.begin();
        radio.setAutoAck(false);
        radio.setDataRate(RF24_250KBPS);
        radio.setRetries(8, 15);
        radio.openWritingPipe(rxAddr);
        radio.openReadingPipe(1, myAdd);
        radio.flush_tx();
        radio.stopListening();
        digitalWrite(goLED, LOW);
        digitalWrite(stopLED, HIGH);
        return; //out of while resetbutton
      }//end if (resetButtonState == LOW)
    }//end while resetButtonState == HIGH
    //resetButtonState should be high and break out of the while HIGH loop, allowing to exit function
}//end void configure_lanes

