import sys
import spidev

## instantiate the spi object
# for Omega2 firmware v0.3.0 and up:
spi = spidev.SpiDev(0, 1)
# for older firmware:
#spi = spidev.SpiDev(32766,1)

# set the speed to 4MHz
spi.max_speed_hz = 1000000

print("Sending Data...")

arr = bytes('Test', 'ascii')
spi.writebytes(arr)

#for i in range(0, repeat):
#    # perform the transfer
#    #spi.xfer(vals)
#    spi.writebytes(vals)

print("A \n\r")

