#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

//===========================================
// Command Codes - For Sending to the Arduino
//===========================================
// RR - Respiratory Rate (int, 10-20)  breaths per minute
// IR - Inspiratory Rate (float 0.1 - 5.0) seconds
// PEEP - PEEP (int 0-20) cm H2O
// O2 - Oxygen Percentage (0-100) %
// TV - Tidal Volume (int 200-2500) ml
// Status - Ventilator enabled/disabled
// PatientPressure - Patient pressure
// FlowSensor - Air/02 flow being delivered to patient

//=====================================
// Variables for important data
//=====================================
int RR = 0;
int IR = 0;
int PEEP = 0;
int O2 = 0;
int TV = 0;
int Status = 0;
int PatientPressure = 0;
int FlowSensor = 0;
String inputString = "";
String temp = "";
String temp_string = "";
int stringlength = 0;


//=============================================
// String variables for receiving data from USB
//=============================================
String RRstring = "";
String IRstring = "";
String PEEPstring = "";
String O2string = "";
String TVstring = "";
String Statusstring = "";
String PatientPressureString = "";
String FlowSensorString = "";

// How many ms delay in the loop
int LoopDelay = 1000;

//===================
// Some Pin Constants
//===================
const int PatientPressurePin = A0;
const int FlowSensorPin = A1;

//=========================================================
// This variable goes high when we get a newline
// in the serial data, signifying the end of a valid packet
//=========================================================
bool stringComplete = false;




void setup() {
  // Open the serial port to send data
  Serial.begin(9600);

  // LCD Display
  lcd.init();
  lcd.backlight();
}


void loop()
{
    //==================================
    // Read Sensors, store in variables
    //==================================
    PatientPressure = analogRead(PatientPressurePin);
    FlowSensor = analogRead(FlowSensorPin);

    //==================================
    // Send the data out the serial port
    //==================================
    Serial.print("RR,");
    Serial.println(RR);
    Serial.print("IR,");
    Serial.println(IR);
    Serial.print("PEEP,");
    Serial.println(PEEP);
    Serial.print("O2,");
    Serial.println(O2);
    Serial.print("TV,");
    Serial.println(TV);
    Serial.print("Status,");
    Serial.println(Status);
    Serial.print("PatientPressure,");
    Serial.println(PatientPressure);
    Serial.print("FlowSensor,");
    Serial.println(FlowSensor);

    //==================================
    // Read the serial port data
    //==================================
    serialEvent();

    // Wait for a newline from the PI
    if (stringComplete)
    {
      temp = inputString.charAt(0);
      stringlength = inputString.length();

      // Clear the command strings
      RRstring = "";
      IRstring = "";
      PEEPstring = "";
      O2string = "";
      TVstring = "";
      Statusstring = "";
      PatientPressureString = "";
      FlowSensorString = "";

      //==================================================
      // Parse the command code so we can update the value
      //==================================================
      // R is for Respiration Rate
      if (temp == "R")
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          RRstring += temp_string;
        }
        RR = RRstring.toInt();
        //WriteToLCD();
      }
      // I is for Inspiration Rate
      else if (temp == "I")
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          IRstring += temp_string;
        }
        IR = IRstring.toInt();
      }
      // E is for PEEP
      else if (temp == "E")
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          PEEPstring += temp_string;
        }
        PEEP = PEEPstring.toInt();
      }
      // O is for FiO2
      else if (temp == "O")
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          O2string += temp_string;
        }
        O2 = O2string.toInt();
      }
      // T is for Tidal Volume (TV)
      else if (temp == "T")
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          TVstring += temp_string;
        }
        TV = TVstring.toInt();
      }
      // S is for Ventilator Status
      else if (temp == "S")
      {
        for (int i = 1; i <= stringlength; i = i + 1)
        {
          temp_string = inputString.charAt(i);
          Statusstring += temp_string;
        }
        Status = Statusstring.toInt();
      }
      else
      {
        //WriteToLCD4("na","na");
      }

      // clear the string:
      inputString = "";
      stringComplete = false;
    }

    WriteToLCD();
    delay(LoopDelay);
}


void WriteToLCD()
{
      lcd.clear();

      lcd.setCursor(0,0);
      lcd.print("RR:");
      lcd.print("20");

      lcd.setCursor(0,1);
      lcd.print("IR:");
      lcd.print("1.7");

      lcd.setCursor(0,2);
      lcd.print("0X:");
      lcd.print("100%");

      lcd.setCursor(0,3);
      lcd.print("PEEP:");
      lcd.print("13"); 

      lcd.setCursor(9,0);
      lcd.print("Press.:");
      lcd.print("1023");

      lcd.setCursor(10,1);
      lcd.print("Status:");
      lcd.print("Off");

      lcd.setCursor(11,2);
      lcd.print("Flow:");
      lcd.print("1023");

      lcd.setCursor(13,3);
      lcd.print("TV:");
      lcd.print("1500");
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