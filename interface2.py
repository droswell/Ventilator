import serial
import threading
import time
import queue
from tkinter import *


class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        s = serial.Serial('/dev/ttyACM1', 9600)
        #s.write(str.encode('*00T%'))
        time.sleep(0.2)
        while True:
            if s.inWaiting() > 0:
                inputValue = s.readline()
                formattedinputvalue = inputValue.strip()
                encodedvalue = formattedinputvalue.decode('utf-8')
                self.queue.put(encodedvalue)

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1360x750")
        frameLabel = LabelFrame(self, padx=40, pady=40)
        self.text = Entry(frameLabel, font='TimesNewRoman 37', bg=self.cget('bg'), relief='flat')
        #self.text = Tk.Text(frameLabel, wrap='word', font='TimesNewRoman 37', bg=self.cget('bg'), relief='flat')
        frameLabel.pack()
        self.text.pack()
        self.queue = queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    def process_serial(self):
        value=True
        while self.queue.qsize():
            try:
                new=self.queue.get()
                if value:
                 self.text.delete(1.0, 'end')
                 value=False
                 self.text.insert('end',new)
            except queue.Empty:
                pass
        self.after(100, self.process_serial)

app = App()
app.mainloop()