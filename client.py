#Team Midas
import socket

#Globals
Revenue = 0
W_cost = 0
J_cost = 0
D_cost = 0

Demand = []
Config = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creates a connection to the game server and starts the game
def init():
    global s
    s.connect(("hackathon.hopto.org", 27832))
    s.send("INIT Midas")
    data = s.recv(1024)
    print data
    s.send("RECD")
    data = s.recv(1024)
    print data
    parseCost(data)
    s.send("START")
    data = s.recv(1024)
    print data

#parses cost data and stores it in the respective globals
def parseCost(data):
    global Revenue 
    global W_cost
    global J_cost
    global D_cost
    cost = data.split()
    Revenue = int(cost[1])
    W_cost = int(cost[2])
    J_cost = int(cost[3])
    D_cost = int(cost[4])
    print "REVENUE "+ str(Revenue)
    print "WEB " + str(W_cost)
    print "Java " + str(J_cost)
    print "Data " + str(D_cost)

def move():
    global Revenue
    global W_cost
    global J_cost
    global D_cost
    global Demand

    if (True):
        return "CONTROL 0 0 0 0 0 0 0 0 0"

#parses demand data and stores it in global Demand
#global Demand will later be used to predict future demand
def parseDemand(data):
    global Demand
    demand = data.split()
    demand.pop(0)
    Demand.append(("Date", demand[0] + " " + demand[1] + ":" + demand[2] + ":" + demand[3]))
    Demand.append(("Demand", ("NA", demand[4]), ("EU", demand[5]), ("AP", demand[6])))

#Pretty prints Demand
def printDemand():
    for i in range (0,len(Demand),2):
        print str(Demand[i]) + "\t" + str(Demand[i+1])

#Stores our current number of servers in each region into Config
def parseConfig(data):
    global Config
    config = data.split()
    config.pop(0)
    Config["W.na"] = config[0]
    Config["W.eu"] = config[1]
    Config["W.ap"] = config[2]
    Config["J.na"] = config[3]
    Config["J.eu"] = config[4]
    Config["J.ap"] = config[5]
    Config["D.na"] = config[6]
    Config["D.eu"] = config[7]
    Config["D.ap"] = config[8]
    

#Pretty prints a key-value pair in Config
#x is the tier.region you're looking for
#e.g. printConfig("W.na") prints the number of servers in the Web tier of North America
#case-sensitive
def printConfig(x):
    print x + ": " + Config[x]

#Pretty prints all key-value pairs in Config
def printAllConfig():
    configKeys = sorted(Config.keys())
    configKeys.reverse()
    for i in range(0,len(configKeys),3):
        print configKeys[i] + ": " + Config[configKeys[i]] + " \t" + configKeys[i+1] + ": " + Config[configKeys[i+1]] + " \t" + configKeys[i+2] + ": " + Config[configKeys[i+2]]


def main():
    init()
    data = ""
#    while (data != "END"):
    for i in xrange(0,2):
        s.send("RECD")
        #DATA
        data = s.recv(1024)
        print data
        parseDemand(data)
        s.send("RECD")
        #DIST
        data = s.recv(1024)
        print data
        s.send("RECD")
        #PROFIT
        data = s.recv(1024)
        print data
        s.send(move())
        print ""
        #CONFIG
        data = s.recv(1024)
        print data
        parseConfig(data)
    s.send("STOP")
    s.close()

main()
printAllConfig()

print "\nENDED"
