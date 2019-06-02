

MacaddrOfS = 6
MacaddrOfD = 6
MinDatapayload = 0
MaxDatapayload = 84
CRC = 4

timeslot=100
syncFrame = 10
dataFrame = 80
ACKFrame = 10



def getCDataRate():
    MaxFrame = MacaddrOfS + MacaddrOfD + MaxDatapayload + CRC
    MaxDatarateOfChannel = (MaxFrame * 8 / 1048576) / (timeslot * 0.000001)
    print("Channel data rate: %f Mbit/sec" % MaxDatarateOfChannel)

def getUDataRate():
    for payload in range(MinDatapayload, MaxDatapayload + 1):
        Frame = MacaddrOfS + MacaddrOfD + payload + CRC
        DatarateofUser = (Frame * 8 / 1048576) / (timeslot * 0.000001)
        print("user data rate:: %f Mbit/sec with payload %d bytes" % (DatarateofUser, payload))


getCDataRate()
getUDataRate()
