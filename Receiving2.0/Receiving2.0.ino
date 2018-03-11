#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

int button = 9;
unsigned int t1 = 0;
unsigned int t2 = 0;
bool buttonState;
int startSignal = 666;
unsigned int confirmationCode = 24;
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
       if (state == 1){ //If correct signal is received, begin doing stuff
        
          radio.write(&startSignal, sizeof(startSignal));
          
         // t1 = millis();
          //Serial.println("Sent Stuff");
          break;
      }
    }
  }


  //After Sending Stuff, setup radio for listening
  digitalWrite(LED, LOW);
  
  
  radio.startListening();

  //Listening for crap to come in
  bool heatFinish = false;
  
  while (heatFinish == false){
    if (radio.available())
      {
      //char t[32] = {0};
      unsigned int receivedMessage[3];
      radio.read(&receivedMessage, sizeof(receivedMessage));

      //Stuff to confirm receipt of message for robustness
      radio.stopListening();
      unsigned int confirmation[2];
      confirmation[0] = receivedMessage[0];
      confirmation[1] = confirmationCode;
      radio.write(&confirmation, sizeof(confirmation));
      radio.startListening;
      
      
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
  
}
