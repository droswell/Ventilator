import serial

port = '/dev/ttyACM1'
rate = 9600

ser = serial.Serial(port, rate)
ser.flushInput()

comp_list=["Hello Pi, this is arduino uno"]
compare = "Hello Pi, this is arduino uno"

while True:
    if ser.inWaiting() > 0:
        #inputValue = ser.readline().decode('utf-8')
        inputValue = ser.readline()
        formattedinputvalue = inputValue.strip()
        #print(inputValue)
        encodedvalue = formattedinputvalue.decode('utf-8')
        print(encodedvalue)

        if(encodedvalue == compare):
            print("Match!")
            try:
                n = input("1 for on, 2 for off: ")
                datatosend = n.encode()
                ser.write(datatosend)
            except:
                print("Input error, please input a number")
                sendazero = '0'.encode()
                ser.write(sendazero)
