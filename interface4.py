import sys
import tkinter
import tkinter.messagebox
import time
import _thread
import serial
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.animation as animation



# --------------------------------------------
# LIST OF ALL SENSORS AND SIGNALS
# --------------------------------------------
PA = 0  # Supply line pressure sensor
PB = 0  # Regulated air line pressure sensor
PC = 0  # Patient pressure sensor
ER1 = 0  # Air regulator solenoid
ER2 = 0  # O2 regulator solenoid
FM1 = 0  # Air/O2 flow sensor
EV1 = 0  # Inhalation electronic valve (N.C.)
EV2 = 0  # Exhalation electronic valve (N.O.)
PEEP1 = 0  # PEEP regulator solenoid
# --------------------------------------------


# --------------------------------------------
# SOME LIMITS FOR PARAMETERS
# --------------------------------------------
PEEPmax = 15     # No extrinsic PEEP
PEEPmin = 0    # High PEEP
RRmax = 20      # Max of 20 breaths per minute
RRmin = 10      # Min of 10 breaths per minute
FI02max = 100   # 100% O2
FI02min = 0     # 0% 02
TVmax = 2500    # Maximum Total volume in ml
TVmin = 500     #  Minimum Total volume in ml


# --------------------------------------------
# STARTUP SETTINGS
# --------------------------------------------
PEEP = 4    # Start with 4 cm H20
RR = 15     # Start with 15 bpm
FI02 = 0    # Start with 0% oxygenation
TV = 1000   # Global Total Volume Variable


class Menu:


    def __init__(self):
        global PEEP
        global RR
        global FI02
        global TV

        global fig
        global ax

        # Main application window
        self.main_window = tkinter.Tk()
        self.main_window.title("Serial Data monitor")
        w, h = self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
        self.main_window.geometry("%dx%d+0+0" % (w, h))
        self.main_window.config(bg='#0c0c0c')

        # Make the application scale properly
        self.main_window.grid_columnconfigure(0, weight=0)
        self.main_window.grid_columnconfigure(1, weight=100)








        # Variables to Display Data
        self.PAValue = tkinter.StringVar()
        self.PBValue = tkinter.StringVar()
        self.PCValue = tkinter.StringVar()

        self.PEEP = tkinter.StringVar()
        self.PEEP.set(str(PEEP))

        self.RR = tkinter.StringVar()
        self.RR.set(str(RR))

        self.FI02 = tkinter.StringVar()
        self.FI02.set(str(FI02))

        self.TV = tkinter.StringVar()
        self.TV.set(str(TV))


        # Left Frame
        self.LeftFrame = tkinter.LabelFrame(self.main_window, borderwidth=0, font=("Arial", 18, "bold"), bg="#0c0c0c")
        self.LeftFrame.grid(row=0, column=0, sticky='NSEW', padx=10, pady=(10, 0))

        #-----------
        # PEEP FRAME
        #-----------
        # Columns 0/1 Row 0
        self.PEEPFrame = tkinter.LabelFrame(self.LeftFrame, borderwidth=1, relief="sunken", fg='#f2f2f2', bg="#3f3f3f", highlightbackground='#595959')
        self.PEEPFrame.grid(row=0, column=0, sticky='NSEW', padx=20, pady=(10, 10))

        # Column 0, Rows 0
        # Title of Frame Area
        self.PEEPTitle = tkinter.Label(self.PEEPFrame, text="PEEP", bg="#262626", fg='#f2f2f2',  font=("Arial", 12))
        self.PEEPTitle.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8)

        # Column 0, Rows 1/2
        # Display PEEP Data
        self.PEEPValue = tkinter.Label(self.PEEPFrame, textvariable=self.PEEP, bg="#3f3f3f",  fg='#ffffff', font=("Arial", 56))
        self.PEEPValue.grid(column=0, row=1, rowspan=2, padx=10, pady=(0,20))
        self.PEEPlabel = tkinter.Label(self.PEEPFrame, text="cm H20", bg="#3f3f3f",  fg='#ffffff', font=("Arial", 10), width=25)
        self.PEEPlabel.grid(column=0, row=1, rowspan=2, pady=(65, 0))

        # Column 1, Row 1
        self.btnIncreasePEEP = tkinter.Button(self.PEEPFrame, command=self.IncreasePEEP, text="+", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnIncreasePEEP.grid(column=1, row = 1, padx=10, pady=(15, 8))

        # Column 1, Row 2
        self.btnDecreasePEEP = tkinter.Button(self.PEEPFrame, command=self.DecreasePEEP, text="-", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnDecreasePEEP.grid(column=1, row = 2, padx=10, pady=(8, 15))


        #------------------------
        # RESPIRATION RATE FRAME
        #------------------------
        # Columns 0/1 Row 0
        self.RRFrame = tkinter.LabelFrame(self.LeftFrame, borderwidth=1, relief="sunken", fg='#f2f2f2', bg="#3f3f3f", highlightbackground='#595959')
        self.RRFrame.grid(row=1, column=0, sticky='NSEW', padx=20, pady=10)

        # Column 0, Rows 0
        # Title of Frame Area
        self.RRTitle = tkinter.Label(self.RRFrame, text="Respiration Rate", bg="#262626", fg='#f2f2f2',  font=("Arial", 12))
        self.RRTitle.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8)

        # Column 0, Rows 1/2
        # Display Respiration Rate Data
        self.RRValue = tkinter.Label(self.RRFrame, textvariable=self.RR, bg="#3f3f3f",  fg='#92d050', font=("Arial", 56))
        self.RRValue.grid(column=0, row=1, rowspan=2, padx=10, pady=(0, 20))
        self.RRlabel = tkinter.Label(self.RRFrame, text="Breaths Per Minute", bg="#3f3f3f",  fg='#92d050', font=("Arial", 10), width=25)
        self.RRlabel.grid(column=0, row=1, rowspan=2, pady=(70, 0))

        # Column 1, Row 1
        self.btnIncreaseRR = tkinter.Button(self.RRFrame, command=self.IncreaseRR, repeatinterval=50, repeatdelay=150, text="+", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnIncreaseRR.grid(column=1, row = 1, padx=10, pady=(15, 8))

        # Column 1, Row 2
        self.btnDecreaseRR = tkinter.Button(self.RRFrame, command=self.DecreaseRR, repeatinterval=50, repeatdelay=150, text="-", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnDecreaseRR.grid(column=1, row = 2, padx=10, pady=(8, 15))


        #------------------------
        # INSPIRATION RATE FRAME
        #------------------------
        # Columns 0/1 Row 0
        self.IRFrame = tkinter.LabelFrame(self.LeftFrame, borderwidth=1, relief="sunken", fg='#f2f2f2', bg="#3f3f3f", highlightbackground='#595959')
        self.IRFrame.grid(row=2, column=0, sticky='NSEW', padx=20, pady=10)

        # Column 0, Rows 0
        # Title of Frame Area
        self.IRTitle = tkinter.Label(self.IRFrame, text="Inspiration Rate", bg="#262626", fg='#f2f2f2',  font=("Arial", 12))
        self.IRTitle.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8)

        # Column 0, Rows 1/2
        # Display Inspiration Rate Data
        self.IRValue = tkinter.Label(self.IRFrame, textvariable=self.PCValue, bg="#3f3f3f",  fg='#fc9b2a', font=("Arial", 56))
        self.IRValue.grid(column=0, row=1, rowspan=2, padx=10, pady=(0, 20))
        self.IRlabel = tkinter.Label(self.IRFrame, text="Seconds", bg="#3f3f3f",  fg='#fc9b2a', font=("Arial", 10), width=25)
        self.IRlabel.grid(column=0, row=1, rowspan=2, pady=(70, 0))

        # Column 1, Row 1
        self.btnIncreaseIR = tkinter.Button(self.IRFrame, text="+", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnIncreaseIR.grid(column=1, row = 1, padx=10, pady=(15, 8))

        # Column 1, Row 2
        self.btnDecreaseIR = tkinter.Button(self.IRFrame, text="-", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnDecreaseIR.grid(column=1, row = 2, padx=10, pady=(8, 15))


        #------------------------
        # FI02 FRAME
        #------------------------
        # Columns 0/1 Row 0
        self.FI02Frame = tkinter.LabelFrame(self.LeftFrame, borderwidth=1, relief="sunken", fg='#f2f2f2', bg="#3f3f3f", highlightbackground='#595959')
        self.FI02Frame.grid(row=3, column=0, sticky='NSEW', padx=20, pady=10)

        # Column 0, Rows 0
        # Title of Frame Area
        self.FI02Title = tkinter.Label(self.FI02Frame, text="FI02", bg="#262626", fg='#f2f2f2',  font=("Arial", 12))
        self.FI02Title.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8)

        # Column 0, Rows 1/2
        # Display FI02 Data
        self.FI02Value = tkinter.Label(self.FI02Frame, textvariable=self.FI02, bg="#3f3f3f",  fg='#6ae8ff', font=("Arial", 56))
        self.FI02Value.grid(column=0, row=1, rowspan=2, padx=10, pady=(0, 20))
        self.FI02label = tkinter.Label(self.FI02Frame, text="% Oxygen", bg="#3f3f3f",  fg='#6ae8ff', font=("Arial", 10), width=25)
        self.FI02label.grid(column=0, row=1, rowspan=2, pady=(70, 0))

        # Column 1, Row 1
        self.btnIncreaseFI02 = tkinter.Button(self.FI02Frame, command=self.IncreaseO2, repeatinterval=35, repeatdelay=125, text="+", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnIncreaseFI02.grid(column=1, row = 1, padx=10, pady=(15, 8))

        # Column 1, Row 2
        self.btnDecreaseFI02 = tkinter.Button(self.FI02Frame,command=self.DecreaseO2, repeatinterval=35, repeatdelay=125, text="-", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnDecreaseFI02.grid(column=1, row = 2, padx=10, pady=(8, 15))



        #------------------------
        # Total Volume FRAME
        #------------------------
        # Columns 0/1 Row 0
        self.TVFrame = tkinter.LabelFrame(self.LeftFrame, borderwidth=1, relief="sunken", fg='#f2f2f2', bg="#3f3f3f", highlightbackground='#595959')
        self.TVFrame.grid(row=4, column=0, sticky='NSEW', padx=20, pady=(10,20))

        # Column 0, Rows 0
        # Title of Frame Area
        self.TVTitle = tkinter.Label(self.TVFrame, text="Total Volume", bg="#262626", fg='#f2f2f2',  font=("Arial", 12))
        self.TVTitle.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8)

        # Column 0, Rows 1/2
        # Display FI02 Data
        self.TVValue = tkinter.Label(self.TVFrame, textvariable=self.TV, bg="#3f3f3f",  fg='#ffffff', font=("Arial", 48))
        self.TVValue.grid(column=0, row=1, rowspan=2, padx=10, pady=(0, 20))
        self.TVlabel = tkinter.Label(self.TVFrame, text="millileters", bg="#3f3f3f",  fg='#ffffff', font=("Arial", 10), width=25)
        self.TVlabel.grid(column=0, row=1, rowspan=2, pady=(70, 0))

        # Column 1, Row 1
        self.btnIncreaseTV = tkinter.Button(self.TVFrame, command=self.IncreaseTV, repeatinterval=35, repeatdelay=125, text="+", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnIncreaseTV.grid(column=1, row = 1, padx=10, pady=(15, 8))

        # Column 1, Row 2
        self.btnDecreaseTV = tkinter.Button(self.TVFrame, command=self.DecreaseTV, repeatinterval=35, repeatdelay=125, text="-", width=2, bg="#7f7f7f", font=("Arial", 20, "bold"))
        self.btnDecreaseTV.grid(column=1, row = 2, padx=10, pady=(8, 15))


        # Right Frame
        self.RightFrame = tkinter.LabelFrame(self.main_window, borderwidth=0, bg="#262626", width=110)
        self.RightFrame.grid(row=0, column=1, sticky='NSEW', padx=(0,10), pady=10)

        self.RightFrameRow0 = tkinter.LabelFrame(self.RightFrame, borderwidth=0, bg="red")
        self.RightFrameRow0.grid(row=0, column=0, sticky='NSEW', padx=(0,10), pady=10)






        self.RightFrameRow1 = tkinter.LabelFrame(self.RightFrame, borderwidth=0, bg="blue")
        self.RightFrameRow1.grid(row=1, column=0, sticky='NSEW', padx=(0,10), pady=10)
        self.test2 = tkinter.Label(self.RightFrameRow1, text="Test2", bg="#262626", fg='#f2f2f2')
        self.test2.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8, padx=20, pady=20)

        self.RightFrameRow2 = tkinter.LabelFrame(self.RightFrame, borderwidth=0, bg="green")
        self.RightFrameRow2.grid(row=2, column=0, sticky='NSEW', padx=(0,10), pady=10)
        self.test3 = tkinter.Label(self.RightFrameRow2, text="Test3", bg="#262626", fg='#f2f2f2')
        self.test3.grid(row=0, column=0, columnspan=2, sticky='ewns', ipady=8, padx=20, pady=20)


        # Make the application scale properly
        self.RightFrameRow0.grid_rowconfigure(0, weight=1)
        self.RightFrameRow1.grid_rowconfigure(1, weight=1)
        self.RightFrameRow2.grid_rowconfigure(2, weight=1)




        #main loop and quit
        #self.quitButton = tkinter.Button(self.main_window, text='Quit', command=self.main_window.destroy, height=2, width=6)
        #self.quitButton.pack()
        #self.quitButton.place(x=200, y=500)


        self.main_window.after(50, _thread.start_new_thread, self.GetSerialData, ())
        tkinter.mainloop()




    #-----------------------------------------------
    # Functions to send data to the controller
    #-----------------------------------------------
    def open_serial(self):
        baudrate = 9600
        timeout = 5
        port = '/dev/ttyACM0'
        if port == None:
            return None
        else:
            ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            if (not ser.is_open):
                ser.open()
            return ser
    def SendPEEPSetting(self):
        global PEEP
        serial = self.open_serial()
        PEEP_data_to_send = 'p' + str(PEEP) + "\n"
        serial.write(PEEP_data_to_send.encode())
        print("Sending... " + PEEP_data_to_send )
    def SendRRSetting(self):
        global RR
        serial = self.open_serial()
        RR_data_to_send = 'r' + str(RR) + "\n"
        serial.write(RR_data_to_send.encode())
        print("Sending... " + RR_data_to_send )
    def SendFI02Setting(self):
        global FI02
        serial = self.open_serial()
        FI02_data_to_send = 'o' + str(FI02) + "\n"
        serial.write(FI02_data_to_send.encode())
        print("Sending... " + FI02_data_to_send )
    def SendTVSetting(self):
        global TV
        serial = self.open_serial()
        TV_data_to_send = 't' + str(TV) + "\n"
        serial.write(TV_data_to_send.encode())
        print("Sending... " + TV_data_to_send )

    #-----------------------------------------------
    # Functions to receive data from the controller
    #-----------------------------------------------
    def GetSerialData(self):
        global PA, PB, PC, ER1, ER2, FM1, EV1, EV2, PEEP1

        global TV

        s=serial.Serial(port='/dev/ttyACM0', baudrate=9600)
        #string='*00T%'
        while True:
            try:
                #s.write(str.encode(TV))
                #print(string)
                #time.sleep(0.1)
                if s.inWaiting() > 0:
                    inputValue = s.readline()
                    formattedinputvalue = inputValue.strip()
                    encodedvalue = formattedinputvalue.decode('utf-8')

                    splitstring = encodedvalue.split(',')

                    if(splitstring[0]=='PA'):
                        PA = splitstring[1]
                    elif (splitstring[0]=='PB'):
                        PB = splitstring[1]
                    elif(splitstring[0]=='PC'):
                        PC = splitstring[1]
                    elif (splitstring[0] == 'ER1'):
                        ER1 = splitstring[1]
                    elif (splitstring[0] == 'ER2'):
                        ER2 = splitstring[1]
                    elif(splitstring[0]=='FM1'):
                        FM1 = splitstring[1]
                    elif(splitstring[0]=='EV1'):
                        EV1 = splitstring[1]
                    elif (splitstring[0] == 'EV2'):
                        EV2 = splitstring[1]
                    elif(splitstring[0]=='PEEP1'):
                        PEEP1 = splitstring[1]
                    else:
                        # Bad Data, discard
                        print('Received bad data')

                    #print(splitstring[0])
                    #print(splitstring[1])
                    self.PAValue.set(str(PA))
                    self.PBValue.set(str(PB))
                    self.PCValue.set(str(PC))
                    s.flush()
            except:
                print("Failed to receive")

    # ---------------------------------------
    #  PEEP Up / Down Functions
    # ---------------------------------------
    def IncreasePEEP(self):
        global PEEP
        global PEEPmax
        if (PEEP < PEEPmax):
            self.btnDecreasePEEP["state"] = "normal"
            PEEP = PEEP + 1
            self.PEEP.set(str(PEEP))
            if (PEEP >= PEEPmax):
                self.btnIncreasePEEP["state"] = "disabled"
        self.SendPEEPSetting()
    def DecreasePEEP(self):
        global PEEP
        global PEEPmin
        if (PEEP > (PEEPmin)):
            self.btnIncreasePEEP["state"] = "normal"
            PEEP = PEEP - 1
            self.PEEP.set(str(PEEP))
            if (PEEP <= PEEPmin):
                self.btnDecreasePEEP["state"] = "disabled"
        self.SendPEEPSetting()

    #---------------------------------------
    #  Respiration Rate Up / Down Functions
    #---------------------------------------
    def IncreaseRR(self):
        global RR
        global RRmax
        if(RR < RRmax):
            self.btnDecreaseRR["state"] = "normal"
            RR = RR + 1
            self.RR.set(str(RR))
            if(RR >= RRmax):
                self.btnIncreaseRR["state"] = "disabled"
        self.SendRRSetting()
    def DecreaseRR(self):
        global RR
        global RRmin
        if(RR > ( RRmin)):
            self.btnIncreaseRR["state"] = "normal"
            RR = RR - 1
            self.RR.set(str(RR))
            if(RR <= RRmin):
                self.btnDecreaseRR["state"] = "disabled"
        self.SendRRSetting()

    #-------------------------------
    #  O2 Up / Down Functions
    #-------------------------------
    def IncreaseO2(self):
        global FI02
        global FI02max
        if(FI02 < FI02max):
            self.btnDecreaseFI02["state"] = "normal"
            FI02 = FI02 + 1
            self.FI02.set(str(FI02))
            if(FI02 >= FI02max):
                self.btnIncreaseFI02["state"] = "disabled"
        self.SendFI02Setting()
    def DecreaseO2(self):
        global FI02
        global FI02min
        if(FI02 > ( FI02min)):
            self.btnIncreaseFI02["state"] = "normal"
            FI02 = FI02 - 1
            self.FI02.set(str(FI02))
            if(FI02 <= FI02min):
                self.btnDecreaseFI02["state"] = "disabled"
        self.SendFI02Setting()

    #-------------------------------
    #  Tidal Volume Up / Down Functions
    #-------------------------------
    def IncreaseTV(self):
        global TV
        global TVmax
        if(TV < TVmax):
            self.btnDecreaseTV["state"] = "normal"
            TV = TV + 25
            self.TV.set(str(TV))
            if(TV >= TVmax):
                self.btnIncreaseTV["state"] = "disabled"
        self.SendTVSetting()
    def DecreaseTV(self):
        global TV
        global TVmin
        if(TV > TVmin):
            self.btnIncreaseTV["state"] = "normal"
            TV = TV - 25
            self.TV.set(str(TV))
            if(TV <= TVmin):
                self.btnDecreaseTV["state"] = "disabled"
        self.SendTVSetting()

gui = Menu()