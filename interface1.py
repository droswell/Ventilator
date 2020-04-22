import serial
from tkinter import *
from threading import Thread

VentilatorStatus = False


port = '/dev/ttyACM1'
rate = 9600

totalvolume = 500
ser = serial.Serial(port, rate, writeTimeout=0)
ser.flushInput()

comp_list=["Hello Pi, this is arduino uno"]
compare = "Hello Pi, this is arduino uno"





def validatetotalvolumevalue(mintv, maxtv, tv):
    result = False
    if(tv > mintv and tv < maxtv):
        result = True
    return result

def GetSerialData():
    global tv_stringvar

    while True:
        if ser.inWaiting() > 0:
            inputValue = ser.readline()
            formattedinputvalue = inputValue.strip()
            encodedvalue = formattedinputvalue.decode('utf-8')
            tv_stringvar.set(encodedvalue)
    root.after(1, GetSerialData)




t = Thread(target=GetSerialData)
t.start()


root = Tk()
root.geometry("1024x768")
root.title("Test1")

tv_stringvar = StringVar()

tv_label = Label(root, textvariable=tv_stringvar, width=25, relief="sunken")
tv_label.pack()


root.after(100, GetSerialData)
root.mainloop()