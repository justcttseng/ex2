import random
from typing import List

import numpy as NP

STATE_SILENT = 'SILENT'
STATE_ACTIVE = 'ACTIVE'
STATE_CO = 'COLLISION'
STATE_BO = 'BACKOFF'
STATE_TX = 'SUCCESS'
STATE_IDLE = "IDLE"
MAX_RETX = 4


class simulation:
    MacaddrOfS = 6
    MacaddrOfD = 6
    MinDatapayload = 0
    MaxDatapayload = 84
    CRC = 4

    timeslot = 100
    syncFrame = 10
    dataFrame = 80
    ACKFrame = 10
    RetryRound = 3


    node = []

    def __init__(self, num_of_time_slots, num_of_nodes, prob_of_queue):
        self.num_of_time_slots = num_of_time_slots
        self.num_of_nodes = num_of_nodes
        self.prob_of_queue = prob_of_queue
        self.CheckActivies = [STATE_SILENT] * (self.num_of_nodes)
        self.t = 0
        self.results = [[STATE_SILENT for j in range(num_of_time_slots)] for i in range(self.num_of_nodes)]


    def print(self):
        s = 't= ' + str(self.num_of_time_slots) + ',N= ' + str(self.num_of_nodes) + ',Prob= ' + str(self.prob_of_queue)
        print(s)

    def getCDataRate(self):
        maxframe = simulation.MacaddrOfS + simulation.MacaddrOfD + simulation.MaxDatapayload + simulation.CRC
        maxdatarateofchannel = (maxframe * 8 / 1048576) / (simulation.timeslot * 0.000001)
        print("Channel data rate: %f Mbit/sec" % maxdatarateofchannel)

    def getUDataRate(self):
        for payload in range(simulation.MinDatapayload, simulation.MaxDatapayload + 1):
            frame = simulation.MacaddrOfS + simulation.MacaddrOfD + payload + simulation.CRC
            datarateofuser = (frame * 8 / 1048576) / (simulation.timeslot * 0.000001)
            print("user data rate:: %f Mbit/sec with payload %d bytes" % (datarateofuser, payload))

    def checkcctivies(self):

        rangeP = [i / 100 for i in range(10, 110, 10)]

        for n in range(len(self.CheckActivies)):
            if self.CheckActivies[n] == STATE_SILENT:
                if NP.random.choice(rangeP) <= self.prob_of_queue[n]:
                    self.CheckActivies[n] = STATE_ACTIVE

    def iscollision(self):
        count = 0

        for n in range(len(self.CheckActivies)):
            if self.CheckActivies[n] == STATE_ACTIVE:
                count+=1;
        return count

    def print_results(self):
        for j in range(self.num_of_time_slots):
            print('t= ' + str(j+1), end=' ')
            for i in range(len(self.CheckActivies)):
                print(self.results[i][j], end = ' ')
            print("\n")


    def transmission(self):

        backofftime = [0] * (self.num_of_nodes)

        if simulation.iscollision(self) > 1:


            for i in range(len(self.CheckActivies)):
                if self.CheckActivies[i] == STATE_ACTIVE:
                    self.results[i][self.t] = STATE_CO

            self.t += 1
            n = 1

            while n < 4:
                for i in range(len(self.CheckActivies)):
                    if self.CheckActivies[i] == STATE_ACTIVE:
                        backofftime[i] = simulation.get_random_backoff_time(n)
                        self.results[i][self.t] = STATE_CO
                        self.CheckActivies[i] = STATE_CO
                hightest = max(backofftime)
                print(backofftime)


                if len(backofftime) == len(set(backofftime)):
                    print("fuck")
                    # for i in range(len(self.backofftime)):
                    #
                    # #     for j in range(1,backofftime[i]):
                    # #         self.results[i][self.t + j] = STATE_BO
                    # #     self.results[self.t+backofftime[i]+1] = STATE_TX
                    # #     if (hightest-backofftime[i]) > 0:
                    # #         for k in range(hightest-backofftime(i)):
                    # #             self.results[i][self.t + k + 1] = STATE_BO

                else:
                    for i in range(len(backofftime)):
                        if backofftime[i] != 0:
                            for j in range(backofftime[i]):
                                # self.results[i][self.t + j + 1] = STATE_BO
                                print(STATE_BO)

                    n+=1

            #
            # for i in range(len(self.CheckActivies)):
            #     if self.CheckActivies[i] == STATE_ACTIVE:
            #         self.results[i][self.t] = STATE_TX
            # self.t += 1

            # n = 0
            #
            # while n < 4:
            #     for i in range(len(self.CheckActivies)):
            #         if self.CheckActivies[i] == STATE_ACTIVE:
            #             n+=1
            #             backofftime[i] = simulation.get_random_backoff_time(n)
            #             # self.results[i][self.t] = STATE_CO + ':'+str(n)
            #             print(self.results[i][self.t])
            #
            #     # if len(backofftime) == len(set(backofftime)):
            #     #
            #     #     for i in range(len(self.CheckActivies)):
            #     #         for bo in range(len(backofftime)):
            #     #             if backofftime[i] != 0:
            #     #                 # self.results[i][self.t + bo + 1] = STATE_BO
            #     #                 # self.results[i][self.t + bo + 2] = STATE_TX
            #     #                 print('===')
            #     #     self.t += ( max(backofftime)+2)
            #     # else:
            #     #     n+=1
            #     n+=1
            #

        else:
            if simulation.iscollision(self) == 0:
                for i in range(len(self.CheckActivies)):
                    if self.CheckActivies[i] == STATE_SILENT:
                        self.results[i][self.t] = STATE_IDLE
                self.t += 1
            else:
                for i in range(len(self.CheckActivies)):
                    if self.CheckActivies[i] == STATE_ACTIVE:
                        self.results[i][self.t] = STATE_TX
                self.t += 1
        for i in range(len(self.CheckActivies)):
            self.CheckActivies[i] = STATE_SILENT

    def simulation_for_the_comm_of_multi_nodes(self):

        for i in range(self.num_of_time_slots):
            simulation.checkcctivies(self)
            simulation.transmission(self)


        simulation.print_results(self)


        ##print(simulation.get_random_backoff_time(3))

    # def trysend(self):
    #     for n in self.num_of_nodes:
    #         if uniform(0,1) < self.prob_of_queue[n]:
    #
    #
    # def retry(self,n):
    #     for t in simulation.RetryRound:

    def get_random_backoff_time(i):
        return NP.random.randint(0, pow(2, i))


## getCDataRate()
## getUDataRate()

s1 = simulation(20, 3, [0.1, 0.1, 0.1])
# s1.getUDataRate();
# s1.getCDataRate();
# s2 = simulation(200,3,[0.3,0.3,0.3])
# s3 = simulation(200,3,[0,5,0.5,0,5])
# s4 = simulation(200,3,[1,0,0])

s1.simulation_for_the_comm_of_multi_nodes();
# s2.simulation_for_the_comm_of_multi_nodes();
# s3.simulation_for_the_comm_of_multi_nodes();
# s4.simulation_for_the_comm_of_multi_nodes();
# s2.print();
# s3.print();
# s4.print();
