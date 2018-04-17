#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

int button = 9;
unsigned int t1 = 0;
unsigned int t2 = 0;
bool buttonState;
int startSignal = 666;
unsigned int confirmationCode = 24;
int configureCode    = 33;
unsigned long t = 0;
int LED = 9;
int exitConfigureCode = 12345;

RF24 radio(7, 8);

const uint64_t rxAddr = 0xF0F0F0F0E1LL;
const uint64_t txAddr = 0x28;

void setup()
{
  pinMode(button, INPUT_PULLUP);
  pinMode(LED, OUTPUT);

  while (!Serial);
  Serial.begin(9600);

  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(8, 15);
  radio.openReadingPipe(1, rxAddr);
  radio.openWritingPipe(txAddr);
  radio.stopListening();
  radio.flush_tx();

  Serial.println("Ready");

  t = millis();
}

void loop()
{
  //radio.openWritingPipe(rxAddr);
  //radio.stopListening();
  //Waiting to send some crap
  digitalWrite(LED, HIGH);

  while (true) {
    //Wait to receive signal to send start time signal
    if (Serial.available()) {
      int state = Serial.read() - '0';

      if (state == 33) { //If "CONFIGURE" signal, do that
        //Serial.println("Configuring lanes");
        configure_lanes();
      }

      if (state == 1) { //If correct start signal is received, begin doing stuff
        for (int k = 0; k < 100; k++){
        radio.write(&startSignal, sizeof(startSignal));
        }

        digitalWrite(LED, LOW);

        // t1 = millis();
        //Serial.println("Sent Stuff");
        break;
      }
    }
  }


  //After Sending Stuff, setup radio for listening
  
  radio.startListening();

  //Listening for crap to come in
  bool heatFinish = false;


  //Serial.println("Received Stop Time");

  while (heatFinish == false) {
    if (radio.available())
    {
      //char t[32] = {0};
      unsigned int receivedMessage[3];
      radio.read(&receivedMessage, sizeof(receivedMessage));


      //Stuff to confirm receipt of message for robustness
      radio.stopListening();
      radio.flush_tx();
      int confirmation[2];
      confirmation[0] = (int)receivedMessage[0];
      confirmation[1] = confirmationCode;
      radio.write(&confirmation, sizeof(confirmation));
      radio.write(&confirmation, sizeof(confirmation));
      radio.write(&confirmation, sizeof(confirmation));
      //      digitalWrite(LED,HIGH);
      //      delay(100);
      //      digitalWrite(LED,LOW);
      //      delay(100);
      //      digitalWrite(LED,HIGH);
      //      delay(100);
      //      digitalWrite(LED,LOW);
      radio.startListening();

      String messageToSend = (String)receivedMessage[0] + " " + (String)receivedMessage[1] + " " + (String)receivedMessage[2];
      //Serial.print("Shane Time = ");
      Serial.println(messageToSend);
      //Serial.print("My Time = ");
      //Serial.println(t2);
    }

    if (Serial.available()) {

      int state = Serial.read() - '0';
      if (state == 9) { //If correct signal is received, begin doing stuff
        heatFinish = true;
        //digitalWrite(LED, HIGH);
        radio.begin();
        radio.setAutoAck(false);
        radio.setDataRate(RF24_250KBPS);
        radio.setRetries(8, 15);
        radio.openReadingPipe(1, rxAddr);
        radio.openWritingPipe(txAddr);
        radio.stopListening();
        radio.flush_tx();
        //Serial.flush();
      }
    }
  }

  digitalWrite(LED, HIGH);



  radio.stopListening();
  radio.flush_tx();

}

void configure_lanes() {
  bool LED_state = HIGH;
  unsigned long start_time = millis();
  digitalWrite(LED, LED_state);

  unsigned int lane_count = 0;

  while (true) {
    if (Serial.available()) {
      lane_count = Serial.read() - '0';
      break;
    }
  }//end while(true)

  //Broadcast "CONFIGURE" signal
  radio.stopListening();
  radio.flush_tx();
  for (int k = 0; k < 100; k++){
     radio.write(&configureCode, sizeof(configureCode));
     } 

  radio.startListening();

  //Loop while listening for lanes
  for (unsigned int lanes_received = 1; lanes_received <= lane_count; lanes_received++) {
    bool waiting = true;
    while (waiting == true){
    //LED stuff- - - - - - - - - - - - - - -
    unsigned long new_time = millis();
      if (new_time - start_time >= 500) {
        start_time = new_time;
        if (LED_state == LOW) {
          LED_state = HIGH;
        } else {
          LED_state = LOW;
        }
      digitalWrite(LED, LED_state);
    }//End LED stuff- - - - - - - - - - - -

    if (radio.available()) {
      unsigned int incoming[3];
      radio.read(&incoming, sizeof(incoming));
      unsigned int nanoID = incoming[0];
      unsigned int void1  = incoming[1];
      unsigned int void2  = incoming[2];
      //Send out confirmation
      radio.stopListening();
      radio.flush_tx();
      
      //We need to loop, telling the timer it's new identity until the receiver gets confirmation that the timer knows who it is
      send_w_ack(nanoID, confirmationCode, lanes_received);

      Serial.println("adfasdfasdfasdfmissiveasdfasdfasdfasdf");
      waiting = false;
      radio.startListening();
    }//end radio.available() if statement
    }//end while waiting == true

  }//end lane assignment for loop

  //Send massive broadcast to end this configuration madness once & for all!
  unsigned int apocalypse[3] = {exitConfigureCode, exitConfigureCode, exitConfigureCode};
  radio.stopListening();
  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(8, 15);
  radio.openReadingPipe(1, rxAddr);
  radio.openWritingPipe(txAddr);
  radio.stopListening();
  radio.flush_tx();

  //I meant MASSIVE!!!!!!!!!!!!!!!
  for (int z = 0; z < 500; z++) {
    radio.write(&apocalypse, sizeof(apocalypse));
  }


  radio.begin();
  radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.setRetries(8, 15);
  radio.openReadingPipe(1, rxAddr);
  radio.openWritingPipe(txAddr);
  radio.stopListening();
  radio.flush_tx();
  
}//end configure_lanes

//---------------------------------------------------------------------------------------------

bool send_w_ack(unsigned int &a, unsigned int &b, unsigned int &c) {

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

        int conf[2];

        Serial.println("RADIO WAS AVAIALABLE");
        radio.read(&conf, sizeof(conf));
        Serial.println(conf[0]);
        Serial.println(conf[1]);

        if ((conf[0]) == a) {
          //Serial.println("correct identifier");
          if ((conf[1]) == c) {
            //Serial.println("correct confirmationCode");
            successfulComms = true;
            break; //Break out of && while loop, we're good
          }//End confirmation if
        }// End identifier if

      }//end radio.available() if

      listenTime = millis() - startListenTime;

    }// End successfulComm && listenTime for confirmation while

  }//end while (successfulComms == false)

  return false;

}//end void send_w_ack

