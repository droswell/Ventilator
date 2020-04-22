from tkinter import *

root = Tk()
root.geometry("800x600")

TopLeftFrame=Frame(root, bg="blue")
TopLeftFrame.grid(row=0, column=0, sticky=NSEW, padx=15, pady=15)
O2UpButton = Button(TopLeftFrame, text="O2 +", width=12, height=4)
O2UpButton.grid(row=0, column=0, padx=10, pady=10)
#O2DownButton = Button(TopLeftFrame, text="O2 -", width=12, height=4)
#O2DownButton.grid(row=1, column=0, padx=10, pady=10)
#O2Level = Label(TopLeftFrame, text="O2 Level", width=15, height=10)
#O2Level.grid(row=0, column=1, rowspan=2, pady=10)
#O2PercentLabel = Label(TopLeftFrame, text="%", width=5, height=10)
#O2PercentLabel.grid(row=0, column=2, rowspan=2,padx=5, pady=10)

root.mainloop()