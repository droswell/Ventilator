from matplotlib import pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import random
import serial

ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

#engineer_salaries = [38000, 42000, 46573, 49320, 53200, 56000, 62134, 64928, 67317, 68748, 73752]
#scientist_salaries = [45372, 48875, 53580, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]

x_vals = []
y_vals = []


fig = plt.figure()
plt.style.use('dark_background')
#plt.rcParams['axes.facecolor'] = 'g'

index = count()


#plt.plot(ages_x, engineer_salaries, label="Engineer Salaries", color='#64e3ff')
#plt.plot(ages_x, scientist_salaries, label="Scientist Salaries", color='#ff9e2d')

def GetVals(self):
    s = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
    try:
        if s.inWaiting() > 0:
            inputValue = s.readline()
            formattedinputvalue = inputValue.strip()
            encodedvalue = formattedinputvalue.decode('utf-8')
            splitstring = encodedvalue.split(',')

            if (splitstring[0] == 'PA'):
                PA = int(splitstring[1])
            else:
                splitstring[1] = '0'
                # Bad Data, discard
                print('Received bad data')

            print(splitstring[0])
            print(PA)
            s.flush()
    except:
        print("Failed to receive")
    #return int(splitstring[1])
    return PA


def animate(i):
    data = GetVals()
    x_vals.append(random.randint(0, 5))
    y_vals.append(GetVals())
    plt.cla()
    plt.plot(x_vals, y_vals)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.ylabel("Y Label")
plt.xlabel("X Label")
plt.title("Title of Plot")


plt.show()