#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

int button = 9;
unsigned int t1 = 0;
unsigned int t2 = 0;
bool buttonState;
int startSignal = 666;
int confirmationCode = 24;
int configureCode    = 33;
unsigned long t = 0;
int LED = 30;

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
  radio.setRetries(8,15);
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
  
  while (true){
  //Wait to receive signal to send start time signal
    if (Serial.available()){
       int state = Serial.read() - '0';
       
       if (state == 33){ //If "CONFIGURE" signal, do that
        Serial.println("Configuring lanes");
        configure_lanes();
       }
       
       if (state == 1){ //If correct start signal is received, begin doing stuff
          radio.write(&startSignal, sizeof(startSignal));
          radio.write(&startSignal, sizeof(startSignal));
          radio.write(&startSignal, sizeof(startSignal));
          radio.write(&startSignal, sizeof(startSignal));
          radio.write(&startSignal, sizeof(startSignal));
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
      
  while (heatFinish == false){
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
      //Serial.println("Sent Confirmation");
      radio.startListening();


      
      
      //t2 = millis() - t1;
      String messageToSend = "";
      messageToSend = (String)receivedMessage[0] + " " + (String)receivedMessage[1] + " " + (String)receivedMessage[2];
      //Serial.print("Shane Time = ");
      Serial.println(messageToSend);
      //Serial.print("My Time = ");
      //Serial.println(t2);
      }
      
      if (Serial.available()){
        
       int state = Serial.read() - '0';
       if (state == 9){ //If correct signal is received, begin doing stuff
          heatFinish = true;
          //digitalWrite(LED, HIGH);
        }
      }
  }

  digitalWrite(LED, HIGH);


 
  radio.stopListening();
  radio.flush_tx();
  
}

void configure_lanes(){
  bool LED_state = HIGH;
  unsigned long start_time = millis();
  digitalWrite(LED, LED_state);
  
  int lane_count = 0;
  
  if (Serial.available()){
       lane_count = Serial.read() - '0';
  }

  //Broadcast "CONFIGURE" signal
  radio.setRetries(8,15);
  radio.stopListening();
  radio.flush_tx();
  radio.write(&configureCode, sizeof(configureCode));
  radio.startListening();

  //Loop while listening for lanes
  int lanes_received = 1;
  while (lanes_received <= lane_count){

    //LED stuff
    unsigned long new_time = millis();
    if (new_time - start_time >= 500){
      start_time = new_time;
      if (LED_state == LOW) {
      LED_state = HIGH;
    } else {
      LED_state = LOW;
    }
    digitalWrite(LED, LED_state);  
    }//End LED stuff
    
      if (radio.available()){
      unsigned int timerID;
      radio.read(&timerID, sizeof(timerID));
      //Send out confirmation
      radio.stopListening();
      radio.flush_tx();
      unsigned int assignment[3];
      assignment[0] = timerID;
      assignment[1] = confirmationCode;
      assignment[2] = lanes_received;
      radio.write(&assignment, sizeof(assignment));
      Serial.println("Lane 1 Sent");
      radio.startListening();
  }
  
  }
  
}



