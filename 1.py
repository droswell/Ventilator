from tkinter import *

VentilatorStatus = False

def StartVentilator():
    VentilatorStatusLabel.config(text="Running...", fg="#0e7825")
    StartVentilationButton.config(text="Stop Ventilating", bg="#b30000", fg='#FFFFFF')


def StopVentilator():
    VentilatorStatusLabel.config(text="Stopped", fg="red")
    StartVentilationButton.config(text="Start Ventilating", bg="#0e7825")


def ChangeStatus():
    global VentilatorStatus
    if VentilatorStatus == False:
        StartVentilator()
        VentilatorStatus = True
    else:
        StopVentilator()
        VentilatorStatus = False




root = Tk()
root.geometry("1024x768")
# These make the columns and rows expand when the window is resized
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

#---------------
# Top Left Frame
#---------------
TopLeftFrame=LabelFrame(root, borderwidth=1, relief="sunken", text="Oxygen Level", font=("Arial", 18, "bold"))
TopLeftFrame.grid(row=0, column=0, sticky=NSEW, padx=20, pady=10)
# These make the columns and rows expand when the window is resized
TopLeftFrame.grid_columnconfigure(0, weight=3)
TopLeftFrame.grid_columnconfigure(1, weight=2)
TopLeftFrame.grid_columnconfigure(2, weight=2)
TopLeftFrame.grid_rowconfigure(0, weight=1)
TopLeftFrame.grid_rowconfigure(1, weight=1)
# Add the widgets to the frame
O2UpButton = Button(TopLeftFrame, text="+", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
O2UpButton.grid(row=0, column=0, padx=(10, 5), pady=(15, 7), sticky=NSEW)
O2DownButton = Button(TopLeftFrame, text="-", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
O2DownButton.grid(row=1, column=0, padx=(10, 5), pady=(7, 15), sticky=NSEW)
O2Level = Label(TopLeftFrame, text="00", font=("Arial", 36, "bold"), width=5, height=4, bg="#C8C8C8", borderwidth=1, relief="sunken")
O2Level.grid(row=0, column=1, rowspan=2, padx=0, pady=15)
O2PercentLabel = Label(TopLeftFrame, text=" % ", font=("Arial", 30, "bold"), width=3)
O2PercentLabel.grid(row=0, column=2, rowspan=2, sticky=NSEW, padx=(0, 20))

#-----------------
# Top Right Frame
#-----------------
TopRightFrame=LabelFrame(root, borderwidth=1, relief="sunken", text="Total Volume", font=("Arial", 18, "bold"))
TopRightFrame.grid(row=0, column=1, sticky=NSEW, padx=20, pady=10)
# These make the columns and rows expand when the window is resized
TopRightFrame.grid_columnconfigure(0, weight=3)
TopRightFrame.grid_columnconfigure(1, weight=2)
TopRightFrame.grid_columnconfigure(2, weight=2)
TopRightFrame.grid_rowconfigure(0, weight=1)
TopRightFrame.grid_rowconfigure(1, weight=1)
# Add the widgets to the frame
TotalVolumeUpButton = Button(TopRightFrame, text="+", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
TotalVolumeUpButton.grid(row=0, column=0, padx=(10, 5), pady=(15, 7), sticky=NSEW)
TotalVolumeDownButton = Button(TopRightFrame, text="-", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
TotalVolumeDownButton.grid(row=1, column=0, padx=(10, 5), pady=(7, 15), sticky=NSEW)
TotalVolumeLevel = Label(TopRightFrame, text="600", font=("Arial", 36, "bold"), width=5, height=4, bg="#C8C8C8", borderwidth=1, relief="sunken")
TotalVolumeLevel.grid(row=0, column=1, rowspan=2, padx=0, pady=15)
TotalVolumeLabel = Label(TopRightFrame, text="ml", font=("Arial", 30, "bold"), width=3)
TotalVolumeLabel.grid(row=0, column=2, rowspan=2, sticky=NSEW, padx=(0,20))

#-------------------
# Bottom Right Frame
#-------------------
BottomRightFrame=LabelFrame(root, borderwidth=1, relief="sunken", text="Inspiratory Rate", font=("Arial", 18, "bold"))
BottomRightFrame.grid(row=1, column=1, sticky=NSEW, padx=20, pady=10)
# These make the columns and rows expand when the window is resized
BottomRightFrame.grid_columnconfigure(0, weight=3)
BottomRightFrame.grid_columnconfigure(1, weight=2)
BottomRightFrame.grid_columnconfigure(2, weight=2)
BottomRightFrame.grid_rowconfigure(0, weight=1)
BottomRightFrame.grid_rowconfigure(1, weight=1)
# Add the widgets to the frame
InspiratoryRateUpButton = Button(BottomRightFrame, text="+", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
InspiratoryRateUpButton.grid(row=0, column=0, padx=(10, 5), pady=(15, 7), sticky=NSEW)
InspiratoryRateDownButton = Button(BottomRightFrame, text="-", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
InspiratoryRateDownButton.grid(row=1, column=0, padx=(10, 5), pady=(7, 15), sticky=NSEW)
InspiratoryRateLevel = Label(BottomRightFrame, text="1.1", font=("Arial", 36, "bold"), width=5, height=4, bg="#C8C8C8", borderwidth=1, relief="sunken")
InspiratoryRateLevel.grid(row=0, column=1, rowspan=2, padx=0, pady=15)
InspiratoryRatePercentLabel  = Label(BottomRightFrame, text=" s ", font=("Arial", 30, "bold"), width=3)
InspiratoryRatePercentLabel .grid(row=0, column=2, rowspan=2, sticky=NSEW, padx=(0,20))

#-------------------
# Bottom Left Frame
#-------------------
BottomLeftFrame=LabelFrame(root, borderwidth=1, relief="sunken", text="Respiratory Rate", font=("Arial", 18, "bold"))
BottomLeftFrame.grid(row=1, column=0, sticky=NSEW, padx=20, pady=10)
# These make the columns and rows expand when the window is resized
BottomLeftFrame.grid_columnconfigure(0, weight=3)
BottomLeftFrame.grid_columnconfigure(1, weight=2)
BottomLeftFrame.grid_columnconfigure(2, weight=2)
BottomLeftFrame.grid_rowconfigure(0, weight=1)
BottomLeftFrame.grid_rowconfigure(1, weight=1)
# Add the widgets to the frame
RespiratoryRateUpButton = Button(BottomLeftFrame, text="+", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
RespiratoryRateUpButton.grid(row=0, column=0, padx=(10, 5), pady=(15, 7), sticky=NSEW)
RespiratoryRateDownDownButton = Button(BottomLeftFrame, text="-", width=5, bg="#A6B8C0", font=("Arial", 36, "bold"))
RespiratoryRateDownDownButton.grid(row=1, column=0, padx=(10, 5), pady=(7, 15), sticky=NSEW)
RespiratoryRateLevel = Label(BottomLeftFrame, text="15", font=("Arial", 36, "bold"), width=5, height=4, bg="#C8C8C8", borderwidth=1, relief="sunken")
RespiratoryRateLevel.grid(row=0, column=1, rowspan=2, padx=0, pady=15)
RespiratoryRatePercentLabel  = Label(BottomLeftFrame, text="bpm", font=("Arial", 30, "bold"), width=3)
RespiratoryRatePercentLabel .grid(row=0, column=2, rowspan=2, sticky=NSEW, padx=(0,20))




# Bottom frame for enabling ventilation controls
BottomFrame=LabelFrame(root, borderwidth=1, width=200, height=150)
BottomFrame.grid(row=2, column=0, columnspan=2, sticky=NSEW, padx=20, pady=5)
VentilatorStatusLabel = Label(BottomFrame, font=("Arial", 28, "bold"), justify="center")
VentilatorStatusLabel.grid(row=2, column=0, pady=15)
StartVentilationButton = Button(root, command=ChangeStatus, font=("Arial", 24, "bold"), borderwidth=3, fg="#FFFFFF")
StartVentilationButton.grid(row=2, column=1, columnspan=2, padx=15, pady=5, sticky=NSEW)
# When the device is turned on make sure it starts in off state
StopVentilator()





root.mainloop()
