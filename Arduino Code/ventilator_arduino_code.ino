#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display


//Variables for receiving data from USB:
String inputString = ""; 
String temp = "";
String volumeString = "";
String breathString = "";
String peepString = "";
String ratioString = "";
String oxygenString = "";
String alarmString = "";
String statusString = "";
String temp_string = "";

//Misc Variables:
int a = 0;
int volume = 0;
int breath = 12;
int peep = 5;
int ratio = 1;
int oxygen = 21;
int alarm = 30;
int stringlength = 0;
int ventStatus = 0;


int i=0;

char string[32];
char byteRead;

const int PAPin = A0; 
const int PBPin = A1; 
const int PCPin = A2; 
int PA = 0;
int PB = 0;
int PC = 0;

int serialdata = 0;
bool stringComplete = false; 


void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  //Serial.println("Hello Pi, this is arduino uno");

  // LCD Stuff
  lcd.init(); 
  lcd.backlight();

}


void loop() 
{
    // Read Sensors, store in variables
    PA = analogRead(PAPin);
    PB = analogRead(PBPin);
    PC = analogRead(PCPin);

    // Send the data out the serial port
    //Serial.print(i);
    //Serial.print(",");
    Serial.print("PA,");
    Serial.println(PA);
    Serial.print("PB,");
    Serial.println(PB);
    Serial.print("PC,");
    Serial.println(PC);


    i++;
    
    // Read the serial port
    serialEvent();



    if (stringComplete) 
    {
      temp = inputString.charAt(0); 
      stringlength = inputString.length();
      
      volumeString ="";
      breathString = "";
      peepString = "";
      ratioString = "";
      oxygenString = "";
      alarmString = "";
      statusString = "";
      
      if (temp == "t") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          volumeString += temp_string;
        }
        volume = volumeString.toInt();  
        WriteToLCD4(temp,volumeString);
        
      }
      else if (temp == "s") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          statusString += temp_string;
        }
        ventStatus = statusString.toInt();  
        WriteToLCD4(temp,statusString);

      }
      else if (temp == "b") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          breathString += temp_string;
        }
        breath = breathString.toInt();  
        WriteToLCD4(temp,breathString);

      }
      else if (temp == "p") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          peepString += temp_string;
        }
        peep = peepString.toInt();  
        Serial.println(peep);
        WriteToLCD4(temp,peepString);
      }
      else if (temp == "o") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          oxygenString += temp_string;
        }
        oxygen = oxygenString.toInt();  
        Serial.println(oxygen);
        WriteToLCD4(temp,oxygenString);
      }
      else if (temp == "r") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          ratioString += temp_string;
        }
        ratio = ratioString.toInt();  
        WriteToLCD4(temp,ratioString);
      }
      else if (temp == "a") 
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          alarmString += temp_string;
        }
        alarm = alarmString.toInt();  
        Serial.println(alarm);
        WriteToLCD4(temp,alarmString);
      }    
      else
      {
        WriteToLCD4("na","na");        
      }
      
      // clear the string:
      inputString = "";
      stringComplete = false;
    }
           
    

    delay(50);
}

void WriteToLCD2(String command)
{
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Command: ");
      lcd.print(command);
}

void WriteToLCD4(String command, String value)
{
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Command: ");
      lcd.print(command);
      lcd.setCursor(0,1);
      lcd.print("Value: ");
      lcd.print(value);

}
void WriteToLCD3(int value)
{
      //lcd.setCursor(1,0);
      lcd.print("Value: ");
      lcd.print(value);
}

void WriteToLCD(String command, int value)
{
      //lcd.clear();
      lcd.setCursor(0,0);
      //lcd.print("Received:");
      //lcd.setCursor(0,1);
      lcd.print("Command: ");
      lcd.print(command);
      //lcd.setCursor(0,2);
      //lcd.print("Value: ");
      //lcd.print(value);
}




void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
