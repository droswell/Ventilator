import serial

port = '/dev/ttyACM1'
rate = 9600

totalvolume = 500


def validatetotalvolumevalue(mintv, maxtv, tv):
    result = False
    if(tv > mintv and tv < maxtv):
        result = True
    return result



ser = serial.Serial(port, rate)
ser.flushInput()

comp_list=["Hello Pi, this is arduino uno"]
compare = "Hello Pi, this is arduino uno"

while True:
    if ser.inWaiting() > 0:
        inputValue = ser.readline()
        formattedinputvalue = inputValue.strip()
        encodedvalue = formattedinputvalue.decode('utf-8')
        print(encodedvalue)

    #try:
    #   totalvolume = input("1 for on, 2 for off: ")
    #   datatosend = totalvolume.encode()
    #   ser.write(datatosend)
    #except:
    #   print("Input error, please input a number")
    #   sendazero = '0'.encode()
    #   ser.write(sendazero)
    #   break

